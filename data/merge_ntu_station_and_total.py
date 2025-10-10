import pandas as pd

with open("J:\\NTU\\fa-25-econ-5166-group-2\data\\2405_ntu_youbike_data_new.csv", "r", encoding="utf-8", errors="replace") as f:
    total_data = pd.read_csv(f)
    
unique_totals = total_data.groupby("sno", as_index=False)["total"].first()
print(unique_totals)



stations = pd.read_csv("data\\processed\\ntu_area_ubike_stations_new.csv")
stations = pd.merge(stations, unique_totals, how='left', on="sno")
print(stations)
stations.to_csv("data\\processed\\ntu_area_ubike_stations_new.csv", index=False, encoding="utf-8-sig")