import pytest
import pandas as pd
import numpy as np
from temporal_disaggregation.aggregation import TemporalAggregation

@pytest.fixture
def aggregator():
    """Instancia un objeto TemporalAggregation para pruebas."""
    return TemporalAggregation(conversion="sum")

def test_aggregation(aggregator):
    """Verifica que la agregación temporal devuelve valores correctos."""
    df = pd.DataFrame({
        "Date": pd.date_range("2023-01-01", periods=12, freq="ME"),
        "Value": np.arange(1, 13)
    })

    result = aggregator.aggregate(df, time_col="Date", value_col="Value", freq="QE")
    
    # Verificar que la suma sea correcta
    expected_sums = [1+2+3, 4+5+6, 7+8+9, 10+11+12]
    assert result["Value"].tolist() == expected_sums, f"Los valores agregados no coinciden: {result['Value'].tolist()}"
