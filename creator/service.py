import pandas as pd
from django.conf import settings
from datetime import date
from .algorithm.linear_regression import linear_regression
from .algorithm.k_means_clustering import k_means_clustering
import calendar
from datetime import datetime

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
    data.append(data_values)
    
    while len(data) < 4:
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
            num_rows = len(df)
            
            COLUMN_NAME = "Jumlah subscribers"
            data.append(df.iloc[num_rows - 32][COLUMN_NAME])
            data.append(df.iloc[num_rows - 24][COLUMN_NAME])
            data.append(df.iloc[num_rows - 16][COLUMN_NAME])
            data.append(df.iloc[num_rows - 8][COLUMN_NAME])

            return data
        else:
            print("Error: Not enough rows in the CSV file")
            return data
    except Exception as e:
        print("Error reading csv file: ", e)
        return None
    
def get_analytics_restls():
    strength = []
    weakness = []
    to_do = []
    
    try:
        csv = pd.read_csv(ROOT_PATH / "creator/dummy_data/daily_subscribers.csv")
        hari_ke = []
        
        jumlah_subscribers = []
        for i in range(len(csv)):
            jumlah_subscribers.append(csv.iloc[i]["Jumlah subscribers"])
            hari_ke.append(csv.iloc[i]["Hari ke"])
        
        strength, weakness, to_do = predict_subscribers(hari_ke, jumlah_subscribers, strength, weakness, to_do)
        strength, weakness, to_do = clustering_subscribers(hari_ke, jumlah_subscribers, strength, weakness, to_do)
        
        if len(weakness) == 0:
            weakness.append("Tidak ada yang perlu dikhawatirkan, kamu sudah melakukan yang terbaik!")
        
        return strength, weakness, to_do
    except Exception as e:
        print("Error reading csv file: ", e)
        return None, None, None

def predict_subscribers(hari_ke, jumlah_subscribers, strength, weakness, to_do):
    next_week = hari_ke[-1] + 7
    predict = linear_regression(hari_ke, jumlah_subscribers, next_week)
    
    diff_percentage = round(((predict - jumlah_subscribers[-1]) / jumlah_subscribers[-1]) * 100)
    if predict > jumlah_subscribers[-1]:
        strength.append(f'Jumlah subscribers kamu diperkirakan mengalami kenaikan sebesar {diff_percentage}% dari minggu ini')
        to_do.append("Tetap konsisten dalam mengunggah konten yang menarik!")
    else:
        weakness.append(f'Jumlah subscribers kamu mengalami penurunan sebesar {diff_percentage}% dari minggu ini')
        to_do.append("Coba posting lebih sering untuk menarik lebih banyak subscribers")
    
    return strength, weakness, to_do

def construct_data(hari_ke, jumlah_subscribers):
    curr_day = datetime.now().day
    curr_idx = hari_ke[-1] - curr_day
    subscribers_for_each_month = jumlah_subscribers[curr_idx - 1]
    curr_month = datetime.now().month
    curr_year = datetime.now().year
    previous_month = curr_month - 1
    days_left = 365
    
    reports = []
    percentage_deviation_arr = []
    total_subscribers = []
    months_name = []
    
    while days_left > 0:
        if previous_month == 0:
            previous_month = 12
            curr_year -= 1
        days_int_month = calendar.monthrange(curr_year, curr_month)[1]
        days_left -= days_int_month
        
        reports.append({
            "month": previous_month,
            "year": curr_year,
            "total_subscribers": subscribers_for_each_month
        })
        months_name.append(calendar.month_name[previous_month])
        total_subscribers.append(subscribers_for_each_month)
        
        
        curr_idx -= days_int_month
        subscribers_for_each_month = jumlah_subscribers[curr_idx]
        previous_month -= 1
        
        # get avarage of subscribers for 1 year or 365 days
        sum = 0
        percentage_deviation = 0
        for item in reports:
            sum += item["total_subscribers"]
        avg = sum / len(reports)
        
        # count the percentage deviation
        for item in reports:
            percentage_deviation = ((abs(item["total_subscribers"] - avg)) / avg) * 100
            item["percentage_deviation"] = percentage_deviation
            item["subscribers_avg"] = avg
            percentage_deviation_arr.append(percentage_deviation)
    
    return total_subscribers, percentage_deviation_arr, months_name
    
def clustering_subscribers(hari_ke, jumlah_subscribers, strength, weakness, to_do):
    total_subscribers, percentage_deviation, months_name = construct_data(hari_ke, jumlah_subscribers)
    paired_list = [[x_val, y_val] for x_val, y_val in zip(total_subscribers, percentage_deviation)]
    clusters = k_means_clustering(paired_list)

    high_cluster_arr = []
    high_month = []
    
    low_cluster_arr = []
    low_month = []

    for index, item in enumerate(clusters):
        if item == 0:
            high_cluster_arr.append(item)
            high_month.append(months_name[index])
        else:
            low_cluster_arr.append(item)
            
    delimiter = ", "
    if len(high_cluster_arr) > len(low_cluster_arr):
        month_str = delimiter.join(high_month)
        strength.append(f'Kenaikan jumlah subscribers kamu lebih tinggi dibandingkan rata-rata bulanan, yaitu pada bulan {month_str} ')
    elif len(low_cluster_arr) > len(high_cluster_arr):
        month_str = delimiter.join(low_month)
        weakness.append(f'Kenaikan jumlah subscribers kamu lebih rendah dibandingkan rata-rata bulanan, yaitu pada bulan {month_str} ')
        to_do.append(f"Coba posting lebih sering untuk menarik lebih banyak subscribers, terutama pada bulan {month_str}")
    else:
        strength.append("Kenaikan jumlah subscribers kamu seimbang dengan rata-rata bulanan")
        
    return strength, weakness, to_do