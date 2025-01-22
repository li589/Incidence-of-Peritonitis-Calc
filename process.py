import os
import pandas as pd
import numpy as np
from tqdm import tqdm

def open_csv(filename):
    try:
        return pd.read_csv(filename)
    except pd.errors.ParserError:
        print(f"Error: Unable to read CSV file {filename}. Skipping...")
        return None
    
def read_datetime(df_loc):
    # 2008/12/10 0:00
    # p1, p2 = df_loc.split(' ')
    # yr, mon, day = p1.split('/')
    yr, mon, day = df_loc.split('/')
    return int(yr), int(mon), int(day)

def calc_datetime_sub(first_datetime, end_datetime):
    year = int(first_datetime[0])
    month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and (year % 100!= 0 or year % 400 == 0):
        month_day[1] = 29
    first_month = first_datetime[1]
    first_day = first_datetime[2]
    end_month = end_datetime[1]
    end_day = end_datetime[2]
    full_mon = end_month - first_month - 1
    first_cut = (month_day[first_month-1] - first_day + 1)/month_day[first_month-1]
    end_cut = end_day/month_day[end_month-1]
    return full_mon + first_cut + end_cut

def main(all_df, quit_df, out_path, set_year = 2023):
    list_index = []
    list_name = []
    list_dalta = []
    all_df = all_df.dropna(subset=["插管时间"])
    quit_df = quit_df.dropna()
    for index, line in tqdm(enumerate(all_df.iterrows())):
        year, month, day = read_datetime(line[1]["插管时间"])
        print(f"{year}-{month}-{day}")
        if year != set_year or int(year) != set_year:
            continue
        quit_date = [set_year, 12, 31]
        all_quit_info = line[1]["退出日期"]
        if all_quit_info == '' or all_quit_info == None:
            for quit_index, quit_line in enumerate(quit_df.iterrows()):
                if quit_line[1]["姓名"] != line[1]["姓名"]:
                    continue
                quit_year, quit_mon, quit_day = read_datetime(quit_line[1]["退出日期"])
                if quit_year != set_year or int(quit_year) != set_year:
                    continue
                quit_date = [quit_year, quit_mon, quit_day]
                # break
        delta_mon = calc_datetime_sub([year, month, day], quit_date)
        list_index.append(index)
        list_name.append(line[1]["姓名"])
        list_dalta.append(delta_mon)
    df_result = pd.DataFrame({"序号": list_index, "姓名": list_name, "月份总和": list_dalta})
    df_result.to_csv(out_path, index=False)
    

if __name__ == "__main__":
    all_people_data_path = os.path.join("ALL.csv")
    quit_people_data_path = os.path.join("quit_people.csv")
    output_data_path = os.path.join("output.csv")
    
    all_people_data = open_csv(all_people_data_path)
    quit_people_data = open_csv(quit_people_data_path)
    main(all_people_data, quit_people_data, output_data_path)