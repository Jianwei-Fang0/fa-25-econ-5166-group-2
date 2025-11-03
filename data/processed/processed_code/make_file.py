import pandas as pd

data_path = "J:\\NTU\\fa-25-econ-5166-group-2\\data\\processed\\ntu_area_ubike_stations_sorted.csv"

df = pd.read_csv(data_path)

snas =  df["sna"].str.replace(r"^YouBike2\.0_", "", regex=True)


# --- 讀取站點流量資料 ---
data_raw = r"J:\\NTU\\fa-25-econ-5166-group-2\\data\\processed\\station_flow\\station_flow_202405.csv"
raw_data = pd.read_csv(data_raw)

# 🔹 用 snas 當作外部排序順序，並套用到 raw_data["station"]
raw_data["station"] = pd.Categorical(raw_data["station"], categories=snas, ordered=True)

# 🔹 排序：依 station（外部順序）+ date + hour
station_new_03 = raw_data.sort_values(by=["station", "date", "hour"], ascending=[True, True, True]).reset_index(drop=True)

print(station_new_03)
station_new_03.to_csv("station_flow_202405_new.csv", index=False)