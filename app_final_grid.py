
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Bengaluru Dark Store Map",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp { background:#0d1016; }
section[data-testid="stSidebar"] { background:#191c25; }
.title { font-size:30px; font-weight:700; color:white; }
.subtitle { color:#9ea6b5; font-size:14px; margin-bottom:15px; }
.kpi { background:#181c25; border:1px solid #303644;
       border-radius:9px; padding:9px; text-align:center; }
.kpi-label { color:#929aaa; font-size:12px; }
.kpi-value { color:white; font-size:21px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

ORDERS_FILE = r"outputs\customer_orders_with_clusters.csv"
COMPETITOR_FILE = r"data\Competitors.csv"

@st.cache_data
def load_data():
    orders = pd.read_csv(ORDERS_FILE)
    competitors = pd.read_csv(COMPETITOR_FILE)

    city = competitors["City"].astype(str).str.strip().str.lower()
    competitors = competitors[
        city.isin(["bengaluru", "bangalore"])
    ].copy()

    return orders, competitors

try:
    orders, competitors = load_data()
except FileNotFoundError as e:
    st.error(
        f"Missing file: {e.filename}. Keep app.py, "
        "customer_orders_with_clusters.csv and Competitors.csv "
        "in the same folder."
    )
    st.stop()

st.markdown(
    '<div class="title">📦 Bengaluru Dark Store Network Optimization</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Customer Orders • K-Means Clusters • Competitor Dark Stores'
    '</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------

st.sidebar.markdown("## Map Layers")

show_orders = st.sidebar.checkbox(
    "Customer Orders",
    value=True
)

show_clusters = st.sidebar.checkbox(
    "K-Means Clusters",
    value=True
)

show_competitors = st.sidebar.checkbox(
    "Competitor Dark Stores",
    value=True
)

st.sidebar.markdown("### Competitor Dark Stores")

show_blinkit = st.sidebar.checkbox(
    "Blinkit",
    value=True,
    disabled=not show_competitors
)

show_zepto = st.sidebar.checkbox(
    "Zepto",
    value=True,
    disabled=not show_competitors
)

show_instamart = st.sidebar.checkbox(
    "Instamart",
    value=True,
    disabled=not show_competitors
)

# ------------------------------------------------------------
# CLUSTER COLORS
# ------------------------------------------------------------

palette = [
    "#ff4b5c", "#ffd43b", "#37d67a", "#5b8cff",
    "#c77dff", "#ff922b", "#20c997", "#f06595"
]

clusters = sorted(
    orders["cluster"].dropna().astype(int).unique()
)

cluster_colors = {
    c: palette[i % len(palette)]
    for i, c in enumerate(clusters)
}

# ------------------------------------------------------------
# MAP
# ------------------------------------------------------------

m = folium.Map(
    location=[
        orders["Customer_Lat"].mean(),
        orders["Customer_Lon"].mean()
    ],
    zoom_start=11,
    tiles="CartoDB dark_matter",
    control_scale=True
)

# ------------------------------------------------------------
# CUSTOMER ORDERS: ONE PIN PER ORDER
# ------------------------------------------------------------

if show_orders:

    customer_layer = folium.FeatureGroup(
        name="Customer Orders",
        show=True
    )

    for _, row in orders.iterrows():

        cluster = int(row["cluster"])

        if show_clusters:
            pin_color = cluster_colors[cluster]
        else:
            pin_color = "#ff5a69"

        folium.CircleMarker(
            location=[
                float(row["Customer_Lat"]),
                float(row["Customer_Lon"])
            ],
            radius=4,
            color="#ffffff",
            weight=1,
            fill=True,
            fill_color=pin_color,
            fill_opacity=0.90,
            tooltip=f"Order {row['Order_ID']} | Cluster {cluster}",
            popup=(
                f"<b>Customer Order</b><br>"
                f"Order ID: {row['Order_ID']}<br>"
                f"Cluster: {cluster}<br>"
                f"Order Value: ₹{row['Order_Value_INR']:.0f}<br>"
                f"Order Hour: {int(row['Order_Hour'])}"
            )
        ).add_to(customer_layer)

    customer_layer.add_to(m)

# ------------------------------------------------------------
# K-MEANS CLUSTER CENTERS
# ------------------------------------------------------------

if show_clusters:

    center_layer = folium.FeatureGroup(
        name="K-Means Cluster Centers",
        show=True
    )

    centers = (
        orders.groupby("cluster")
        .agg(
            center_lat=("Customer_Lat", "mean"),
            center_lon=("Customer_Lon", "mean"),
            order_count=("Order_ID", "count")
        )
        .reset_index()
    )

    for _, row in centers.iterrows():

        cluster = int(row["cluster"])

        folium.Marker(
            location=[
                float(row["center_lat"]),
                float(row["center_lon"])
            ],
            tooltip=(
                f"Cluster {cluster} | "
                f"{int(row['order_count']):,} orders"
            ),
            icon=folium.Icon(
                color="green",
                icon="info-sign"
            ),
            popup=(
                f"<b>K-Means Cluster {cluster}</b><br>"
                f"Orders: {int(row['order_count']):,}<br>"
                f"Center: {row['center_lat']:.4f}, "
                f"{row['center_lon']:.4f}"
            )
        ).add_to(center_layer)

    center_layer.add_to(m)

# ------------------------------------------------------------
# GRID IN EACH K-MEANS CLUSTER (~1 KM)
# ------------------------------------------------------------

if show_clusters:
    grid_layer = folium.FeatureGroup(
        name="Cluster Grid (~1 km)",
        show=True
    )

    GRID_SIZE = 0.009  # approximately 1 km

    grid_orders = orders.dropna(
        subset=["Customer_Lat", "Customer_Lon", "cluster"]
    ).copy()

    lat_min = grid_orders["Customer_Lat"].min()
    lon_min = grid_orders["Customer_Lon"].min()

    grid_orders["grid_lat"] = (
        (grid_orders["Customer_Lat"] - lat_min) / GRID_SIZE
    ).astype(int)

    grid_orders["grid_lon"] = (
        (grid_orders["Customer_Lon"] - lon_min) / GRID_SIZE
    ).astype(int)

    grid_cells = (
        grid_orders.groupby(
            ["cluster", "grid_lat", "grid_lon"],
            as_index=False
        )
        .agg(order_count=("Order_ID", "count"))
    )

    for _, cell in grid_cells.iterrows():
        cluster = int(cell["cluster"])
        color = cluster_colors[cluster]

        south = lat_min + int(cell["grid_lat"]) * GRID_SIZE
        west = lon_min + int(cell["grid_lon"]) * GRID_SIZE
        north = south + GRID_SIZE
        east = west + GRID_SIZE

        folium.Rectangle(
            bounds=[
                [south, west],
                [north, east]
            ],
            color=color,
            weight=1,
            opacity=0.65,
            fill=True,
            fill_color=color,
            fill_opacity=0.06,
            tooltip=(
                f"Cluster {cluster} | "
                f"{int(cell['order_count']):,} orders"
            )
        ).add_to(grid_layer)

    grid_layer.add_to(m)

# ------------------------------------------------------------
# COMPETITOR DARK STORES
# ------------------------------------------------------------

if show_competitors:

    competitor_layer = folium.FeatureGroup(
        name="Competitor Dark Stores",
        show=True
    )

    selected_companies = []

    if show_blinkit:
        selected_companies.append("Blinkit")
    if show_zepto:
        selected_companies.append("Zepto")
    if show_instamart:
        selected_companies.append("Instamart")

    competitor_view = competitors[
        competitors["Company"].astype(str).str.strip().isin(
            selected_companies
        )
    ].copy()

    for _, row in competitor_view.iterrows():

        company = str(row["Company"]).strip()

        folium.CircleMarker(
            location=[
                float(row["Latitude"]),
                float(row["Longitude"])
            ],
            radius=5,
            color="#ffffff",
            weight=1,
            fill=True,
            fill_color="#ff4b4b",
            fill_opacity=0.95,
            tooltip=f"{company} | {row['Store ID']}",
            popup=(
                f"<b>Competitor Dark Store</b><br>"
                f"Company: {company}<br>"
                f"Store ID: {row['Store ID']}<br>"
                f"City: {row['City']}"
            )
        ).add_to(competitor_layer)

    competitor_layer.add_to(m)

# ------------------------------------------------------------
# LEGEND
# ------------------------------------------------------------

legend = """
<div style="
position:fixed;
bottom:25px;
left:25px;
z-index:9999;
background:rgba(20,22,28,0.94);
padding:10px 12px;
border-radius:7px;
border:1px solid #353a46;
color:white;
font-size:12px;
min-width:135px;">
<b>Map Legend</b><br>
"""

for c in clusters:
    legend += (
        f'<span style="color:{cluster_colors[c]};'
        f'font-size:18px;">●</span> Cluster {c}<br>'
    )

legend += (
    '<span style="color:#ff4b4b;font-size:18px;">●</span> '
    'Competitor Store'
)

legend += "</div>"

m.get_root().html.add_child(
    folium.Element(legend)
)

folium.LayerControl(
    collapsed=False,
    position="topright"
).add_to(m)

# ------------------------------------------------------------
# KPIs
# ------------------------------------------------------------

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">Customer Orders</div>'
        f'<div class="kpi-value">{len(orders):,}</div></div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">K-Means Clusters</div>'
        f'<div class="kpi-value">{len(clusters)}</div></div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f'<div class="kpi"><div class="kpi-label">Competitor Stores</div>'
        f'<div class="kpi-value">{len(competitors):,}</div></div>',
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# MAP
# ------------------------------------------------------------

st.markdown("### Bengaluru Customer Order Map")

st_folium(
    m,
    height=740,
    width=None,
    returned_objects=[]
)

st.caption(
    "Each customer order is displayed as an individual pin. "
    "When K-Means Clusters is enabled, pin color represents "
    "the assigned cluster. Competitor stores are displayed as "
    "separate red pins."
)
