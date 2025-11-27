import pandas as pd

FLOW_PATH = "data\\processed\\station_flow\\station_flow_202501_new.csv"
ROUTES_PATH = "data\\processed\\ntu_youbike_data\\routes_with_sno_clean.csv"
OUTPUT_PATH = "data\\processed\\station_flow\\station_flow_202501_new.csv"
DISTANCE_THRESHOLD_KM = 0.4


def clean_station_name(value: str) -> str:
    """Remove the YouBike prefix to match station names in flow data."""
    prefix = "YouBike2.0_"
    if value.startswith(prefix):
        return value[len(prefix) :]
    return value


def build_neighbor_edges(routes: pd.DataFrame, threshold_km: float) -> pd.DataFrame:
    """Return station-to-neighbor pairs whose distance is within the threshold."""
    routes = routes.copy()
    routes["origin"] = routes["origin"].apply(clean_station_name)
    routes["destination"] = routes["destination"].apply(clean_station_name)

    close_routes = routes[routes["distance_km"] <= threshold_km]
    # print(
    #     f"[INFO] Found {len(close_routes)} origin-destination pairs within {threshold_km * 1000:.0f}m"
    # )
    # print("[INFO] Sample pairs:")
    # print(close_routes[["origin", "destination", "distance_km"]].head())
    
    edges = close_routes[["origin", "destination"]].rename(
        columns={"origin": "station", "destination": "neighbor"}
    )
    reverse_edges = edges.rename(columns={"station": "neighbor", "neighbor": "station"})

    combined = (
        pd.concat([edges, reverse_edges], ignore_index=True)
        .drop_duplicates()
        .query("station != neighbor")
        .reset_index(drop=True)
    )

    unique_stations = combined["station"].drop_duplicates().tolist()
    for idx, station in enumerate(unique_stations, start=1):
        neighbors = combined.loc[combined["station"] == station, "neighbor"].tolist()
        neighbor_list = ", ".join(neighbors)
        # print(
        #     f"[INFO] Station {idx}/{len(unique_stations)} ({station}) has "
        #     f"{len(neighbors)} neighbors within {threshold_km * 1000:.0f}m: {neighbor_list}"
        # )

    return combined


def add_neighbor_inventory(flow: pd.DataFrame, edges: pd.DataFrame) -> pd.DataFrame:
    """Attach a neighbor inventory column using adjacency edges."""
    flow = flow.copy().reset_index(drop=True)
    helper_cols = [c for c in ("Unnamed: 0", "index") if c in flow.columns]
    if helper_cols:
        flow = flow.drop(columns=helper_cols)

    if "inventory" not in flow.columns:
        raise ValueError("Flow data must contain an 'inventory' column.")

    flow["station"] = flow["station"].astype(str)
    flow["date"] = pd.to_datetime(flow["date"])
    flow["hour"] = flow["hour"].astype(int)
    flow["row_id"] = flow.index

    # Only keep edges whose stations exist in flow data.
    valid_stations = set(flow["station"].unique())
    edges = edges[edges["station"].isin(valid_stations)]
    edges = edges[edges["neighbor"].isin(valid_stations)]

    if edges.empty:
        flow["neighbor_inventory_450m"] = 0.0
        return flow.drop(columns="row_id")

    neighbor_map = flow.merge(edges, on="station", how="left")

    neighbor_inventory = flow[
        ["station", "date", "hour", "inventory"]
    ].rename(columns={"station": "neighbor", "inventory": "neighbor_inventory"})

    neighbor_values = neighbor_map.merge(
        neighbor_inventory,
        on=["neighbor", "date", "hour"],
        how="left",
    )

    sums = (
        neighbor_values.groupby("row_id")["neighbor_inventory"]
        .sum(min_count=1)
        .fillna(0)
    )

    flow["neighbor_inventory_450m"] = flow["row_id"].map(sums).fillna(0)

    return flow.drop(columns="row_id")


def main() -> None:
    routes = pd.read_csv(ROUTES_PATH)
    edges = build_neighbor_edges(routes, DISTANCE_THRESHOLD_KM)

    flow = pd.read_csv(FLOW_PATH)
    flow_with_neighbors = add_neighbor_inventory(flow, edges)
    flow_with_neighbors.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")


if __name__ == "__main__":
    main()

