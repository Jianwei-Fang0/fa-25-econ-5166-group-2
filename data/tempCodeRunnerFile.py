import pandas as pd
fined_data = pd.read_csv("data\processed\station_flow\station_flow_202406.csv")
return_data_dates = sorted(fined_data['date'].unique())
print(f"歸還數據日期範圍: {min(return_data_dates)} 到 {max(return_data_dates)}")
print(f"歸還數據日期數量: {len(return_data_dates)}")