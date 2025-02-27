import pytest
import numpy as np
import pandas as pd
from temporal_disaggregation.processor import TimeSeriesProcessor

# 📆 Definir fechas y frecuencias
start_date_hf = "2001-01-01"
end_date_hf = "2024-01-01"
start_date_lf = "2001-01-01"
end_date_lf = "2024-01-01"
freq_hf = "ME"  # Mensual
freq_lf = "YE"  # Anual

# Generar valores de alta y baja frecuencia
num_months = pd.date_range(start_date_hf, end_date_hf, freq=freq_hf).shape[0]
num_years = pd.date_range(start_date_lf, end_date_lf, freq=freq_lf).shape[0]
values_hf = np.linspace(100, 350, num_months)
values_lf = np.linspace(150, 500, num_years)

@pytest.fixture
def processor():
    """Instancia un objeto TimeSeriesProcessor para pruebas."""
    return TimeSeriesProcessor(values_hf, start_date_hf, end_date_hf, freq_hf,
                               values_lf, start_date_lf, end_date_lf, freq_lf)

def test_creation(processor):
    """Verifica que el objeto TimeSeriesProcessor se crea correctamente."""
    assert processor is not None
    assert isinstance(processor.ts_high_freq, pd.DataFrame)
    assert isinstance(processor.ts_low_freq, pd.DataFrame)

def test_merge_series(processor):
    """Verifica que la serie fusionada no contenga valores nulos y tenga las columnas esperadas."""
    merged_series = processor.process_and_merge_series()
    
    # Validar que no haya valores nulos
    assert not merged_series.isnull().values.any(), "La serie fusionada contiene valores nulos."
    
    # Validar que contenga las columnas esperadas
    expected_columns = {"Index", "Grain", "X", "y"}
    assert set(merged_series.columns) == expected_columns, f"Las columnas esperadas son {expected_columns}, pero se encontraron {merged_series.columns}"

def test_frequency_inference(processor):
    """Verifica que la inferencia de frecuencia funcione correctamente."""
    assert processor._infer_frequency("D") == 365
    assert processor._infer_frequency("W") == 52
    assert processor._infer_frequency("M") == 12
    assert processor._infer_frequency("Q") == 4
    assert processor._infer_frequency("A") == 1
