# Temporal Disaggregation

A **Python library** for **temporal disaggregation** of time series data using various statistical and econometric methods.

This library enables **high-frequency estimation** from low-frequency data, ensuring consistency with the original aggregated series. It includes **multiple disaggregation methods**, such as:

- **Denton Method** (Proportional/Level Difference Minimization)
- **Chow-Lin Method** (Maximum Likelihood / GLS Regression)
- **Litterman Method** (Random Walk + AR(1))
- **Fernandez Method** (Special Case of Litterman with ρ = 0)
- **Ordinary Least Squares (OLS)**
- **Fast Approximation (Denton-Cholette Alternative)**
- **Optimized Chow-Lin and Litterman Methods**
- **Chow-Lin Ecotrim / Quilis Variants**

Designed for **economic, financial, and scientific time series**, ensuring smooth interpolation while maintaining theoretical constraints.

---

## 📦 Installation

Install the package from **PyPI**:

```sh
!pip install temporal-disaggregation
```

```python
from temporal_disaggregation import TemporalDisaggregation

# Initialize the disaggregator
td = TemporalDisaggregation(conversion="sum")

# Create sample data
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "Index": np.repeat(np.arange(2000, 2010), 4),  # 10 low-frequency periods
    "Grain": np.tile(np.arange(1, 5), 10),         # 4 observations per period
    "X": np.random.rand(40) * 100,                # High-frequency data
    "y": np.repeat(np.random.rand(10) * 1000, 4)  # Low-frequency data
})

# Disaggregate using the Chow-Lin method
df_predicted = td.predict(df, method="chow-lin")

# Display results
print(df_predicted.head())
```

## 📖 Available Methods

1️⃣ Denton Method (denton_estimation)
Minimizes distortions while preserving the movement of the high-frequency indicator.

```python
df_predicted = td.predict(df, method="denton", h=1)
```

2️⃣ Chow-Lin Method (chow_lin_estimation)
A GLS-based regression method with an autoregressive (AR) structure.
```python
df_predicted = td.predict(df, method="chow-lin", rho=0.5)
```

3️⃣ Litterman Method (litterman_estimation)
Uses a random-walk structure for residuals to model non-stationary series.
```python
df_predicted = td.predict(df, method="litterman", rho=0.5)
```

4️⃣ Fernandez Method (fernandez_estimation)
A special case of Litterman where rho = 0.
```python
df_predicted = td.predict(df, method="fernandez")
```

5️⃣ Ordinary Least Squares (OLS) Method (ols_estimation)
A simple OLS regression-based disaggregation method.
```python
df_predicted = td.predict(df, method="ols")
```

6️⃣ Fast Approximation (fast_estimation)
A Denton-Cholette alternative, computationally efficient.
```python
df_predicted = td.predict(df, method="fast")
```

7️⃣ Optimized Chow-Lin & Litterman Methods
These methods automatically estimate the best autoregressive parameter (ρ).
```python
df_predicted = td.predict(df, method="chow-lin-opt")
df_predicted = td.predict(df, method="litterman-opt")
```

8️⃣ Chow-Lin Ecotrim & Quilis Variants
Alternative GLS estimation methods minimizing RSS.
```python
df_predicted = td.predict(df, method="chow-lin-ecotrim")
df_predicted = td.predict(df, method="chow-lin-quilis")
```

## ⚙️ How It Works

🔄 Conversion Matrix
The library automatically constructs a conversion matrix (C) to map high-frequency data into low-frequency equivalents.

```python
C = td.build_conversion_matrix(df)
```
## 🛠️ Customization
You can customize:

Conversion method ("sum", "average", "first", "last")
Autoregressive parameter bounds (min_rho_boundarie, max_rho_boundarie)
Negative values adjustment (apply_adjustment=True)

```python
td = TemporalDisaggregation(conversion="average", min_rho_boundarie=-0.5, max_rho_boundarie=0.95)
```

## Adjusting Negative Values

The adjust_negative_values method is designed to eliminate negative values in the predicted high-frequency series (y_hat) while maintaining aggregation consistency with the original low-frequency data.

---

## 📌 **Function Signature**
```python
apply_adjustment = False  # Enables or disables automatic negative value correction
```
