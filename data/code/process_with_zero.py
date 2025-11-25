import pandas as pd


INPUT_PATH = "data\\processed\\station_flow\\station_flow_202501.csv"
OUTPUT_PATH = "data\\processed\\station_flow\\station_flow_202501_new.csv"

STATION_ORDER = [
    "辛亥復興路口西北側",
    "新生南路三段52號前",
    "新生南路三段66號前",
    "新生南路三段82號前",
    "銘傳國小側門",
    "捷運公館站(2號出口)",
    "第二學生活動中心",
    "臺灣科技大學正門",
    "臺灣科技大學側門",
    "臺大男七舍前",
    "臺大男一舍前",
    "臺大男六舍前",
    "臺大動物醫院前",
    "臺大萬才館前",
    "臺大國青大樓宿舍前",
    "臺大社科院圖書館前",
    "臺大法人語言訓練中心前",
    "臺大綜合體育館停車場前",
    "辛亥新生路口東南側",
    "基隆長興路口東側",
    "捷運公館站(3號出口)",
    "新生南路三段94巷口",
    "基隆長興路口",
    "臺大資訊大樓",
    "捷運公館站(1號出口)",
    "捷運公館站(4號出口)",
    "臺大男八舍東側",
    "臺大禮賢樓東南側",
    "臺大農業陳列館北側",
    "臺大管理學院二館北側",
    "臺大土木系館",
    "臺大大一女舍北側",
    "臺大女九舍西南側",
    "臺大小福樓東側",
    "臺大立體機車停車場",
    "臺大工綜館南側",
    "臺大天文數學館南側",
    "臺大心理系館南側",
    "臺大樂學館東側",
    "臺大農化新館西側",
    "臺大五號館西側",
    "臺大舊體育館西側",
    "臺大共同教室東南側",
    "臺大鹿鳴堂東側",
    "臺大公館停車場西北側",
    "臺大第二行政大樓南側",
    "臺大明達館機車停車場",
    "臺大二號館",
    "臺大凝態館南側",
    "臺大社科院西側",
    "臺大社會系館南側",
    "臺大思亮館東南側",
    "臺大椰林小舖",
    "臺大計資中心南側",
    "臺大原分所北側",
    "臺大生命科學館西北側",
    "臺大第一活動中心西南側",
    "臺大博理館西側",
    "臺大博雅館西側",
    "臺大森林館北側",
    "臺大一號館",
    "臺大小小福西南側",
    "臺大教研館北側",
    "臺大四號館東北側",
    "臺大新生教室南側",
    "臺大鄭江樓北側",
    "臺大電機二館東南側",
    "臺大圖資系館北側",
    "臺大總圖書館西南側",
    "臺大黑森林西側",
    "臺大獸醫館南側",
    "臺大新體育館東南側",
    "臺大明達館北側(員工宿舍)",
]


def ensure_full_hours(df: pd.DataFrame) -> pd.DataFrame:
    """Guarantee each station-date block has hours 0-23, filling zeros when missing."""
    df = df.copy()

    # Drop helper index columns if present.
    helper_cols = [c for c in ("Unnamed: 0", "index") if c in df.columns]
    if helper_cols:
        df = df.drop(columns=helper_cols)

    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["hour"] = df["hour"].astype(int)

    # Decide final station order: preferred list first, then any leftover stations
    existing_order = df["station"].drop_duplicates().tolist()
    station_categories = [s for s in STATION_ORDER if s in existing_order]
    station_categories += [s for s in existing_order if s not in STATION_ORDER]
    df["station"] = pd.Categorical(df["station"], categories=station_categories, ordered=True)

    def fill_group(group: pd.DataFrame) -> pd.DataFrame:
        """Fill a single station/date group to all 24 hours."""
        if isinstance(group.name, tuple):
            base_station, base_date = group.name
        else:
            base_station = group["station"].iloc[0]
            base_date = group["date"].iloc[0]

        idx = pd.Index(range(24), name="hour")
        filled = group.set_index("hour").reindex(idx)
        filled["station"] = base_station
        filled["date"] = base_date
        filled["borrow_count"] = filled["borrow_count"].fillna(0)
        filled["return_count"] = filled["return_count"].fillna(0)
        return filled.reset_index()

    df = (
        df.groupby(["station", "date"], observed=True, group_keys=False)
        .apply(fill_group, include_groups=False)
        .reset_index(drop=True)
    )

    df["station"] = pd.Categorical(df["station"], categories=station_categories, ordered=True)
    df = df.sort_values(["station", "date", "hour"]).reset_index(drop=True)
    df["station"] = df["station"].astype(str)

    return df[["station", "date", "hour", "borrow_count", "return_count"]]


def main() -> None:
    df = pd.read_csv(INPUT_PATH)
    df = ensure_full_hours(df)
    df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()