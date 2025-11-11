import pandas as pd

df = pd.DataFrame({'date': pd.date_range('2024-03-01', '2025-01-31')})
df['weekday'] = df['date'].dt.weekday  # 星期幾（週一=0, 週日=6）
df['is_weekend'] = df['weekday'] >= 5  # 週六日為 True
# 刪除不必要的 weekday 欄
df = df.drop(['weekday'], axis=1)



# === 2024年 國定假日 ===
holidays_2024 = [
    # 元旦
    "2023-12-30", "2023-12-31", "2024-01-01",
    # 春節
    "2024-02-08", "2024-02-09", "2024-02-10", "2024-02-11", "2024-02-12", "2024-02-13", "2024-02-14",
    # 228紀念日
    "2024-02-28",
    # 兒童節及清明節
    "2024-04-04", "2024-04-05", "2024-04-06", "2024-04-07",
    # 五一勞動節（僅勞工）
    "2024-05-01",
    # 端午節
    "2024-06-08", "2024-06-09", "2024-06-10",
    # 中秋節
    "2024-09-17",
    # 國慶日
    "2024-10-10"
]

# === 2025年 國定假日 ===
holidays_2025 = [
    # 元旦
    "2025-01-01",
    # 春節連假：1/25(六)~2/2(日)
    "2025-01-25", "2025-01-26", "2025-01-27", "2025-01-28",
    "2025-01-29", "2025-01-30", "2025-01-31", "2025-02-01", "2025-02-02",
    # 補班日（非假日）：2025-02-08
]

# 合併成完整假期清單
taiwan_holidays = holidays_2024 + holidays_2025

# 轉為日期型別（方便比對 DataFrame 的 date 欄）
taiwan_holidays = pd.to_datetime(taiwan_holidays)
print(taiwan_holidays)

df['is_holiday'] = df['date'].isin(taiwan_holidays)

# 檢查輸出
print(df.head())
df.to_csv("data\\processed\\weekdayornot.csv")