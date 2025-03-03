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