#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by dmitrii at 05.01.2025

from dataclasses import dataclass, field
from typing import List, Optional, Union, Callable
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from ts_features_sculptor.transformers.time_validator import TimeValidator


@dataclass
class RowRollingAggregator(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Выполняет аггрегирование в скользящем окне с исключением текущей 
    строки. Окно определяется числом строк.

    Parameters
    ----------
    time_col : str, default="time"
        Имя столбца с временными метками.
    feature_col : str, default="tte"
        Имя столбца с данными для аггрегации.
    window_size : Optional[int], default=3
        Размер скользящего окна для расчёта агрегации.
    agg_funcs : List[Union[str, Callable]], default=["mean"]
        Список аггрегирующих функций (например, "mean", "max").
    fillna : Optional[float], default=0
        Значение для заполнения пропусков.
    shift : int, default=0
        Определяет выбор интервала для скользящего окна.
        Если 0, используется полуоткрытый интервал 
        [current_time - window_size, current_time)
        (текущая строка исключается), если 1, используется полуоткрытый 
        интервал (current_time - window_size, current_time]
        (текущая строка включается).

    Methods
    -------
    fit(X, y=None)
        Не используется, возвращает self.

    transform(X)
        Добавляет столбцы с новыми аггрегированными статистиками. Для 
        каждой функции агрегации создается отдельный столбец с именем:
        `{feature_col}_row_rolling_{func_name}_{window_size}`.
        
    Notes
    -----
    Текущая строка исключается из расчёта агрегатов для предотвращения 
    утечки данных при обучении. Исключение достигается за счет 
    использования полуоткрытого интервала 
    [current_time - `window_size`, current_time) с параметром closed="left" 
    (при shift=0) или (current_time - `window_size`, current_time] 
    с параметром closed="right" (при shift=1).

    Для приведения значений столбца со временем к datetime и сортировки
    используйте трансформеры `ToDatetime` и `SortByTime`.

    Наследует `TimeValidator` для проверки того, что в колонке `time_col`
    содержаться отсортированные значения datetime.

    При  `shift=0` и `window_size=2` текущая строка исключается из 
    расчёта:

          time  tte  tte_row_rolling_mean_2
    2025-01-01  2.0                     NaN
    2025-01-04  3.0              2 = 2  2.0  <-- не знаем о tte = 3
    2025-01-05  4.0  (2 + 3) / 2 = 2.5  2.5  <-- не знаем о tte = 4
    2025-01-10  NaN  (3 + 4) / 2 = 3.5  3.5  <-- текущий tte не известен

    Если `tte` является целевой переменной, то при использовании 
    полученного датасета для обучения модели утечки данных не будет.

    При `shift=1` и `window_size=2` текущая строка попадает в расчёт:

          time  tte  tte_row_rolling_mean_2
    2025-01-01  2.0              2 = 2  2.0  <-- знаем о tte = 2
    2025-01-04  3.0  (2 + 3) / 2 = 2.5  2.5  <-- знаем о tte = 3
    2025-01-05  4.0  (3 + 4) / 2 = 3.5  3.5  <-- знаем о tte = 4
    2025-01-10  NaN                     NaN

    Если `tte` является целевой переменной, то при использовании 
    полученного датасета для обучения модели произойдёт утечка данных.


    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> data = {
    ...     "time": [
    ... "2025-01-01", "2025-01-04", "2025-01-05", "2025-01-10"],
    ...     "tte": [2., 3., 4., np.nan]
    ... }
    >>> df = pd.DataFrame(data)
    >>> df["time"] = pd.to_datetime(df["time"])
    >>> transformer = RowRollingAggregator(
    ...     time_col="time",
    ...     feature_col="tte",
    ...     window_size=2,
    ...     agg_funcs=['mean'],
    ...     fillna=np.nan,
    ...     shift=0
    ... )
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
          time  tte  tte_row_rolling_mean_2
    2025-01-01  2.0                     NaN
    2025-01-04  3.0                     2.0
    2025-01-05  4.0                     2.5
    2025-01-10  NaN                     3.5
    """

    time_col: str = 'time'
    feature_col: str = 'tte'
    window_size: Optional[int] = 3
    agg_funcs: List[Union[str, Callable]] = field(
        default_factory=lambda: ['mean'])
    fillna: Optional[float] = 0
    shift: int = 0

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        self._validate_time_column(X)

        X_copy = X.copy()

        closed_interval = "left" if self.shift == 0 else "right"
        for func in self.agg_funcs:
            func_name = func.__name__ if callable(func) else func
            col_name = (
                f"{self.feature_col}_row_rolling_{func_name}_"
                f"{self.window_size}"
            )
            X_copy[col_name] = X_copy[self.feature_col].rolling(
                self.window_size, min_periods=1, closed=closed_interval
            ).agg(func)
            if self.fillna is not None:
                X_copy[col_name] = X_copy[col_name].fillna(self.fillna)

        return X_copy
