#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Created by dmitrii at 07.01.2025

import pandas as pd
import numpy as np
from ts_features_sculptor import RowRollingAggregator


def test_row_rolling_aggregator_default_params():
    """
    Тест трансформера RowRollingAggregator. Значения по умолчанию.
    """
    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-04', '2025-01-05', '2025-01-10']),
        'tte': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = RowRollingAggregator()
    result_df = transformer.transform(df)
    
    # Проверяем, что добавлен столбец с агрегацией
    expected_col = 'tte_row_rolling_mean_3'
    assert expected_col in result_df.columns
    
    # С учетом shift=0, window_size=3 и fillna=0 по умолчанию
    # второе значение 2
    # третье значение (2.0 + 3.0) / 2 = 2.5
    # четвертое значение (2.0 + 3.0 + 4.0) / 3 = 3.0
    expected_values = [0.0, 2.0, 2.5, 3.0]
    np.testing.assert_array_almost_equal(
        result_df[expected_col].values,
        expected_values
    )
