import pandas as pd

INPUT_PATH = "data\\processed\\station_flow\\station_flow_202501_new.csv"
OUTPUT_PATH = "data\\processed\\station_flow\\station_flow_202501_new.csv"
INITIAL_STATION_PATH = "data\\processed\\ntu_youbike_data\\ntu_area_ubike_stations_sorted.csv"

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


def load_initial_totals(path: str) -> pd.Series:
    """Load starting bike totals indexed by station name."""
    stations = pd.read_csv(path)
    stations["station"] = stations["sna"].str.replace("YouBike2.0_", "", n=1, regex=False)
    return stations.set_index("station")["total"]


def build_station_order(df: pd.DataFrame) -> list[str]:
    """Combine preferred station order with any extra stations present in the data."""
    observed = df["station"].drop_duplicates().tolist()
    ordered = [s for s in STATION_ORDER if s in observed]
    ordered += [s for s in observed if s not in ordered]
    return ordered


def add_inventory(df: pd.DataFrame, initial_totals: pd.Series) -> pd.DataFrame:
    """Append an inventory column based on cumulative returns/borrows."""
    df = df.copy()
    helper = [c for c in ("Unnamed: 0", "index") if c in df.columns]
    if helper:
        df = df.drop(columns=helper)

    df["date"] = pd.to_datetime(df["date"])
    df["hour"] = df["hour"].astype(int)
    df["station"] = df["station"].astype(str)

    station_order = build_station_order(df)
    df["station"] = pd.Categorical(df["station"], categories=station_order, ordered=True)
    df = df.sort_values(["station", "date", "hour"]).reset_index(drop=True)
    df["station"] = df["station"].astype(str)

    def compute_inventory(group: pd.DataFrame) -> pd.DataFrame:
        if "station" in group.columns:
            station = group["station"].iloc[0]
        else:
            station = group.name
            group = group.assign(station=station)
        start = initial_totals.get(station, 0)
        net = group["return_count"].cumsum() - group["borrow_count"].cumsum()
        group["inventory"] = start + net
        return group

    df = (
        df.groupby("station", group_keys=False, observed=True)
        .apply(compute_inventory, include_groups=False)
        .reset_index(drop=True)
    )

    return df[["station", "date", "hour", "borrow_count", "return_count", "inventory"]]


def main() -> None:
    totals = load_initial_totals(INITIAL_STATION_PATH)
    flow = pd.read_csv(INPUT_PATH)
    enriched = add_inventory(flow, totals)
    enriched.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()

