import pandas as pd
import numpy as np

class TimeSeriesProcessor:
    """
    Class to process, interpolate, and merge time series of different frequencies.
    """

    def __init__(self, ts_high_freq, start_date_hf, end_date_hf, freq_hf,
                 ts_low_freq, start_date_lf, end_date_lf, freq_lf, interp_method='nearest'):
        """
        Initializes the class with high- and low-frequency time series.

        :param ts_high_freq: High-frequency time series (array or list).
        :param start_date_hf: Start date of the high-frequency series (str or datetime).
        :param end_date_hf: End date of the high-frequency series (str or datetime).
        :param freq_hf: Frequency of the high-frequency series (e.g., 'D' for daily, 'H' for hourly).
        :param ts_low_freq: Low-frequency time series (array or list).
        :param start_date_lf: Start date of the low-frequency series (str or datetime).
        :param end_date_lf: End date of the low-frequency series (str or datetime).
        :param freq_lf: Frequency of the low-frequency series (e.g., 'M' for monthly, 'Q' for quarterly).
        :param interp_method: Interpolation method for missing values (default is 'nearest').
        """
        self.freq_hf = freq_hf  # Stores the frequency of the high-frequency series
        self.freq_lf = freq_lf  # Stores the frequency of the low-frequency series
        self.interp_method = interp_method  # Defines the interpolation method

        # Create DataFrames for time series using a helper method
        self.ts_high_freq = self._create_time_series(ts_high_freq, start_date_hf, end_date_hf, freq_hf, "High_freq")
        self.ts_low_freq = self._create_time_series(ts_low_freq, start_date_lf, end_date_lf, freq_lf, "Low_freq")

        # Ensure both time series were successfully created
        if self.ts_high_freq is None or self.ts_low_freq is None:
            raise ValueError("Error in creating time series.")

    def _create_time_series(self, values, start_date, end_date, freq, col_name):
        """
        Creates a pandas DataFrame with a time series.

        :param values: List of numerical values.
        :param start_date: Start date of the time series.
        :param end_date: End date of the time series.
        :param freq: Frequency of the time series.
        :param col_name: Name of the values column.
        :return: Pandas DataFrame with 'Date' and the time series.
        """
        try:
            # Generate date range based on start, end, and frequency
            dates = pd.date_range(start=start_date, end=end_date, freq=freq)

            # Ensure the number of generated dates matches the number of values
            if len(dates) != len(values):
                raise ValueError(f"Error: Number of values does not match generated dates for {col_name}.")

            # Create DataFrame with dates and values
            df = pd.DataFrame({'Date': dates, col_name: values})
            return df
        except Exception as e:
            print(f"Error creating time series {col_name}: {e}")
            return None

    def _interpolate_and_fill(self, series):
        """
        Applies interpolation and fills missing values.

        :param series: Pandas Series with possible NaN values.
        :return: Interpolated Series without NaN values.
        """
        try:
            # Apply interpolation using the defined method and fill missing values forward and backward
            series = series.interpolate(method=self.interp_method).ffill().bfill()
            return series
        except Exception as e:
            print(f"Error in interpolation and filling: {e}")
            return None

    def _infer_frequency(self, freq):
        """
        Infers the number of periods per year based on the series frequency.

        :param freq: Frequency of the time series (e.g., 'D', 'W', 'M', 'Q', 'A').
        :return: Number of periods per year.
        """
        # Mapping different time frequencies to their corresponding periods per year
        freq_map = {"D": 365, "W": 52, "M": 12, "Q": 4, "A": 1}
        return freq_map.get(freq[0].upper(), 1)  # Default to 1 if not found

    def _infer_start_value(self, date_index, periods_per_year):
        """
        Infers the initial value of the cyclic indicator based on the date.

        :param date_index: Date index of the time series.
        :param periods_per_year: Number of periods per year.
        :return: Initial value of the cyclic indicator.
        """
        try:
            first_date = date_index[0]  # Retrieve the first date of the series

            # Assign the starting value based on the frequency
            if periods_per_year == 365:
                return first_date.timetuple().tm_yday  # Day of the year
            elif periods_per_year == 52:
                return first_date.isocalendar()[1]  # ISO week number
            elif periods_per_year == 12:
                return first_date.month  # Month number
            elif periods_per_year == 4:
                return (first_date.month - 1) // 3 + 1  # Quarter of the year
            else:
                return 1  # Default value if none match
        except Exception as e:
            print(f"Error in _infer_start_value: {e}")
            return 1  # Return a default value in case of failure

    def _generate_indicator(self, num_obs, periods_per_year, start_value):
        """
        Generates a cyclic indicator based on the number of periods per year.

        :param num_obs: Total number of observations.
        :param periods_per_year: Expected periods per year.
        :param start_value: Initial value of the indicator.
        :return: Vector with the cyclic indicator.
        """
        try:
            # Adjust the start value to ensure it fits within the cycle
            start_value = (start_value - 1) % periods_per_year + 1

            # Create a cyclic pattern by repeating values in the expected period
            return (np.arange(num_obs) + start_value - 1) % periods_per_year + 1
        except Exception as e:
            print(f"Error in _generate_indicator: {e}")
            return np.array([])  # Return an empty array in case of failure

    def process_and_merge_series(self):
        """
        Processes and integrates high- and low-frequency time series.

        :return: Pandas DataFrame with the combined series.
        """
        # Merge high- and low-frequency series using a left join on the date
        merged_df = pd.merge(self.ts_high_freq, self.ts_low_freq, on="Date", how="left")

        # Interpolate and fill missing values in the low-frequency series
        merged_df["Low_freq"] = self._interpolate_and_fill(merged_df["Low_freq"])

        # Infer the number of periods per year based on high-frequency data
        periods_per_year = self._infer_frequency(self.freq_hf)

        # Determine the starting value of the cyclic indicator
        start_value = self._infer_start_value(merged_df["Date"], periods_per_year)

        # Generate the cyclic indicator based on inferred parameters
        merged_df["Indicator"] = self._generate_indicator(len(merged_df), periods_per_year, start_value)

        # Extract year from the date column and rename it as 'index'
        merged_df["Year"] = pd.to_numeric(merged_df["Date"].dt.year).astype(int)

        # Rename columns to match expected output format
        merged_df = merged_df.rename(columns={"Year": "Index",
                                              "High_freq": "X",
                                              "Low_freq": "y",
                                              "Indicator": "Grain"})

        # Return only the required columns
        return merged_df[['Index', 'Grain', 'X', 'y']]