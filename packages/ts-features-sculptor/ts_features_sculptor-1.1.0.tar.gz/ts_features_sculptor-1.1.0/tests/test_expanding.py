#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Created by dmitrii at 07.01.2025

import pandas as pd
import numpy as np
from ts_features_sculptor import Expanding


def test_expanding_transformer_default_params():
    """
    Тест трансформера Expanding.
    """

    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-04', '2025-01-05', '2025-01-10']),
        'value': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = Expanding()
    result_df = transformer.transform(df)
    
    assert 'value_expanding_mean' in result_df.columns
    
    # с учетом, что  shift=1 по умолчанию
    expected_values = [0.0, 2.0, 2.5, 3.0]
    np.testing.assert_array_almost_equal(
        result_df['value_expanding_mean'].values,
        expected_values
    )


def test_expanding_transformer_no_shift():
    """
    Тест трансформера Expanding без сдвига (shift=0)
    """
    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-04', '2025-01-05', '2025-01-10']),
        'value': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = Expanding(shift=0)
    result_df = transformer.transform(df)
    
    # Проверяем значения без сдвига
    expected_values = [2.0, 2.5, 3.0, 3.5]
    np.testing.assert_array_almost_equal(
        result_df['value_expanding_mean'].values,
        expected_values
    )
