import pandas as pd

def convert_quarter_to_date(quarter_str):
    """
    Converts a quarter string (e.g., '2023 Q1') to a pandas Timestamp.
    
    Args:
        quarter_str (str): String in the format 'YYYY QN' where YYYY is the year 
                          and N is the quarter number (1-4)
    
    Returns:
        pd.Timestamp: First day of the first month in the quarter
    """
    year, quarter = quarter_str.split(' ')
    month = {'Q1': 1, 'Q2': 4, 'Q3': 7, 'Q4': 10}[quarter]  # Map quarters to their starting months
    return pd.Timestamp(year=int(year), month=month, day=1)

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
    year, week = week_str.split(' W')
    return pd.to_datetime(f'{year}-W{week}-1', format='%Y-W%W-%w')