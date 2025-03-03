import pandas as pd
import numpy as np

def convert_quarter_to_date(quarter_str):
    """
    Converts a quarter string (e.g., '2023 Q1') to a pandas Timestamp.
    
    Args:
        quarter_str (str): String in the format 'YYYY QN' where YYYY is the year 
                          and N is the quarter number (1-4)
    
    Returns:
        pd.Timestamp: First day of the first month in the quarter
    
    Example:
        >>> convert_quarter_to_date('2023 Q1')
        Timestamp('2023-01-01 00:00:00')
    """
    try:
        year, quarter = quarter_str.split(' ')
        month = {'Q1': 1, 'Q2': 4, 'Q3': 7, 'Q4': 10}[quarter]  # Map quarters to their starting months
        return pd.Timestamp(year=int(year), month=month, day=1)
    except (ValueError, KeyError) as e:
        raise ValueError(f"Invalid quarter string format: {quarter_str}. Expected format: 'YYYY QN' (e.g., '2023 Q1')") from e


def convert_week_to_date(week_str):
    """
    Converts a week string in the format 'YYYY Www' to a datetime object.

    Args:
        week_str (str): A string representing the week in the format 'YYYY Www',
                        where 'YYYY' is the year and 'ww' is the week number.

    Returns:
        pd.Timestamp: A pandas Timestamp object representing the first day (Monday)
                      of the specified week.

    Example:
        >>> convert_week_to_date('2023 W10')
        Timestamp('2023-03-06 00:00:00')
    """
    try:
        year, week = week_str.split(' W')
        return pd.to_datetime(f'{year}-W{week}-1', format='%Y-W%W-%w')
    except ValueError as e:
        raise ValueError(f"Invalid week string format: {week_str}. Expected format: 'YYYY Www' (e.g., '2023 W10')") from e


def prepare_data(df, ds, y, t_type='No'):
    """
    Prepares a DataFrame for time series analysis by standardizing the date column
    and aggregating the target variable.

    Args:
        df (pd.DataFrame): Input DataFrame containing the time series data.
        ds (str): Name of the column containing the date or time information.
        y (str): Name of the column containing the target variable.
        t_type (str, optional): Type of time format in the `ds` column. Options:
                                - 'q': Quarter format (e.g., '2023 Q1')
                                - 'w': Week format (e.g., '2023 W10')
                                - 'y': Year format (e.g., '2023')
                                - 'm_string': Month format (e.g., '2023 Jan')
                                - 'n_date': Numeric date format (e.g., '2023-01-01')
                                - 'No': No transformation (default)
    
    Returns:
        pd.DataFrame: A standardized DataFrame with columns ['ds', 'y', 'unique_id'].
    """
    # Validate input DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input `df` must be a pandas DataFrame.")
    if ds not in df.columns:
        raise ValueError(f"Column '{ds}' not found in DataFrame.")
    if y not in df.columns:
        raise ValueError(f"Column '{y}' not found in DataFrame.")

    # Filter and copy the original DataFrame
    df2 = df[[ds, y]].copy()

    # Rename the time column
    df2.rename(columns={ds: 'ds'}, inplace=True)

    # Rename the y column
    df2['y'] = df2[y]

    # Group by 'ds' and sum 'y'
    df2 = df2.groupby('ds', as_index=False)['y'].sum()

    # Create unique ID
    df2['unique_id'] = y

    # Transform the 'ds' column based on the specified time format
    if t_type == 'q':
        df2['ds'] = df2['ds'].apply(convert_quarter_to_date)
    elif t_type == 'w':
        df2['ds'] = df2['ds'].apply(convert_week_to_date)
    elif t_type == 'y':
        df2['ds'] = pd.to_datetime(df2['ds'].astype(str) + '-01-01')
    elif t_type == 'm_string':
        df2['ds'] = pd.to_datetime(df2['ds'], format='%Y %b')
    elif t_type == 'n_date':
        df2['ds'] = pd.to_datetime(df2['ds'])
    elif t_type != 'No':
        raise ValueError(f"Invalid `t_type`: {t_type}. Valid options are 'q', 'w', 'y', 'm_string', 'n_date', or 'No'.")

    # Set 'ds' as the index and sort by date
    df2 = df2.set_index('ds', drop=False).rename_axis("Date_Index")
    return df2[['ds', 'y', 'unique_id']].sort_values('ds')


def get_residuals_arima(self_1):
    """
    Extracts standardized residuals from an ARIMA model.

    Args:
        self_1: A fitted ARIMA model object (e.g., from `statsmodels`).

    Returns:
        pd.Series: Standardized residuals of the ARIMA model.
    """
    # Validate input
    if not hasattr(self_1, 'filter_results'):
        raise AttributeError("Input model must have `filter_results` attribute.")

    # Eliminate residuals associated with burned or diffuse likelihoods
    d = np.maximum(self_1.loglikelihood_burn, self_1.nobs_diffuse)

    # Get residuals
    if hasattr(self_1.data, 'dates') and self_1.data.dates is not None:
        ix = self_1.data.dates[d:]
    else:
        ix = np.arange(self_1.nobs - d)

    # Extract standardized residuals
    resid = pd.Series(
        self_1.filter_results.standardized_forecasts_error[0, d:],  # Assuming variable index 0
        index=ix
    )

    return resid.dropna()