from fcst_python_ieseg.date_utils import convert_quarter_to_date
import pandas as pd

def test_convert_quarter_to_date():
    # Test case 1
    result = convert_quarter_to_date("2023 Q2")
    assert result == pd.Timestamp(year=int(2023), month=4, day=1), f"Expected '2023-04-01', got {result}"

    # Test case 2
    result = convert_quarter_to_date("2022 Q4")
    assert result == pd.Timestamp(year=int(2022), month=10, day=1), f"Expected '2022-10-01', got {result}"

    print("All tests passed!")