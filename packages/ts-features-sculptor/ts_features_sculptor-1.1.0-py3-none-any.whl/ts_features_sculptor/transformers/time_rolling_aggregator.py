#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by dmitrii at 05.01.2025

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Optional, Union, Callable
from sklearn.base import BaseEstimator, TransformerMixin
from ts_features_sculptor.transformers.time_validator import TimeValidator


@dataclass
class TimeRollingAggregator(BaseEstimator, TransformerMixin, TimeValidator):
    """
    Выполняет аггрегирование в скользящем окне. Окно задается в днях.

    Parameters
    ----------
    time_col : str, default='time'
        Имя столбца с временными метками.
    feature_col : str, default='tte'
        Имя столбца с данными для аггрегации.
    window_days : int, default=3
        Размер временного окна в днях для расчёта агрегации.
    agg_funcs : List[Union[str, Callable]], default=['mean']
        Список аггрегирующих функций (например, 'mean', 'max').
    fillna : Optional[float], default=0
        Значение для заполнения пропусков.
    shift : int, default=0
        Определяет выбор интервала для скользящего окна:
        - Если shift=0, используется полуоткрытый интервал 
          [current_time - window_days, current_time)
          (текущая строка исключается из расчёта).
        - Если shift=1, используется полуоткрытый интервал 
          (current_time - window_days, current_time]
          (текущая строка включается в расчёт).

    Methods
    -------
    fit(X, y=None)
        Возвращает self.
    transform(X)
        Добавляет столбцы с новыми агрегированными статистиками. 
        Для каждой функции агрегации создаётся отдельный столбец 
        с именем:
        {feature_col}_time_rolling_{func_name}_{window_days}.

    Notes
    -----
    При shift=0 используется полуоткрытый интервал 
    [current_time - window_days, current_time)
    - Пример с  `shift=0` и `window_days=5`, текущая строка исключается 
      из расчёта:

              time  tte      tte_time_rolling_mean_5
        2025-01-01  2.0                          NaN
        2025-01-03  3.0                2 = 2     2.0  <-- не знаем о tte = 3
        2025-01-06  4.0      (2 + 3) / 2 = 2.5   2.5  <-- не знаем о tte = 4
        2025-01-10  NaN                4 = 4     4.0

    Если `tte` является целевой переменной, то при использовании 
    полученного датасета для обучения модели утечки данных не будет.

    При shift=1 используется полуоткрытый интервал 
    (current_time - window_days, current_time]
    - Пример с  `shift=1`, текущая строка попадает в расчёт:

              time  tte  tte_time_rolling_mean_5
        2025-01-01  2.0                      2.0  <-- знаем о tte = 2
        2025-01-03  3.0                      2.5  <-- знаем о tte = 3
        2025-01-06  4.0                      3.5  <-- знаем о tte = 4
        2025-01-10  NaN                      4.0

    Если `tte` является целевой переменной, то при использовании 
    полученного датасета для обучения модели произойдёт утечка данных.

    Для приведения значений столбца со временем к datetime и сортировки
    используйте трансформеры ToDatetime и SortByTime.

    Наследует TimeValidator для проверки того, что в колонке time_col
    содержатся отсортированные значения datetime.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> data = {
    ...     "time": [
    ...         "2025-01-01", "2025-01-03", "2025-01-06", "2025-01-10"],
    ...     "tte": [2., 3., 4., np.nan]
    ... }
    >>> df = pd.DataFrame(data)
    >>> df["time"] = pd.to_datetime(df["time"])
    >>> transformer = TimeRollingAggregator(
    ...     time_col="time",
    ...     feature_col="tte",
    ...     window_days=5,
    ...     agg_funcs=['mean'],
    ...     fillna=np.nan,
    ...     shift=0
    ... )
    >>> result_df = transformer.transform(df)
    >>> print(result_df.to_string(index=False))
          time  tte  tte_time_rolling_mean_5
    2025-01-01  2.0                      NaN
    2025-01-03  3.0                      2.0
    2025-01-06  4.0                      2.5
    2025-01-10  NaN                      4.0
    """

    time_col: str = 'time'
    feature_col: str = 'tte'
    window_days: int = 3
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
                f"{self.feature_col}_time_rolling_{func_name}_"
                f"{self.window_days}"
            )
            X_copy[col_name] = X_copy.rolling(
                window=f"{self.window_days}d",
                on=self.time_col,
                min_periods=1,
                closed=closed_interval
            )[self.feature_col].agg(func)
            if self.fillna is not None:
                X_copy[col_name] = X_copy[col_name].fillna(self.fillna)

        return X_copy


if __name__ == "__main__":
    import pandas as pd
    import numpy as np


    data = {
        "time": [
            "2025-01-01", "2025-01-03", "2025-01-06", "2025-01-10"],
        "tte": [2., 3., 4., np.nan]
    }
    df = pd.DataFrame(data)
    df["time"] = pd.to_datetime(df["time"])
    transformer = TimeRollingAggregator(
        time_col="time",
        feature_col="tte",
        window_days=5,
        agg_funcs=['mean'],
        fillna=np.nan,
        shift=1
    )
    result_df = transformer.transform(df)
    print(result_df.to_string(index=False))
