# Standard Libraries
import numpy as np  # Numerical operations
import pandas as pd  # Data handling and processing
from datetime import datetime  # Handling date and time-related operations

# Visualization
import matplotlib.pyplot as plt  # Plotting and visualization

# Numerical Computation and Linear Algebra
from scipy.linalg import toeplitz, solve, inv, pinv  # Linear algebra tools for matrix operations
from scipy.optimize import minimize, minimize_scalar  # Optimization functions for parameter estimation

import warnings

class TemporalDisaggregation:
    """
    Class for temporal disaggregation of time series data using various statistical methods.
    """

    def __init__(self, conversion="sum", min_rho_boundarie=-0.9, max_rho_boundarie=0.99, apply_adjustment = False):
        """
        Initializes the TemporalDisaggregation class with parameters for disaggregation.

        Parameters:
            conversion (str): Specifies the type of aggregation method to ensure consistency during disaggregation.
                             Options include:
                                - "sum": Ensures that the sum of the disaggregated values matches the low-frequency series.
                                - "average": Ensures the average value remains consistent.
                                - "first": Preserves the first observed value in each aggregated period.
                                - "last": Maintains the last observed value in each aggregated period.

            min_rho_boundarie (float): The minimum allowed value for the autoregressive parameter (rho).
                                       This is used to constrain the estimation process to avoid instability.

            max_rho_boundarie (float): The maximum allowed value for the autoregressive parameter (rho).
                                       It prevents the estimation from diverging or producing unreliable results.
            
            apply_adjustment (bool): The bool value that reflects whether the series must be corrected or not.
                                       Negative values must be transformed.

        Attributes:
            self.conversion (str): Stores the specified conversion method for future computations.
            self.min_rho_boundarie (float): Lower bound for rho to ensure a stable disaggregation process.
            self.max_rho_boundarie (float): Upper bound for rho to prevent extreme values.
            self.apply_adjustment (bool): Boolean for negative values adjustment
        """

        # Store the chosen conversion method for disaggregation
        self.conversion = conversion  

        # Set the lower boundary for the autoregressive parameter (rho)
        self.min_rho_boundarie = min_rho_boundarie  

        # Set the upper boundary for the autoregressive parameter (rho)
        self.max_rho_boundarie = max_rho_boundarie 

        # Set the negative values adjustment
        self.apply_adjustment = apply_adjustment


    def build_conversion_matrix(self, df):
        """
        Constructs a conversion matrix to map high-frequency data to low-frequency data.

        This matrix ensures that the disaggregated series maintains consistency with the 
        specified aggregation method.

        Parameters:
            df (pd.DataFrame): A DataFrame containing time series data with "Index" and "Grain" columns.

        Returns:
            np.ndarray: Conversion matrix for temporal disaggregation.
        """

        def get_conversion_vector(size, conversion):
            """
            Generates a conversion vector based on the specified aggregation method.

            Parameters:
                size (int): The number of high-frequency observations corresponding to a single low-frequency period.
                conversion (str): The method of aggregation ('sum', 'average', 'first', 'last').

            Returns:
                np.ndarray: A vector that defines how high-frequency data should be aggregated.
            """
            if conversion == "sum":
                return np.ones(size)  # Assigns equal weight to all values to preserve the sum.
            elif conversion == "average":
                return np.ones(size) / size  # Distributes weights equally to maintain the average.
            elif conversion == "first":
                vec = np.zeros(size)
                vec[0] = 1  # Assigns weight only to the first observation.
                return vec
            elif conversion == "last":
                vec = np.zeros(size)
                vec[-1] = 1  # Assigns weight only to the last observation.
                return vec
            raise ValueError("Invalid method in conversion.")  # Ensures an error is raised for unsupported methods.

        # Extract unique (index, grain) combinations, ensuring order consistency
        unique_combinations = df[["Index", "Grain"]].drop_duplicates().sort_values(["Index", "Grain"])

        # Get unique low-frequency index values
        unique_indexes = unique_combinations["Index"].unique()
        n_l = len(unique_indexes)  # Number of unique low-frequency periods

        # Initialize an empty conversion matrix with dimensions (low-frequency periods x total observations)
        C = np.zeros((n_l, len(df)))

        # Populate the conversion matrix by iterating through unique low-frequency indices
        for i, idx in enumerate(unique_indexes):
            mask = (df["Index"] == idx).values  # Boolean mask for high-frequency observations corresponding to idx
            num_valid = np.sum(mask)  # Count the number of high-frequency observations in the current period

            # Assign appropriate conversion weights using the selected aggregation method
            C[i, mask] = get_conversion_vector(num_valid, self.conversion)

        return C  # Returns the constructed conversion matrix

    def denton_estimation(self, y_l, X, C, h=1):
        """
        Performs Denton temporal disaggregation.

        This method minimizes distortions by preserving the movement of the 
        high-frequency indicator while ensuring consistency with the low-frequency data.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.
            h (int, optional): Degree of differencing (0 for levels, 1 for first differences, etc.).

        Returns:
            np.ndarray: The estimated high-frequency series.
        """

        try:
            n = len(X)  # Number of high-frequency observations

            # Preprocess inputs to ensure proper formatting and dimensions
            y_l, X, C = self.preprocess_inputs(y_l, X, C)

            # Construct the differencing matrix (D) to compute differences in time series
            D = np.eye(n) - np.diag(np.ones(n - 1), -1)  # First-order difference matrix (D)

            # Apply differencing according to the specified degree (h)
            # If h = 0, no differencing is applied (identity matrix is used)
            D_h = np.linalg.matrix_power(D, h) if h > 0 else np.eye(n)

            # Compute the inverse covariance matrix (Σ_D) using the pseudoinverse
            # This helps in controlling the smoothness of the high-frequency series
            Sigma_D = pinv(D_h.T @ D_h)

            # Compute the Denton adjustment matrix (D_matrix) 
            # This maps residual adjustments from low-frequency to high-frequency
            D_matrix = Sigma_D @ C.T @ pinv(C @ Sigma_D @ C.T)

            # Compute residuals (discrepancies between actual low-frequency values and aggregated high-frequency data)
            u_l = y_l - C @ X

            # Adjust the high-frequency series using the computed transformation matrix
            return X + D_matrix @ u_l

        except:
            print(f"Error in Denton estimation")
            return None  # Return None in case of an error


    def chow_lin_estimation(self, y_l, X, C, rho=0.5):
        """
        Performs Chow-Lin temporal disaggregation.

        This method estimates high-frequency values based on a regression approach
        with an autoregressive process.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.
            rho (float, optional): Autoregressive parameter for residuals.

        Returns:
            np.ndarray: The estimated high-frequency series.
        """
        try:
            n = len(X)  # Number of high-frequency observations

            # Preprocess inputs to ensure proper formatting and dimensions
            y_l, X, C = self.preprocess_inputs(y_l, X, C)

            # Ensure the autoregressive parameter rho is within the allowed boundaries
            rho = np.clip(rho, self.min_rho_boundarie, self.max_rho_boundarie)

            # Construct the covariance matrix (Σ_CL) for the autoregressive process
            # This models the dependency structure of the high-frequency residuals
            Sigma_CL = (1 / (1 - rho**2)) * toeplitz((rho ** np.arange(n)).ravel())

            # Compute the variance-covariance matrix of the aggregated series
            Q = C @ Sigma_CL @ C.T  # Q = C * Σ_CL * C'

            # Compute the pseudo-inverse of Q to handle potential singularity issues
            inv_Q = pinv(Q)

            # Estimate the regression coefficients (β) using Generalized Least Squares (GLS)
            # β = (X' C' Q^-1 C X)^-1 * (X' C' Q^-1 y_l)
            beta = solve(X.T @ C.T @ inv_Q @ C @ X, X.T @ C.T @ inv_Q @ y_l).reshape(-1, 1)

            # Reshape X to ensure matrix compatibility
            X = X.reshape(-1, 1)

            # Compute the preliminary high-frequency estimate (p = X * β)
            p = X @ beta

            # Compute the Denton-like distribution matrix (D) that adjusts for residuals
            # D = Σ_CL * C' * Q^-1
            D = Sigma_CL @ C.T @ inv_Q

            # Compute the low-frequency residuals (u_l = y_l - C * p)
            u_l = y_l.reshape(-1, 1) - C @ p

            # Final high-frequency estimate by adjusting the preliminary estimate with residuals
            return p + D @ u_l

        except:
            print(f"Error in Chow Lin estimation")
            return None  # Return None in case of an error


    def litterman_estimation(self, y_l, X, C, rho=0.5):
        """
        Implements the Litterman method for temporal disaggregation.

        This approach extends the Chow-Lin method by incorporating a random-walk structure 
        in the residuals, allowing for better handling of non-stationary series.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.
            rho (float, optional): Autoregressive parameter.

        Returns:
            np.ndarray: The estimated high-frequency series.
        """
        try:
            n = len(X)  # Number of high-frequency observations

            # Preprocess inputs to ensure proper formatting and dimensions
            y_l, X, C = self.preprocess_inputs(y_l, X, C)

            # Ensure the autoregressive parameter rho is within the allowed range
            rho = np.clip(rho, self.min_rho_boundarie, self.max_rho_boundarie)

            # Construct the Litterman transformation matrix (H)
            # This incorporates the random-walk structure into the residuals
            H = np.eye(n) - np.diag(np.ones(n - 1), -1) * rho

            # Compute the inverse covariance matrix (Σ_L), ensuring numerical stability using pinv()
            # Σ_L = (H' H)^-1
            Sigma_L = pinv(H.T @ H)

            # Compute the variance-covariance matrix for the aggregated series
            Q = C @ Sigma_L @ C.T  # Q = C * Σ_L * C'

            # Compute the pseudo-inverse of Q to handle singular matrices
            inv_Q = pinv(Q)

            # Estimate the regression coefficients (β) using Generalized Least Squares (GLS)
            # β = (X' C' Q^-1 C X)^-1 * (X' C' Q^-1 y_l)
            beta = solve(X.T @ C.T @ inv_Q @ C @ X, X.T @ C.T @ inv_Q @ y_l).reshape(-1, 1)

            # Reshape X to ensure matrix compatibility
            X = X.reshape(-1, 1)

            # Compute the preliminary high-frequency estimate (p = X * β)
            p = X @ beta

            # Compute the adjustment matrix (D) to refine the high-frequency series
            # D = Σ_L * C' * Q^-1
            D = Sigma_L @ C.T @ inv_Q

            # Compute the low-frequency residuals (u_l = y_l - C * p)
            u_l = y_l.reshape(-1, 1) - C @ p

            # Final high-frequency estimate by adjusting the preliminary estimate with residuals
            return p + D @ u_l

        except:
            print(f"Error in Litterman estimation")
            return None  # Return None in case of an error


    def fernandez_estimation(self, y_l, X, C):
        """
        Uses the Fernandez method for temporal disaggregation.

        This method is a special case of the Litterman approach where 
        the autoregressive parameter is set to zero, modeling residuals 
        as a simple random walk.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.

        Returns:
            np.ndarray: The estimated high-frequency series.
        """
        try:
            n = len(X)  # Number of high-frequency observations

            # Construct the first-difference operator matrix (Δ)
            # Δ transforms the series into first differences, enforcing smoothness
            Delta = np.eye(n) - np.diag(np.ones(n - 1), -1)

            # Compute the covariance matrix (Σ_F) for a random walk process
            # Σ_F = (Δ' Δ)^-1 ensures residuals follow a simple random walk
            Sigma_F = np.linalg.inv(Delta.T @ Delta)

            # Compute the variance-covariance matrix for the aggregated series
            Q = C @ Sigma_F @ C.T  # Q = C * Σ_F * C'

            # Compute the inverse of Q to ensure numerical stability
            inv_Q = np.linalg.inv(Q)

            # Estimate the regression coefficients (β) using Generalized Least Squares (GLS)
            # β = (X' C' Q^-1 C X)^-1 * (X' C' Q^-1 y_l)
            beta = solve(X.T @ C.T @ inv_Q @ C @ X, X.T @ C.T @ inv_Q @ y_l).reshape(-1, 1)

            # Compute the preliminary high-frequency estimate (p = X * β)
            p = X.reshape(-1, 1) @ beta

            # Compute the adjustment matrix (D) to refine the high-frequency series
            # D = Σ_F * C' * Q^-1
            D = Sigma_F @ C.T @ inv_Q

            # Compute the low-frequency residuals (u_l = y_l - C * p)
            u_l = y_l.reshape(-1, 1) - C @ p

            # Final high-frequency estimate by adjusting the preliminary estimate with residuals
            return (p + D @ u_l).flatten()

        except:
            print(f"Error in Fernandez estimation")
            return None  # Return None in case of an error


    def ols_estimation(self, y_l, X, C):
        """
        Applies Ordinary Least Squares (OLS) regression for temporal disaggregation.

        This method assumes a simple linear relationship between the low-frequency 
        data and the high-frequency indicators without considering autocorrelation.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.

        Returns:
            np.ndarray: The estimated high-frequency series.
        """
        try:
            # Ensure y_l and X are treated as 2D column vectors
            # Preprocess inputs to ensure proper formatting and dimensions
            y_l, X, C = self.preprocess_inputs(y_l, X, C)

            # Aggregate the high-frequency indicator using the conversion matrix C
            X_l = np.atleast_2d(C @ X)  # X_l represents the aggregated high-frequency data

            # Compute the OLS regression coefficients (β) using the pseudo-inverse
            # β = (X_l' X_l)^-1 * X_l' y_l
            beta = pinv(X_l.T @ X_l) @ X_l.T @ y_l

            # Estimate the high-frequency values (ŷ = X * β)
            y_hat = X @ beta

            # Flatten the output to return a 1D array
            return y_hat.flatten()

        except:
            print(f"Error in OLS estimation")
            return None  # Return None in case of an error
       
        
    def fast_estimation(self, y_l, X, C):
        """
        Provides a fast approximation of Chow-Lin estimation.

        This method uses a fixed high autoregressive parameter and is computationally 
        efficient, closely replicating Denton-Cholette smoothing.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.

        Returns:
            np.ndarray: The estimated high-frequency series.
        """
        try:
            rho = 0.9  # Fixed high autoregressive parameter for efficient computation
            n = len(X)  # Number of high-frequency observations

            # Ensure y_l and X are treated as column vectors
            # Preprocess inputs to ensure proper formatting and dimensions
            y_l, X, C = self.preprocess_inputs(y_l, X, C)

            # Construct the transformation matrix (H)
            # This matrix incorporates a high degree of autoregression (ρ = 0.9)
            H = np.eye(n) - np.diag(np.ones(n - 1), -1) * rho

            # Compute the covariance matrix (Σ_F) for the process
            # Σ_F = (H' H)^-1 ensures smooth transition in the estimated series
            Sigma_F = pinv(H.T @ H)

            # Compute the variance-covariance matrix for the aggregated series
            Q = C @ Sigma_F @ C.T  # Q = C * Σ_F * C'

            # Compute the pseudo-inverse of Q to ensure numerical stability
            inv_Q = pinv(Q)

            # Estimate the regression coefficients (β) using Generalized Least Squares (GLS)
            # β = (X' C' Q^-1 C X)^-1 * (X' C' Q^-1 y_l)
            beta = solve(X.T @ C.T @ inv_Q @ C @ X, X.T @ C.T @ inv_Q @ y_l)

            # Compute the preliminary high-frequency estimate (p = X * β)
            p = X @ beta

            # Compute the adjustment matrix (D) to refine the high-frequency series
            # D = Σ_F * C' * Q^-1
            D = Sigma_F @ C.T @ inv_Q

            # Compute the low-frequency residuals (u_l = y_l - C * p)
            u_l = y_l - C @ p

            # Final high-frequency estimate by adjusting the preliminary estimate with residuals
            y_hat = p + D @ u_l

            # Flatten the output to return a 1D array
            return y_hat.flatten()

        except:
            print(f"Error in Fast estimation")
            return None  # Return None in case of an error


    def power_matrix_calculation(self, n):
        """
        Computes a power matrix used in autoregressive modeling.

        This matrix captures dependencies between different time periods 
        to model the persistence of the series.

        Parameters:
            n (int): Number of time periods.

        Returns:
            np.ndarray: Power matrix for autoregressive modeling.
        """
        # Generate a matrix where each entry (i, j) represents |i - j|
        # This encodes the absolute distance between time periods
        # and is useful in modeling autoregressive dependencies.
        return np.abs(np.subtract.outer(np.arange(n), np.arange(n)))


    def q_calculation(self, rho, pm):
        """
        Computes the covariance matrix for an autoregressive process.

        This matrix is used in regression-based disaggregation methods 
        to model the correlation between observations.

        Parameters:
            rho (float): Autoregressive parameter.
            pm (np.ndarray): Power matrix representing time dependencies.

        Returns:
            np.ndarray: Covariance matrix for the autoregressive process.
        """
        epsilon = 1e-6  # Small constant to prevent division by zero or instability

        # Ensure rho is within the valid range to maintain numerical stability
        rho = np.clip(rho, self.min_rho_boundarie, self.max_rho_boundarie)

        # Compute the scaling factor for the covariance matrix
        # This ensures proper normalization to prevent over-scaling of the model
        factor = 1 / (1 - rho**2 + epsilon)

        # Compute the covariance matrix using the power matrix (pm)
        # Each entry represents rho raised to the power of the absolute difference in time steps
        Q = factor * (rho ** pm)

        return Q

        
    def q_lit_calculation(self, X, rho=0):
        """
        Computes the pseudo-variance-covariance matrix for the Litterman method.

        This matrix incorporates an autoregressive structure if specified.

        Parameters:
            X (np.ndarray): High-frequency indicator series.
            rho (float, optional): Autoregressive parameter. Defaults to 0 (no autoregression).

        Returns:
            np.ndarray: Pseudo-variance-covariance matrix.
        """
        n = X.shape[0]  # Number of high-frequency observations
        epsilon = 1e-8  # Small constant to improve numerical stability

        # Construct the transformation matrix (H) incorporating the autoregressive parameter (ρ)
        # H introduces the autoregressive component in the variance structure
        H = np.eye(n) - np.diag(np.ones(n - 1), -1) * rho

        # Construct the first-difference operator matrix (D)
        # D applies a first-difference transformation, ensuring smoothness in estimates
        D = np.eye(n) - np.diag(np.ones(n - 1), -1)

        # Compute the pseudo-variance-covariance matrix (Q_Lit)
        # This matrix captures dependencies in the autoregressive process
        Q_Lit = D.T @ H.T @ H @ D

        try:
            # Compute the inverse of Q_Lit with regularization (adds ε * I to avoid singularity)
            Q_Lit_inv = np.linalg.inv(Q_Lit + np.eye(n) * epsilon)
        except np.linalg.LinAlgError:
            # If the matrix is singular, use the Moore-Penrose pseudo-inverse
            Q_Lit_inv = np.linalg.pinv(Q_Lit)

        return Q_Lit_inv


    def rho_optimization(self, y_l, X, C, method="maxlog"):
        """
        Finds the optimal autoregressive parameter (rho).

        This is done by maximizing the likelihood function or minimizing 
        the residual sum of squares, which is crucial for Chow-Lin and Litterman methods.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.
            method (str, optional): Optimization criterion. Options: "maxlog" (maximize log-likelihood) 
                                    or "minrss" (minimize residual sum of squares).

        Returns:
            float: Optimal autoregressive parameter rho.
        """
        # Compute the aggregated high-frequency series using the conversion matrix
        X_l = np.atleast_2d(C @ X)

        # Compute the power matrix, which captures time dependencies
        pm = self.power_matrix_calculation(X.shape[0])

        # Ensure input dimensions are properly formatted before optimization
        y_l, X, C = self.preprocess_inputs(y_l, X, C)

        def objective(rho):
            """
            Defines the optimization objective function for rho.

            The function either maximizes the log-likelihood (maxlog) 
            or minimizes the residual sum of squares (minrss).
            """
            # Ensure rho is within the specified boundaries
            if not (self.min_rho_boundarie < rho < self.max_rho_boundarie):
                return np.inf  # Return infinity to prevent invalid rho values

            # Compute the covariance matrix Q for the autoregressive process
            Q = self.q_calculation(rho, pm)

            # Compute the variance-covariance matrix for the aggregated series
            vcov = C @ Q @ C.T

            # Compute the inverse of vcov, adding a small regularization term for stability
            inv_vcov = pinv(vcov + np.eye(vcov.shape[0]) * 1e-8)

            # Ensure that the dimensions match for matrix operations
            if X_l.shape[0] != inv_vcov.shape[0]:
                return np.inf  # Return infinity to prevent errors

            # Compute (X' C' inv_vcov C X), ensuring it's a square matrix
            XTX = X_l.T @ inv_vcov @ X_l
            if XTX.shape[0] != XTX.shape[1]:
                return np.inf  # Return infinity if matrix inversion is not feasible

            # Estimate regression coefficients (β) using the Generalized Least Squares (GLS) formula
            beta = pinv(XTX) @ X_l.T @ inv_vcov @ y_l

            # Compute residuals (difference between observed and estimated values)
            u_l = y_l - X_l @ beta

            # Choose the optimization method: log-likelihood maximization or residual minimization
            if method == "maxlog":
                # Maximize log-likelihood: minimize its negative
                return -(-0.5 * (np.log(np.abs(np.linalg.det(vcov)) + 1e-8) + u_l.T @ inv_vcov @ u_l))
            elif method == "minrss":
                # Minimize the residual sum of squares
                return u_l.T @ inv_vcov @ u_l
            else:
                raise ValueError("Invalid method for rho calculation")

        # Perform bounded scalar optimization within the defined range of rho
        opt_result = minimize_scalar(objective, bounds=(self.min_rho_boundarie, self.max_rho_boundarie), method="bounded")

        # Return the optimal rho value
        return opt_result.x

    
    def litterman_opt_estimation(self, y_l, X, C):
        """
        Implements the optimized Litterman method.

        This method estimates the best autoregressive parameter before performing 
        disaggregation, refining the standard Litterman approach for better accuracy.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.

        Returns:
            np.ndarray: The estimated high-frequency series.
        """
        try:
            # Preprocess inputs to ensure proper formatting and dimensions
            y_l, X, C = self.preprocess_inputs(y_l, X, C)

            # Validate that the number of columns in C matches the number of rows in X
            if C.shape[1] != X.shape[0]:
                return None  # Return None if dimensions are incompatible

            # Compute the aggregated high-frequency series using the conversion matrix
            X_l = np.atleast_2d(C @ X)

            # Optimize the autoregressive parameter (rho) by minimizing residual sum of squares (minrss)
            rho_opt = self.rho_optimization(y_l, X, C, method="minrss")

            # Compute the variance-covariance matrix (Q_Lit) for the optimized Litterman method
            Q_Lit = self.q_lit_calculation(X, rho_opt)

            # Compute the variance-covariance matrix for the aggregated series
            vcov = C @ Q_Lit @ C.T

            # Compute the pseudo-inverse of vcov, adding a small regularization term for numerical stability
            inv_vcov = pinv(vcov + np.eye(vcov.shape[0]) * 1e-8)

            # Validate dimensions to prevent computational errors
            if X_l.shape[0] != inv_vcov.shape[0]:
                return None  # Return None if dimensions mismatch

            # Compute (X' C' inv_vcov C X), ensuring it is a square matrix before inversion
            XTX = X_l.T @ inv_vcov @ X_l
            if XTX.shape[0] != XTX.shape[1]:
                return None  # Return None if matrix is not square

            # Estimate regression coefficients (β) using Generalized Least Squares (GLS)
            # β = (X' C' Q^-1 C X)^-1 * (X' C' Q^-1 y_l)
            beta = pinv(XTX) @ X_l.T @ inv_vcov @ y_l

            # Compute the preliminary high-frequency estimate (p = X * β)
            p = X @ beta

            # Compute the adjustment matrix (D) to refine the high-frequency series
            # D = Q_Lit * C' * Q^-1
            D = Q_Lit @ C.T @ inv_vcov

            # Compute the low-frequency residuals (u_l = y_l - C * p)
            u_l = y_l - C @ p

            # Final high-frequency estimate by adjusting the preliminary estimate with residuals
            y_hat = p + D @ u_l

            # Flatten the output to return a 1D array
            return y_hat.flatten()
        except:
            print("Error in optimized Litterman")


    def chow_lin_opt_estimation(self, y_l, X, C):
        """
        Implements the optimized Chow-Lin method.

        This method estimates the best autoregressive parameter before performing 
        disaggregation, improving accuracy by tuning the autoregressive component.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.

        Returns:
            np.ndarray: The estimated high-frequency series.
        """
        try:
            # Preprocess inputs to ensure proper formatting and dimensions
            y_l, X, C = self.preprocess_inputs(y_l, X, C)

            # Validate that the number of columns in C matches the number of rows in X
            if C.shape[1] != X.shape[0]:
                return None  # Return None if dimensions are incompatible

            # Compute the aggregated high-frequency series using the conversion matrix
            X_l = np.atleast_2d(C @ X)

            # Optimize the autoregressive parameter (rho) by maximizing the log-likelihood (maxlog)
            rho_opt = self.rho_optimization(y_l, X, C, method="maxlog")

            # Number of high-frequency observations
            n = X.shape[0]

            # Construct the autoregressive covariance matrix (Σ_CL)
            # This models the dependency structure of the high-frequency residuals
            Sigma_CL = (1 / (1 - rho_opt**2)) * toeplitz(np.ravel(rho_opt ** np.arange(n)))

            # Compute the variance-covariance matrix for the aggregated series
            Q = C @ Sigma_CL @ C.T

            # Ensure Q is a square matrix before inversion
            if Q.shape[0] != Q.shape[1]:
                return None  # Return None if dimensions are incorrect

            # Compute the pseudo-inverse of Q, adding a small regularization term for numerical stability
            inv_Q = pinv(Q + np.eye(Q.shape[0]) * 1e-8)

            # Validate dimensions to prevent computational errors
            if X_l.shape[0] != inv_Q.shape[0]:
                return None  # Return None if dimensions mismatch

            # Compute (X' C' inv_Q C X), ensuring it is a square matrix before inversion
            XTX = X_l.T @ inv_Q @ X_l
            if XTX.shape[0] != XTX.shape[1]:
                return None  # Return None if matrix is not square

            # Estimate regression coefficients (β) using Generalized Least Squares (GLS)
            # β = (X' C' Q^-1 C X)^-1 * (X' C' Q^-1 y_l)
            beta = pinv(XTX) @ X_l.T @ inv_Q @ y_l

            # Compute the preliminary high-frequency estimate (p = X * β)
            p = X @ beta

            # Compute the adjustment matrix (D) to refine the high-frequency series
            # D = Σ_CL * C' * Q^-1
            D = Sigma_CL @ C.T @ inv_Q

            # Compute the low-frequency residuals (u_l = y_l - C * p)
            u_l = y_l - C @ p

            # Final high-frequency estimate by adjusting the preliminary estimate with residuals
            y_hat = p + D @ u_l

            # Flatten the output to return a 1D array
            return y_hat.flatten()
        except:
            print("Error in optimized Litterman")

    
    def preprocess_inputs(self, y_l, X, C):
        """
        Preprocesses inputs for temporal disaggregation methods.

        This function ensures the correct shape and format of the input data.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.

        Returns:
            tuple: Processed (y_l, X, C) as numpy arrays with the correct dimensions.
        """
        # Ensure y_l and X are treated as 2D column vectors
        y_l = np.atleast_2d(y_l).reshape(-1, 1)
        X = np.atleast_2d(X).reshape(-1, 1)

        # Validate that the number of rows in C matches the number of observations in y_l
        if C.shape[0] != y_l.shape[0]:
            raise ValueError(f"Shape mismatch: C.shape[0] ({C.shape[0]}) != y_l.shape[0] ({y_l.shape[0]})")

        # Validate that the number of columns in C matches the number of rows in X
        if C.shape[1] != X.shape[0]:
            raise ValueError(f"Shape mismatch: C.shape[1] ({C.shape[1]}) != X.shape[0] ({X.shape[0]})")

        # Return the processed inputs with corrected dimensions
        return y_l, X, C
    

    def chow_lin_minrss_ecotrim(self, y_l, X, C, rho=0.75):
        """
        Implements the Chow-Lin method with RSS minimization (Ecotrim).

        This method estimates high-frequency values by minimizing the 
        residual sum of squares (RSS) while preserving correlation structure.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.
            rho (float): Autoregressive parameter.

        Returns:
            np.ndarray: Estimated high-frequency series.
        """
        # Preprocess inputs to ensure proper formatting and dimensions
        y_l, X, C = self.preprocess_inputs(y_l, X, C)
                                               
        n = X.shape[0]  # Number of high-frequency observations

        # Ensure rho is within valid boundaries
        rho = np.clip(rho, self.min_rho_boundarie, self.max_rho_boundarie)

        # Compute the correlation matrix R (instead of covariance matrix)
        # Toeplitz structure models time dependency with autoregressive correlation
        R = toeplitz(rho ** np.arange(n))

        # Compute the aggregated variance-covariance matrix
        Q = C @ R @ C.T  # Q = C * R * C'

        # Compute the pseudo-inverse for numerical stability
        inv_Q = pinv(Q + np.eye(Q.shape[0]) * 1e-8)

        # Generalized Least Squares (GLS) estimation of beta coefficients
        beta = pinv(X.T @ C.T @ inv_Q @ C @ X) @ X.T @ C.T @ inv_Q @ y_l

        # Compute the preliminary high-frequency estimate (p = X * β)
        p = X @ beta

        # Compute the adjustment matrix (D) to refine the high-frequency series
        # D = R * C' * Q^-1
        D = R @ C.T @ inv_Q

        # Compute the low-frequency residuals (u_l = y_l - C * p)
        u_l = y_l - C @ p

        # Final high-frequency estimate by adjusting the preliminary estimate with residuals
        return p + D @ u_l
    
    def chow_lin_minrss_quilis(self, y_l, X, C, rho=0.15):
        """
        Implements the Chow-Lin method with RSS minimization (Quilis approach).

        This method estimates high-frequency values by minimizing the 
        residual sum of squares (RSS) while scaling the correlation matrix.

        Parameters:
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.
            rho (float): Autoregressive parameter.

        Returns:
            np.ndarray: Estimated high-frequency series.
        """
        # Preprocess inputs to ensure proper formatting and dimensions
        y_l, X, C = self.preprocess_inputs(y_l, X, C)

        n = X.shape[0]  # Number of high-frequency observations

        # Ensure rho is within valid boundaries
        rho = np.clip(rho, self.min_rho_boundarie, self.max_rho_boundarie)

        # Compute the scaled correlation matrix R
        # Unlike Ecotrim, Quilis scales the matrix with (1 / (1 - rho^2))
        epsilon = 1e-6 
        R = (1 / (1 - (rho + epsilon)**2)) * toeplitz(rho ** np.arange(n))

        # Compute the aggregated variance-covariance matrix
        Q = C @ R @ C.T  # Q = C * R * C'

        # Compute the pseudo-inverse for numerical stability
        inv_Q = pinv(Q + np.eye(Q.shape[0]) * 1e-8)

        # Generalized Least Squares (GLS) estimation of beta coefficients
        beta = pinv(X.T @ C.T @ inv_Q @ C @ X) @ X.T @ C.T @ inv_Q @ y_l

        # Compute the preliminary high-frequency estimate (p = X * β)
        p = X @ beta

        # Compute the adjustment matrix (D) to refine the high-frequency series
        # D = R * C' * Q^-1
        D = R @ C.T @ inv_Q

        # Compute the low-frequency residuals (u_l = y_l - C * p)
        u_l = y_l - C @ p

        # Final high-frequency estimate by adjusting the preliminary estimate with residuals
        return p + D @ u_l

    def predict(self, df, method, **kwargs):
        """
        General interface for performing temporal disaggregation.

        Selects and applies the appropriate estimation method.

        Parameters:
            method (str): The disaggregation method to use.
            y_l (np.ndarray): Low-frequency time series.
            X (np.ndarray): High-frequency indicator series.
            C (np.ndarray): Conversion matrix.
            **kwargs: Additional parameters for specific methods.

        Returns:
            np.ndarray: The estimated high-frequency series.
        """
        # Dictionary of available disaggregation methods
        all_methods = {
            "ols": self.ols_estimation,
            "denton": self.denton_estimation,
            "chow-lin": self.chow_lin_estimation,
            "litterman": self.litterman_estimation,
            "fernandez": self.fernandez_estimation,
            "fast": self.fast_estimation,
            "chow-lin-opt": self.chow_lin_opt_estimation,
            "litterman-opt": self.litterman_opt_estimation,
            "chow-lin-ecotrim": self.chow_lin_minrss_ecotrim,
            "chow-lin-quilis": self.chow_lin_minrss_quilis,
        }

        df_predicted = df.copy()

        # Build the conversion matrix
        C = self.build_conversion_matrix(df_predicted)

        # Extract low-frequency series (one observation per low-frequency period)
        y_l = df_predicted.groupby("Index")["y"].first().values

        # Extract high-frequency indicator series
        X = df_predicted["X"].values

        # Ensure the method is valid
        if method not in all_methods:
            raise ValueError(f"Method '{method}' is not supported. Available methods: {list(all_methods.keys())}")

        # Ensure input arrays are column vectors
        y_l = np.atleast_2d(y_l).reshape(-1, 1)
        X = np.atleast_2d(X).reshape(-1, 1)

        # Validate matrix dimensions before proceeding
        if C.shape[1] != X.shape[0]:
            raise ValueError(f"Shape mismatch: C.shape[1] ({C.shape[1]}) != X.shape[0] ({X.shape[0]})")
        if C.shape[0] != y_l.shape[0]:
            raise ValueError(f"Shape mismatch: C.shape[0] ({C.shape[0]}) != y_l.shape[0] ({y_l.shape[0]})")

        # Define the list of valid keyword arguments that methods can accept
        valid_args = ["h", "rho", "alpha", "weights"]

        # Filter only the valid arguments to pass to the method
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in valid_args}

        try:
            # Execute the selected disaggregation method and return the estimated series
            y_hat = all_methods[method](y_l, X, C, **filtered_kwargs)
    
        except:
            try:
                # Execute the selected disaggregation method (first backup)
                warnings.warn("Error in disaggregation. FAST used as default method", UserWarning)
                y_hat = all_methods["fast"](y_l, X, C, **filtered_kwargs)
             
            except:
                # Execute the selected disaggregation method (second backup)
                warnings.warn("Error in disaggregation. OLS used as default method", UserWarning)
                y_hat = all_methods["ols"](y_l, X, C, **filtered_kwargs)

        df_predicted["y_hat"] = y_hat

        if self.apply_adjustment:
            df_predicted = self.adjust_negative_values(df_predicted)

        return df_predicted
    

    def adjust_negative_values(self, df):
        """
        Adjusts negative values in the predicted high-frequency series while preserving aggregation constraints.

        Parameters:
            df (pd.DataFrame): The dataframe containing the following columns:
                            ['Index', 'Grain', 'X', 'y', 'y_hat'].

        Returns:
            pd.DataFrame: The adjusted dataframe with non-negative values in 'y_hat'.
        """
        df_adjusted = df.copy()
        df_adjusted["y_hat_adj"] = df_adjusted["y_hat"].copy()
        
        # Identificar los índices con valores negativos en y_hat
        negative_indexes = df_adjusted[df_adjusted["y_hat"] < 0]["Index"].unique()
        
        for index in negative_indexes:
            group = df_adjusted[df_adjusted["Index"] == index].reset_index(drop=True)
            y_hat = group["y_hat"].values

            # Si no hay valores negativos, continuar con el siguiente grupo
            if (y_hat >= 0).all():
                continue
            
            if self.conversion in ["sum", "average"]:
                # Sumar todas las diferencias negativas para crear un factor de ajuste
                negative_sum = np.abs(y_hat[y_hat < 0].sum())
                
                # Obtener valores positivos y su suma
                positive_values = y_hat[y_hat > 0]
                positive_sum = positive_values.sum()

                if positive_sum > 0:
                    # Calcular las participaciones relativas de los valores positivos
                    weights = positive_values / positive_sum

                    # Aplicar ajuste proporcionalmente
                    y_hat[y_hat > 0] -= negative_sum * weights
                    
                    # Ajustar los valores negativos a un pequeño valor positivo si se requiere
                    y_hat[y_hat < 0] = 0

                else:
                    # Si no hay valores positivos, distribuir de manera uniforme
                    y_hat[:] = negative_sum / len(y_hat)

            elif self.conversion == "first":
                # Mantener el primer valor fijo
                first_value = y_hat[0]
                remaining_values = y_hat[1:]

                if remaining_values.sum() < 0:
                    remaining_values[:] = 0
                else:
                    negative_sum = np.abs(remaining_values[remaining_values < 0].sum())
                    positive_values = remaining_values[remaining_values > 0]
                    positive_sum = positive_values.sum()

                    if positive_sum > 0:
                        weights = positive_values / positive_sum
                        remaining_values[remaining_values > 0] -= negative_sum * weights
                    
                    remaining_values[remaining_values < 0] = 0
                
                y_hat[1:] = remaining_values
                y_hat[0] = first_value

            elif self.conversion == "last":
                # Mantener el último valor fijo
                last_value = y_hat[-1]
                remaining_values = y_hat[:-1]

                if remaining_values.sum() < 0:
                    remaining_values[:] = 0
                else:
                    negative_sum = np.abs(remaining_values[remaining_values < 0].sum())
                    positive_values = remaining_values[remaining_values > 0]
                    positive_sum = positive_values.sum()

                    if positive_sum > 0:
                        weights = positive_values / positive_sum
                        remaining_values[remaining_values > 0] -= negative_sum * weights
                    
                    remaining_values[remaining_values < 0] = 0
                
                y_hat[:-1] = remaining_values
                y_hat[-1] = last_value
            
            # Reasignar los valores ajustados
            df_adjusted.loc[df_adjusted["Index"] == index, "y_hat_adj"] = y_hat

        return df_adjusted
