import pandas as pd
from django.conf import settings
from datetime import date

ROOT_PATH = settings.BASE_DIR

def get_csv_data(csv_name):
    try:
        csv_data = pd.read_csv(ROOT_PATH / f'creator/dummy_data/{csv_name}')
        return csv_data
    except Exception as e:
        print("Error reading csv file: ", e)
        return None
    
def get_four_previous_weeks_date():
    data = []
    today = date.today()

    data_values = f'{today.day} {today.strftime("%B")} {today.year}'
    print("data_values:", data_values)
    data.append(data_values)
    
    while len(data) < 4:
        #  check if day is less than
        if today.day < 7:
            today = today.replace(day=30 - 7 + today.day, month=today.month-1)
        elif today.day < 7 and today.month == 1:
            today = today.replace(day=30 - 7 + today.day, month=12, year=today.year-1)
        else:
            today = today.replace(day=today.day-7)
        data_values = f'{today.day} {today.strftime("%B")} {today.year}'
        data.append(data_values)
    data.reverse()
    return data

def get_subs_for_last_four_weeks():
    try:
        df = pd.read_csv(ROOT_PATH / "creator/dummy_data/daily_subscribers.csv")
        data = []
        if len(df) >= 8:
            # Get the number of rows
            num_rows = len(df)

            # Get the seventh last row
            data.append(df.iloc[num_rows - 32]["Jumlah subscribers"])
            data.append(df.iloc[num_rows - 24]["Jumlah subscribers"])
            data.append(df.iloc[num_rows - 16]["Jumlah subscribers"])
            data.append(df.iloc[num_rows - 8]["Jumlah subscribers"])

            # Print the entire row
            # print(seventh_last_row)
            return data
        else:
            print("Error: Not enough rows in the CSV file")
            return data
    except Exception as e:
        print("Error reading csv file: ", e)
        return None