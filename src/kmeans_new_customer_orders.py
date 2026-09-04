
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from pathlib import Path

# =========================================================
# K-MEANS CLUSTERING FOR NEW CUSTOMER ORDER DATA
# =========================================================
# New input file:
# customer_orders.csv
#
# Columns in new dataset:
# Order_ID
# Customer_Lat
# Customer_Lon
# Order_Timestamp
# Order_Value_INR
# Order_Hour
# Order_Time_Str
#
# We do NOT need Number_of_Items.
# =========================================================

# ---------------------------------------------------------
# 1. FILE PATHS
# ---------------------------------------------------------

INPUT_FILE = Path("customer_orders.csv")

OUTPUT_ORDERS = Path("customer_orders_with_clusters.csv")
OUTPUT_SUMMARY = Path("demand_cluster_summary.csv")
OUTPUT_MODEL = Path("kmeans_model_comparison.csv")


# ---------------------------------------------------------
# 2. LOAD DATA
# ---------------------------------------------------------

orders = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully.")
print("Number of orders:", len(orders))

print("\nColumns:")
print(orders.columns.tolist())


# ---------------------------------------------------------
# 3. CHECK REQUIRED COLUMNS
# ---------------------------------------------------------

required_columns = [
    "Order_ID",
    "Customer_Lat",
    "Customer_Lon",
    "Order_Timestamp",
    "Order_Value_INR",
    "Order_Hour",
    "Order_Time_Str"
]

missing_columns = [
    col for col in required_columns
    if col not in orders.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


# ---------------------------------------------------------
# 4. PREPARE DATA FOR K-MEANS
# ---------------------------------------------------------
# We only use geographic coordinates.
#
# K-Means question:
# "Where are customer orders geographically concentrated?"
# ---------------------------------------------------------

X = orders[
    [
        "Customer_Lat",
        "Customer_Lon"
    ]
].copy()


# ---------------------------------------------------------
# 5. TEST DIFFERENT K VALUES
# ---------------------------------------------------------
# We test K = 3 to 8.
#
# Inertia -> helps with the Elbow Method
# Silhouette -> helps compare cluster separation
# ---------------------------------------------------------

results = []

for k in range(3, 9):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20
    )

    labels = model.fit_predict(X)

    inertia = model.inertia_

    silhouette = silhouette_score(
        X,
        labels
    )

    results.append({
        "k": k,
        "inertia": inertia,
        "silhouette_score": silhouette
    })


model_scores = pd.DataFrame(results)

print("\n========================================")
print("K-MEANS MODEL COMPARISON")
print("========================================")

print(
    model_scores.round(4).to_string(index=False)
)

model_scores.to_csv(
    OUTPUT_MODEL,
    index=False
)


# ---------------------------------------------------------
# 6. CHOOSE FINAL K
# ---------------------------------------------------------
# We start with K = 5 to keep the Bengaluru demand
# segmentation easy to explain.
#
# IMPORTANT:
# K-Means discovers the locations; we are NOT using
# predefined geographic zones to create the clusters.
# ---------------------------------------------------------

K = 5

final_model = KMeans(
    n_clusters=K,
    random_state=42,
    n_init=20
)

orders["cluster"] = (
    final_model.fit_predict(X) + 1
)


# ---------------------------------------------------------
# 7. CLUSTER CENTERS
# ---------------------------------------------------------

cluster_centers = pd.DataFrame(
    final_model.cluster_centers_,
    columns=[
        "cluster_lat",
        "cluster_lon"
    ]
)

cluster_centers.insert(
    0,
    "cluster",
    range(1, K + 1)
)


# ---------------------------------------------------------
# 8. CLUSTER SUMMARY
# ---------------------------------------------------------

cluster_summary = (
    orders
    .groupby("cluster")
    .agg(
        total_orders=("Order_ID", "count"),
        avg_order_value=("Order_Value_INR", "mean"),
        avg_lat=("Customer_Lat", "mean"),
        avg_lon=("Customer_Lon", "mean")
    )
    .reset_index()
)

# Add K-Means center coordinates
cluster_summary = cluster_summary.merge(
    cluster_centers,
    on="cluster",
    how="left"
)

# Demand share
cluster_summary["demand_share_pct"] = (
    cluster_summary["total_orders"]
    / len(orders)
    * 100
)

# Sort from highest demand to lowest
cluster_summary = cluster_summary.sort_values(
    "total_orders",
    ascending=False
).reset_index(drop=True)


# ---------------------------------------------------------
# 9. DISPLAY FINAL RESULT
# ---------------------------------------------------------

print("\n========================================")
print("FINAL K-MEANS RESULTS")
print("========================================")

print("Chosen K:", K)

print("\nDemand Cluster Summary:")

print(
    cluster_summary.round(3).to_string(index=False)
)


# ---------------------------------------------------------
# 10. SAVE DATA WITH CLUSTERS
# ---------------------------------------------------------

orders.to_csv(
    OUTPUT_ORDERS,
    index=False
)

cluster_summary.to_csv(
    OUTPUT_SUMMARY,
    index=False
)


# ---------------------------------------------------------
# 11. SAVE CLUSTER CENTERS SEPARATELY
# ---------------------------------------------------------

cluster_centers.to_csv(
    "cluster_centers.csv",
    index=False
)


# ---------------------------------------------------------
# 12. FINAL FILE LIST
# ---------------------------------------------------------

print("\n========================================")
print("FILES CREATED")
print("========================================")

print(OUTPUT_ORDERS)
print(OUTPUT_SUMMARY)
print(OUTPUT_MODEL)
print("cluster_centers.csv")

print("\nDone.")
