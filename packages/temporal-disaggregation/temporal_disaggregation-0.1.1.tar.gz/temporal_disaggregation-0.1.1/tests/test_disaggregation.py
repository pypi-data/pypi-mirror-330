import pytest
import numpy as np
import pandas as pd
from temporal_disaggregation.disaggregation import TemporalDisaggregation

@pytest.fixture
def disaggregator():
    """Instancia un objeto TemporalDisaggregation para pruebas."""
    return TemporalDisaggregation(conversion="sum")

@pytest.fixture
def sample_data():
    """Genera datos de prueba para la desagregación temporal."""
    df = pd.DataFrame({
        "Index": np.repeat(np.arange(2000, 2010), 4),  # 10 períodos de baja frecuencia
        "Grain": np.tile(np.arange(1, 5), 10),         # 4 observaciones por período
        "X": np.random.rand(40) * 100,                # 40 valores de alta frecuencia
        "y": np.repeat(np.random.rand(10) * 1000, 4)  # 10 valores de baja frecuencia repetidos 4 veces
    })
    return df

@pytest.fixture
def sample_matrices(disaggregator, sample_data):
    """Genera las matrices requeridas para los métodos de desagregación."""
    C = disaggregator.build_conversion_matrix(sample_data)
    y_l = sample_data.groupby("Index")["y"].first().values
    X = sample_data["X"].values
    return y_l, X, C

# 📌 TEST PARA CADA MÉTODO

def test_denton_estimation(disaggregator, sample_matrices):
    """Verifica que el método Denton de desagregación no genere valores nulos."""
    y_l, X, C = sample_matrices
    result = disaggregator.denton_estimation(y_l, X, C, h=1)
    assert result is not None, "Denton estimation devolvió None"
    assert not np.isnan(result).any(), "El resultado de Denton contiene valores nulos"

def test_chow_lin_estimation(disaggregator, sample_matrices):
    """Verifica que el método Chow-Lin de desagregación funcione correctamente."""
    y_l, X, C = sample_matrices
    result = disaggregator.chow_lin_estimation(y_l, X, C, rho=0.5)
    assert result is not None, "Chow-Lin estimation devolvió None"
    assert not np.isnan(result).any(), "El resultado de Chow-Lin contiene valores nulos"

def test_litterman_estimation(disaggregator, sample_matrices):
    """Verifica que el método Litterman de desagregación funcione correctamente."""
    y_l, X, C = sample_matrices
    result = disaggregator.litterman_estimation(y_l, X, C, rho=0.5)
    assert result is not None, "Litterman estimation devolvió None"
    assert not np.isnan(result).any(), "El resultado de Litterman contiene valores nulos"

def test_fernandez_estimation(disaggregator, sample_matrices):
    """Verifica que el método Fernandez de desagregación funcione correctamente."""
    y_l, X, C = sample_matrices
    result = disaggregator.fernandez_estimation(y_l, X, C)
    assert result is not None, "Fernandez estimation devolvió None"
    assert not np.isnan(result).any(), "El resultado de Fernandez contiene valores nulos"

def test_ols_estimation(disaggregator, sample_matrices):
    """Verifica que el método OLS de desagregación funcione correctamente."""
    y_l, X, C = sample_matrices
    result = disaggregator.ols_estimation(y_l, X, C)
    assert result is not None, "OLS estimation devolvió None"
    assert not np.isnan(result).any(), "El resultado de OLS contiene valores nulos"

def test_fast_estimation(disaggregator, sample_matrices):
    """Verifica que el método Fast de desagregación funcione correctamente."""
    y_l, X, C = sample_matrices
    result = disaggregator.fast_estimation(y_l, X, C)
    assert result is not None, "Fast estimation devolvió None"
    assert not np.isnan(result).any(), "El resultado de Fast contiene valores nulos"

def test_chow_lin_opt_estimation(disaggregator, sample_matrices):
    """Verifica que el método optimizado Chow-Lin funcione correctamente."""
    y_l, X, C = sample_matrices
    result = disaggregator.chow_lin_opt_estimation(y_l, X, C)
    assert result is not None, "Chow-Lin optimizado devolvió None"
    assert not np.isnan(result).any(), "El resultado de Chow-Lin optimizado contiene valores nulos"

def test_litterman_opt_estimation(disaggregator, sample_matrices):
    """Verifica que el método optimizado Litterman funcione correctamente."""
    y_l, X, C = sample_matrices
    result = disaggregator.litterman_opt_estimation(y_l, X, C)
    assert result is not None, "Litterman optimizado devolvió None"
    assert not np.isnan(result).any(), "El resultado de Litterman optimizado contiene valores nulos"

def test_chow_lin_minrss_ecotrim(disaggregator, sample_matrices):
    """Verifica que el método Chow-Lin Ecotrim funcione correctamente."""
    y_l, X, C = sample_matrices
    result = disaggregator.chow_lin_minrss_ecotrim(y_l, X, C, rho=0.75)
    assert result is not None, "Chow-Lin Ecotrim devolvió None"
    assert not np.isnan(result).any(), "El resultado de Chow-Lin Ecotrim contiene valores nulos"

def test_chow_lin_minrss_quilis(disaggregator, sample_matrices):
    """Verifica que el método Chow-Lin Quilis funcione correctamente."""
    y_l, X, C = sample_matrices
    result = disaggregator.chow_lin_minrss_quilis(y_l, X, C, rho=0.15)
    assert result is not None, "Chow-Lin Quilis devolvió None"
    assert not np.isnan(result).any(), "El resultado de Chow-Lin Quilis contiene valores nulos"
