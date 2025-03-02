#!/usr/bin/env python3
# -*- coding: utf-8 -*
# Created by dmitrii at 07.01.2025

import pandas as pd
import numpy as np
from ts_features_sculptor import Lag


def test_lag_transformer_default_params():
    """
    Тест трансформера Lag с параметрами по умолчанию
    """

    data = {
        'time': pd.to_datetime(
            ['2025-01-01', '2025-01-04', '2025-01-05', '2025-01-10']),
        'tte': [2.0, 3.0, 4.0, 5.0]
    }
    df = pd.DataFrame(data)
    
    transformer = Lag()
    result_df = transformer.transform(df)
    
    assert 'tte_lag_1' in result_df.columns
    
    expected_lag_values = [0.0, 2.0, 3.0, 4.0]
    np.testing.assert_array_equal(
        result_df['tte_lag_1'].values, expected_lag_values)
