import pandas as pd
import time
## 加 header

data_path= "data\\raw\\202501_YouBike.csv"

with open(data_path, "r", encoding="utf-8", errors="replace") as f:
    raw_data = pd.read_csv(f, header=None)

raw_data.columns = [
    "borrow_datetime", "borrow_site",
    "return_datetime", "return_site",
    "borrowing_time","type", "date"
]

raw_data.to_csv(data_path, index=False, encoding="utf-8-sig")



# 　只留下NTU站

def extract_station_name(sna):
    """從 sna 中提取 YouBike2.0_ 後面的部分"""
    if sna.startswith("YouBike2.0_"):
        return sna[11:]  # 移除 "YouBike2.0_" (11個字符)
    return sna  # 如果沒有前綴，直接返回原值



ntu_station = pd.read_csv("data/raw/ntu_area_ubike_stations_new.csv")
ntu_stations = set(ntu_station["sna"].apply(extract_station_name))

# 分批處理大檔案
saved_fined_datapath = "data\\processed\\ntu_youbike_data_202501.csv"
flow_datapath = "data\\processed\\station_flow_202501.csv"

chunk_size = 100000  # 每次處理10萬筆
ntu_data_chunks = []

print("開始分批過濾數據...")
start_time = time.time()

with open(data_path, "r", encoding="utf-8", errors="replace") as f:
    raw_data = pd.read_csv(f)
    
try:
    # 分批讀取和過濾
    for chunk_num, chunk in enumerate(pd.read_csv(data_path, chunksize=chunk_size)):
        print(f"處理第 {chunk_num + 1} 批數據 ({len(chunk)} 筆)...")
        
        # 過濾NTU相關的借還車記錄
        ntu_chunk = chunk[
            (chunk['borrow_site'].isin(ntu_stations)) | 
            (chunk['return_site'].isin(ntu_stations))
        ]
        
        if len(ntu_chunk) > 0:
            ntu_data_chunks.append(ntu_chunk)
            print(f"  -> 找到 {len(ntu_chunk)} 筆NTU相關記錄")
        
        # 每處理10批顯示進度
        if (chunk_num + 1) % 10 == 0:
            elapsed = time.time() - start_time
            print(f"已處理 {chunk_num + 1} 批，耗時 {elapsed:.1f} 秒")

except Exception as e:
    print(f"處理過程中出現錯誤: {e}")
    # 如果出錯，嘗試用更小的chunk_size
    print("嘗試用更小的批次大小...")
    chunk_size = 50000
    ntu_data_chunks = []
    
    for chunk_num, chunk in enumerate(pd.read_csv(data_path, chunksize=chunk_size)):
        print(f"處理第 {chunk_num + 1} 批數據...")
        ntu_chunk = chunk[
            (chunk['borrow_site'].isin(ntu_stations)) | 
            (chunk['return_site'].isin(ntu_stations))
        ]
        if len(ntu_chunk) > 0:
            ntu_data_chunks.append(ntu_chunk)

# 合併所有NTU數據
if ntu_data_chunks:
    print("合併所有NTU數據...")
    ntu_data = pd.concat(ntu_data_chunks, ignore_index=True)
    
    print(f"過濾完成！")
    print(f"原始數據: {len(data_path)}")
    print(f"NTU相關數據: {len(ntu_data)} 筆")
    print(f"過濾率: {len(ntu_data)/5552542*100:.2f}%")
    
    # 保存過濾後的數據
    output_file = saved_fined_datapath
    ntu_data.to_csv(output_file, index=False, encoding="utf-8-sig")
    print(f"已保存到: {output_file}")
    
    # 開始時段統計分析
    print("\n開始時段統計分析...")
    
    # 轉換時間格式
    ntu_data['borrow_datetime'] = pd.to_datetime(ntu_data['borrow_datetime'])
    ntu_data['return_datetime'] = pd.to_datetime(ntu_data['return_datetime'])
    
    # 提取日期和小時
    ntu_data['borrow_date'] = ntu_data['borrow_datetime'].dt.date
    ntu_data['borrow_hour'] = ntu_data['borrow_datetime'].dt.hour
    ntu_data['return_date'] = ntu_data['return_datetime'].dt.date
    ntu_data['return_hour'] = ntu_data['return_datetime'].dt.hour
    
    
    # 統計各站點各時段借用量
    print("\n=== 各站點各時段借用量 ===")
    # 只統計從NTU站點借出的記錄
    ntu_borrow_data = ntu_data[ntu_data['borrow_site'].isin(ntu_stations)]
    station_borrow_hour = ntu_borrow_data.groupby(['borrow_site', 'borrow_date', 'borrow_hour']).size().reset_index(name='borrow_count')
    print(f"NTU借出數據形狀: {station_borrow_hour.shape}")
    print(station_borrow_hour.head())
    
    # 統計各站點各時段歸還量（只統計NTU站點的歸還）
    print("\n=== 各站點各時段歸還量 ===")
    # 只統計還到NTU站點的記錄
    ntu_return_data = ntu_data[ntu_data['return_site'].isin(ntu_stations)]
    station_return_hour = ntu_return_data.groupby(['return_site', 'return_date', 'return_hour']).size().reset_index(name='return_count')
    print(f"NTU歸還數據形狀: {station_return_hour.shape}")
    print(station_return_hour.head())
    
    # 保存統計結果
    print("\n保存統計結果...")
    
    # 重命名欄位以便合併
    station_borrow_hour = station_borrow_hour.rename(columns={
        'borrow_site': 'station', 
        'borrow_date': 'date', 
        'borrow_hour': 'hour'
    })
    station_return_hour = station_return_hour.rename(columns={
        'return_site': 'station', 
        'return_date': 'date', 
        'return_hour': 'hour'
    })
    
    # 合併借出和借入數據
    station_flow = pd.merge(
        station_borrow_hour, 
        station_return_hour, 
        on=['station', 'date', 'hour'], 
        how='outer'
    ).fillna(0)
    
    print("合併後的流量數據:")
    print(station_flow.head(10))

    print(f"\n=== 數據統計 ===")
    print(f"總記錄數: {len(station_flow)}")
    print(f"站點數: {station_flow['station'].nunique()}")
    print(f"日期數: {station_flow['date'].nunique()}")
    print(f"小時數: {station_flow['hour'].nunique()}")
    
    # 保存流量數據
    station_flow.to_csv(flow_datapath, encoding="utf-8-sig")
        
    
    
    print("統計結果已保存到 data/processed/ 目錄")
    
    
    # # 顯示熱門站點
    # print("\n=== 熱門站點分析 ===")
    # borrow_counts = ntu_data['borrow_site'].value_counts()
    # return_counts = ntu_data['return_site'].value_counts()
    
    # print("借車熱門站點 (前5名):")
    # print(borrow_counts.head())
    
    # print("\n還車熱門站點 (前5名):")
    # print(return_counts.head())
    
else:
    print("未找到任何NTU相關數據")

total_time = time.time() - start_time
print(f"\n總處理時間: {total_time:.1f} 秒")

# import pandas as pd
fined_data = pd.read_csv("data\processed\station_flow_202501.csv")
return_data_dates = sorted(fined_data['date'].unique())
print(f"歸還數據日期範圍: {min(return_data_dates)} 到 {max(return_data_dates)}")
print(f"歸還數據日期數量: {len(return_data_dates)}")


    




