#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Created by dmitrii at 08.01.2025

import pandas as pd
import numpy as np
from ts_features_sculptor import TimeRollingAggregator


def test_time_rolling_aggregator_default_params():
    """
    Тест трансформера TimeRollingAggregator с параметрами по умолчанию.
    """

    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-03', '2025-01-06', '2025-01-10']),
        'tte': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = TimeRollingAggregator()
    result_df = transformer.transform(df)
    
    expected_col = 'tte_time_rolling_mean_3'
    assert expected_col in result_df.columns

    # расчет для 2025-01-06
    # '2025-01-01'    2 
    # '2025-01-02'    -  
    # '2025-01-03'    3 ---
    # '2025-01-04'    -
    # '2025-01-05'    - --- 3 дней, 3
    # '2025-01-06'    4  
    # '2025-01-07'    -
    # '2025-01-08'    -
    # '2025-01-09'    -
    # '2025-01-10'    5
    
    # C учетом shift=0 (left-closed), window_days=3 дня и fillna=0 
    # по умолчанию
    # первое значение будет заполнено 0
    # Второе значение: 2.0 (только первое значение в окне 3 дней)
    # Третье значение: 3.0 (окно 3 дня)
    # Четвертое значение: 0 (в окне перед 2025-01-10 ничего нет)
    expected_values = [0.0, 2.0, 3.0, 0.0]
    np.testing.assert_array_almost_equal(
        result_df[expected_col].values,
        expected_values
    )


def test_time_rolling_aggregator_with_shift():
    """
    Тест трансформера TimeRollingAggregator с shift=1.
    """

    data = {
        'time': pd.to_datetime([
            '2025-01-01', '2025-01-03', '2025-01-06', '2025-01-10']),
        'tte': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = TimeRollingAggregator(
        window_days=5,
        shift=1,
        fillna=np.nan
    )
    result_df = transformer.transform(df)
    
    expected_col = 'tte_time_rolling_mean_5'
    assert expected_col in result_df.columns

    # расчет для 2025-01-06
    # '2025-01-01'    2
    # '2025-01-02'    -  ---
    # '2025-01-03'    3
    # '2025-01-04'    -
    # '2025-01-05'    -
    # '2025-01-06'    4  --- 5 дней, (3 + 4) / 2 = 3.5
    # '2025-01-07'    -
    # '2025-01-08'    -
    # '2025-01-09'    -
    # '2025-01-10'    5
    # 
    # с учетом shift=1 и window_days=5)
    # Первое значение: 2.0 (текущее значение)
    # Второе значение: (2.0 + 3.0) / 2 = 2.5
    # Третье значение: (3.0 + 4.0) / 2 = 3.5
    # Четвертое значение: (4.0 + 5.0) / 2 = 4.5
    expected_values = [2.0, 2.5, 3.5, 4.5]
    np.testing.assert_array_almost_equal(
        result_df[expected_col].values,
        expected_values
    )
