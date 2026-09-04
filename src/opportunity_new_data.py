
import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# OPPORTUNITY AREA ANALYSIS
# New dataset version
#
# Logic:
# High local order demand
#        +
# Relatively low competitor presence
#        =
# Potential opportunity area
#
# Input:
#   customer_orders_with_clusters.csv
#   Competitors.csv
#
# Output:
#   opportunity_areas.csv
# ============================================================

ORDERS_FILE = Path("customer_orders_with_clusters.csv")
COMPETITOR_FILE = Path("Competitors.csv")
OUTPUT_FILE = Path("opportunity_areas.csv")


# ============================================================
# 1. LOAD DATA
# ============================================================

orders = pd.read_csv(ORDERS_FILE)
competitors = pd.read_csv(COMPETITOR_FILE)

print("Orders loaded:", len(orders))
print("Competitor records loaded:", len(competitors))


# ============================================================
# 2. CHECK REQUIRED COLUMNS
# ============================================================

required_orders = [
    "Order_ID",
    "Customer_Lat",
    "Customer_Lon",
    "Order_Timestamp",
    "Order_Value_INR",
    "Order_Hour",
    "cluster"
]

required_competitors = [
    "Store ID",
    "Company",
    "City",
    "Latitude",
    "Longitude"
]

missing_orders = [
    c for c in required_orders
    if c not in orders.columns
]

missing_competitors = [
    c for c in required_competitors
    if c not in competitors.columns
]

if missing_orders:
    raise ValueError(
        f"Missing order columns: {missing_orders}"
    )

if missing_competitors:
    raise ValueError(
        f"Missing competitor columns: {missing_competitors}"
    )


# ============================================================
# 3. KEEP BENGALURU COMPETITORS
# ============================================================

city = (
    competitors["City"]
    .astype(str)
    .str.strip()
    .str.lower()
)

competitors = competitors[
    city.isin(["bengaluru", "bangalore"])
].copy()

print("Bengaluru competitor stores:", len(competitors))


# ============================================================
# 4. CREATE SMALL GEOGRAPHIC ZONES
# ============================================================
# We use approximately 1 km cells.
#
# This is only for identifying local demand pockets.
# It is NOT a claim about actual business boundaries.
# ============================================================

GRID_SIZE_KM = 1.0

mean_lat = orders["Customer_Lat"].mean()

lat_step = GRID_SIZE_KM / 111.0

lon_step = GRID_SIZE_KM / (
    111.0 * np.cos(np.radians(mean_lat))
)

base_lat = orders["Customer_Lat"].min()
base_lon = orders["Customer_Lon"].min()

orders["grid_lat"] = np.floor(
    (orders["Customer_Lat"] - base_lat) / lat_step
).astype(int)

orders["grid_lon"] = np.floor(
    (orders["Customer_Lon"] - base_lon) / lon_step
).astype(int)


# ============================================================
# 5. CALCULATE DEMAND FOR EACH SMALL ZONE
# ============================================================

zones = (
    orders
    .groupby(["grid_lat", "grid_lon"])
    .agg(
        total_orders=("Order_ID", "count"),
        cluster=("cluster", lambda x: int(x.mode().iloc[0])),
        center_lat=("Customer_Lat", "mean"),
        center_lon=("Customer_Lon", "mean")
    )
    .reset_index()
)

# Number of unique days in the dataset
orders["Order_Timestamp"] = pd.to_datetime(
    orders["Order_Timestamp"]
)

analysis_days = orders["Order_Timestamp"].dt.date.nunique()

zones["avg_daily_orders"] = (
    zones["total_orders"] / analysis_days
)


# ============================================================
# 6. HAVERSINE DISTANCE
# ============================================================

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)

    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(dlon / 2) ** 2
    )

    return 2 * R * np.arcsin(
        np.sqrt(a)
    )


# ============================================================
# 7. COMPETITOR COVERAGE
# ============================================================

COMPETITOR_RADIUS_KM = 2.0

competitor_lat = competitors[
    "Latitude"
].to_numpy(dtype=float)

competitor_lon = competitors[
    "Longitude"
].to_numpy(dtype=float)

competitor_counts = []
nearest_competitor = []

