import pandas as pd 
import glob
import os

files = glob.glob("taipei_daan_weather_data/*.csv")

all_data = []

for file in files:
    headers = pd.read_csv(file, nrows=1, header=None).values.tolist()[0]
    df = pd.read_csv(file, skiprows=2, names=headers)
    df["source_file"] = os.path.basename(file)
    all_data.append(df)

print('loop completed ')

merged = pd.concat(all_data, ignore_index=True)
merged.to_csv("weather_2024_full.csv", index=False, encoding="utf-8-sig")

print('merge completed')