for _, zone in zones.iterrows():

    distances = haversine(
        zone["center_lat"],
        zone["center_lon"],
        competitor_lat,
        competitor_lon
    )

    competitor_counts.append(
        int(np.sum(
            distances <= COMPETITOR_RADIUS_KM
        ))
    )

    nearest_competitor.append(
        round(float(np.min(distances)), 2)
    )


zones["competitors_within_2km"] = (
    competitor_counts
)

zones["nearest_competitor_km"] = (
    nearest_competitor
)


# ============================================================
# 8. DEMAND LEVEL
# ============================================================
# High demand = top 25% of zones by order count.
# Medium = middle 50%.
# Low = bottom 25%.
# ============================================================

q75 = zones["total_orders"].quantile(0.75)
q25 = zones["total_orders"].quantile(0.25)

zones["demand_level"] = np.select(
    [
        zones["total_orders"] >= q75,
        zones["total_orders"] <= q25
    ],
    [
        "High",
        "Low"
    ],
    default="Medium"
)


# ============================================================
# 9. SIMPLE OPPORTUNITY CLASSIFICATION
# ============================================================
# We focus on:
#
# High demand + 0-2 competitors = High Opportunity
# High/Medium demand + <=5 competitors = Medium Opportunity
# Everything else = Low Opportunity
# ============================================================

zones["opportunity_level"] = np.select(
    [
        (
            (zones["demand_level"] == "High")
            & (zones["competitors_within_2km"] <= 2)
        ),
        (
            zones["demand_level"].isin(
                ["High", "Medium"]
            )
            & (zones["competitors_within_2km"] <= 5)
        )
    ],
    [
        "High Opportunity",
        "Medium Opportunity"
    ],
    default="Low Opportunity"
)


# ============================================================
# 10. SIMPLE OPPORTUNITY SCORE
# ============================================================
# This is only a ranking aid.
#
# 60% relative demand
# 40% relative low competition
# ============================================================

max_orders = zones["total_orders"].max()
max_competitors = zones["competitors_within_2km"].max()

zones["demand_score"] = (
    zones["total_orders"]
    / max_orders
    * 100
)

if max_competitors > 0:

    zones["competition_score"] = (
        1
        - zones["competitors_within_2km"]
        / max_competitors
    ) * 100

else:

    zones["competition_score"] = 100


zones["opportunity_score"] = (
    0.60 * zones["demand_score"]
    + 0.40 * zones["competition_score"]
)


# ============================================================
# 11. RANK
# ============================================================

priority = {
    "High Opportunity": 1,
    "Medium Opportunity": 2,
    "Low Opportunity": 3
}

zones["priority"] = (
    zones["opportunity_level"]
    .map(priority)
)

zones = zones.sort_values(
    [
        "priority",
        "opportunity_score",
        "avg_daily_orders"
    ],
    ascending=[True, False, False]
).reset_index(drop=True)

zones.insert(
    0,
    "opportunity_id",
    [
        f"OPP{i:03d}"
        for i in range(1, len(zones) + 1)
    ]
)


# ============================================================
# 12. FINAL OUTPUT COLUMNS
# ============================================================

output = zones[
    [
        "opportunity_id",
        "cluster",
        "center_lat",
        "center_lon",
        "total_orders",
        "avg_daily_orders",
        "demand_level",
        "competitors_within_2km",
        "nearest_competitor_km",
        "opportunity_score",
        "opportunity_level"
    ]
].copy()


# ============================================================
# 13. SAVE
# ============================================================

output.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 14. DISPLAY TOP RESULTS
# ============================================================

print("\n============================================")
print("TOP OPPORTUNITY AREAS")
print("============================================")

print(
    output
    .head(15)
    .round(2)
    .to_string(index=False)
)

print("\nOutput saved to:")
print(OUTPUT_FILE)


# ============================================================
# 15. INTERVIEW NOTE
# ============================================================

print("\nINTERVIEW LOGIC:")
print(
    "1. Count customer orders in small geographic zones."
)
print(
    "2. Measure competitor stores within 2 km."
)
print(
    "3. Identify relatively high-demand and lower-competition zones."
)
print(
    "4. Treat these as potential opportunity areas, "
    "not confirmed dark-store locations."
)
