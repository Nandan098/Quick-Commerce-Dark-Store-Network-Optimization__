# Quick-Commerce Dark Store Network Analysis — Bengaluru Case Study

## STAR Method — Interview-Ready Project Documentation

This project was developed as a **supply-chain analytics case study** to understand where potential dark-store opportunity areas could exist in Bengaluru based on customer demand, geographic concentration, competitor coverage, capacity, and geographic accessibility.

> **Important:** This is an analytical case study and decision-support framework. It does not claim that a real dark store was opened or that the recommended areas are final commercial locations.

---

## 1. Project Story in STAR Format

### S — Situation

Quick-commerce businesses depend on dark stores to serve customers within a short delivery window. A poor store-location decision can create service gaps in high-demand areas, while opening a store in an area with low demand or strong competitor coverage may not be attractive.

For this case study, I used a customer-order dataset representing demand across Bengaluru and a competitor-location dataset containing actual store locations for Blinkit, Zepto, and Instamart. The business problem was to understand **where customer demand is concentrated, where competitor coverage is relatively lower, and whether shortlisted areas appear operationally feasible**.

### T — Task

My task was to build a data-driven framework that could:

1. Analyze customer demand patterns.
2. Identify geographic demand clusters.
3. Compare demand areas with competitor-store coverage.
4. Identify potential high-demand and relatively lower-competition opportunity areas.
5. Check whether local demand could theoretically be handled by a dark store.
6. Evaluate geographic accessibility of customers around shortlisted areas.
7. Present the results through an interactive map and business dashboard.

The objective was not to make a final real-world expansion decision, but to create a **decision-support analysis** that could narrow down areas for further investigation.

### A — Action

I divided the project into several stages.

#### Step 1 — Customer Order Data

I started with a customer-order dataset containing approximately 6,000 orders and fields such as:

- `Order_ID`
- `Customer_Lat`
- `Customer_Lon`
- `Order_Timestamp`
- `Order_Value_INR`
- `Order_Hour`
- `Order_Time_Str`

I first explored the data for missing values, duplicates, data types, descriptive statistics, order values, time patterns, and geographic spread.

#### Step 2 — Demand Analysis

I used **SQL and Python/Pandas** to analyze customer demand.

The analysis included:

- Order count by hour
- Total order value
- Average order value
- Overall order volume
- Geographic distribution of customer orders

This helped identify when customer demand was highest and provided a baseline for later operational analysis.

#### Step 3 — K-Means Geographic Clustering

I used **K-Means clustering** on customer latitude and longitude to identify geographic concentrations of orders.

I tested multiple values of K and compared the clustering using measures such as:

- Inertia
- Silhouette score

For this case study, I selected **K = 5** as a simple segmentation for the final analysis.

The purpose of clustering was to answer:

> **Where are customers geographically concentrated?**

The clusters were then used as an analytical layer rather than as actual predefined city zones.

#### Step 4 — Competitor Store Analysis

I used the available competitor-location dataset containing actual store locations for:

- Blinkit
- Zepto
- Instamart

For each geographic opportunity area, I calculated:

- Number of competitor stores within approximately 2 km
- Distance to the nearest competitor store

I used the **Haversine distance** calculation to estimate geographic distance between locations.

This helped answer:

> **Which demand areas have relatively lower competitor coverage?**

#### Step 5 — Opportunity Area Identification

Because high demand alone does not necessarily mean a good expansion opportunity, I combined demand and competition.

I created a simple screening framework:

- **High demand + lower competitor coverage → High Opportunity**
- **Medium/high demand + moderate competitor coverage → Medium Opportunity**
- **Other combinations → Low Opportunity**

I also created a transparent opportunity score using:

- 60% demand score
- 40% lower-competition score

This score is only a ranking/screening mechanism for the case study and is not an industry-standard location score.

#### Step 6 — Capacity Check

After identifying opportunity areas, I checked whether the local demand could theoretically be handled by a dark store.

For the case study, I used an assumed planning capacity of:

**1,200 orders per day per store**

The calculations were:

**Average Daily Local Demand**

`Local orders within 2 km / Number of analysis days`

**Stores Required**

`CEILING(Average Daily Local Demand / 1,200)`

**Capacity Utilization**

`Average Daily Local Demand / 1,200 × 100`

This assumption is only used for analytical planning. It should not be presented as a universal dark-store capacity benchmark.

#### Step 7 — Geographic Accessibility

I then analyzed how close customers were geographically to the shortlisted opportunity areas.

The measures included:

- Average customer distance
- Percentage of orders within 1 km
- Percentage of orders within 2 km
- Maximum customer distance

A 10-minute delivery target may be used as an **illustrative case-study service target**, but I did not directly convert geographic distance into delivery time.

A real implementation would require:

- Road-network travel time
- Traffic conditions
- Rider availability
- Store processing time
- Actual company SLA

Therefore, geographic distance was treated only as an **initial accessibility proxy**.

#### Step 8 — Visualization

I used **Streamlit and Folium** to create an interactive Bengaluru map.

The map shows:

- Individual customer-order pins
- K-Means clusters
- Cluster centers
- Blinkit stores
- Zepto stores
- Instamart stores

I also used **Power BI** to present the business findings through three analytical pages:

1. Demand Overview
2. Competition & Opportunity
3. Capacity & Accessibility

---

## 2. R — Result

The result of the project is a **decision-support framework for dark-store network analysis** rather than a real store-opening decision.

The analysis provides a structured way to:

- Understand customer demand patterns.
- Identify geographic concentrations of orders.
- Compare demand with competitor coverage.
- Shortlist areas with relatively high demand and lower competition.
- Estimate theoretical capacity requirements.
- Assess geographic accessibility.
- Present the findings through interactive dashboards.

A major insight from the demand analysis is that customer ordering activity is concentrated in specific periods, with the dataset showing **around 8 PM as a peak ordering period**.

The project also demonstrates that:

> **High customer demand alone is not enough to select a dark-store location.**

Demand needs to be considered together with competitor coverage, local capacity requirements, and geographic accessibility.

---

## 3. STAR Answer for an Amazon Interview

### 60–90 Second Version

> **Situation:** I worked on a quick-commerce dark-store network analysis case study for Bengaluru. The problem I wanted to solve was how to identify areas where customer demand was high but competitor coverage was relatively lower.
>
> **Task:** My task was to build a data-driven framework that could analyze demand, identify geographic clusters, compare competitor presence, and check whether shortlisted areas were operationally feasible.
>
> **Action:** I started with around 6,000 customer orders and analyzed demand using SQL and Python. I then applied K-Means clustering on customer latitude and longitude to identify geographic demand clusters. After that, I used the actual competitor-location data for Blinkit, Zepto and Instamart and calculated the number of competitor stores within a 2-kilometer radius and the distance to the nearest competitor. Based on demand and competition, I identified potential opportunity areas. I then compared local average daily demand with an assumed dark-store capacity of 1,200 orders per day and used geographic distance as an accessibility proxy. Finally, I presented the results through Streamlit and Power BI.
>
> **Result:** The final outcome was a decision-support framework that helped identify areas with relatively high demand and lower competitor coverage while also checking capacity and geographic accessibility. One key insight was that peak demand occurred around 8 PM, which is important for fulfillment planning. I also learned that a location decision should not be based on demand alone; competition and operational feasibility also matter.

---

## 4. 30-Second Version

> I built a Bengaluru quick-commerce dark-store analysis using Python, SQL, K-Means, Streamlit and Power BI. I analyzed around 6,000 customer orders, identified geographic demand clusters, compared them with actual Blinkit, Zepto and Instamart locations, and shortlisted high-demand areas with relatively lower competition. I then checked local demand against an assumed store capacity and evaluated geographic accessibility. The final output was an analytical decision-support framework rather than an actual store-opening recommendation.

---

## 5. Technical Architecture

```text
Customer Orders
      |
      v
Data Exploration
      |
      v
SQL Demand Analysis
      |
      v
K-Means Geographic Clustering
      |
      v
Small Geographic Demand Areas
      |
      v
Competitor Store Analysis
      |
      v
Demand + Competition
      |
      v
Opportunity Areas
      |
      +----------------------+
      |                      |
      v                      v
Capacity Check        Geographic Accessibility
      |                      |
      +----------+-----------+
                 |
                 v
        Power BI + Streamlit
```

---

## 6. Tech Stack

| Tool / Technology | Purpose |
|---|---|
| Python | Main analysis and modelling |
| Pandas | Data cleaning and transformation |
| NumPy | Numerical calculations |
| SQL | Demand and business analysis |
| Scikit-learn | K-Means clustering |
| Haversine distance | Geographic distance calculations |
| Folium | Interactive map |
| Streamlit | Interactive geographic application |
| Power BI | Business dashboards |
| Jupyter Notebook | Step-by-step analysis |
| GitHub | Project version control and presentation |

---

## 7. Repository Structure

```text
quick-commerce-dark-store-analysis/
│
├── README.md
│
├── data/
│   ├── customer_orders.csv
│   ├── Competitors.csv
│   └── README.md
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_sql_demand_analysis.sql
│   ├── 03_kmeans_clustering.ipynb
│   ├── 04_competitor_opportunity_analysis.ipynb
│   └── 05_capacity_accessibility_analysis.ipynb
│
├── src/
│   ├── kmeans_new_customer_orders.py
│   ├── opportunity_new_data.py
│   └── utils.py
│
├── outputs/
│   ├── customer_orders_with_clusters.csv
│   ├── demand_cluster_summary.csv
│   ├── kmeans_model_comparison.csv
│   ├── cluster_centers.csv
│   ├── opportunity_areas.csv
│   └── final_opportunity_sla_analysis.csv
│
├── streamlit/
│   ├── app_final.py
│   └── requirements.txt
│
├── powerbi/
│   └── dark_store_network_analysis.pbix
│
├── screenshots/
│   ├── streamlit_map.png
│   ├── demand_dashboard.png
│   ├── competition_opportunity_dashboard.png
│   └── capacity_accessibility_dashboard.png
│
├── docs/
│   ├── methodology.md
│   └── project_flow.png
│
└── .gitignore
```

---

## 8. Dataset Description

### Customer Orders

The customer-order dataset contains approximately 6,000 records.

Main fields:

```text
Order_ID
Customer_Lat
Customer_Lon
Order_Timestamp
Order_Value_INR
Order_Hour
Order_Time_Str
```

### Competitor Stores

The competitor dataset contains store-level location information.

Main fields:

```text
Store ID
Company
City
State
Latitude
Longitude
```

The analysis uses the Bengaluru records for competitor comparison.

---

## 9. Business Questions Answered

This project is designed around the following questions:

### Demand

**Where is customer demand concentrated?**

Answered using order analysis and K-Means clustering.

### Time

**When is demand highest?**

Answered using order-hour analysis.

### Competition

**Which demand areas have relatively lower competitor presence?**

Answered using competitor counts within 2 km and nearest competitor distance.

### Opportunity

**Which areas may deserve further investigation for dark-store expansion?**

Answered using demand and competitor coverage.

### Capacity

**Can the expected local demand theoretically be handled by one assumed store?**

Answered using average daily local demand and the 1,200-orders/day planning assumption.

### Accessibility

**Are customers geographically close to the opportunity area?**

Answered using average distance and percentage of customers within 1 km and 2 km.

---

## 10. Key Metrics

### Total Orders

Number of customer orders in the dataset.

### Average Order Value

Average value of customer orders.

### Total Order Value

Total monetary value represented by the analyzed orders.

### Competitors Within 2 km

Number of competitor stores located within approximately 2 km of an opportunity area.

### Nearest Competitor Distance

Geographic distance from an opportunity area to the closest competitor store.

### Average Daily Local Demand

Average number of customer orders per day within the local 2 km catchment.

### Stores Required

Estimated number of stores required under the 1,200-orders/day planning assumption.

### Capacity Utilization

Estimated local demand divided by assumed store capacity.

### Orders Within 1 km

Percentage of local customer orders located within 1 km of the opportunity area.

---

## 11. Methodology Details

### K-Means

Input features:

```text
Customer_Lat
Customer_Lon
```

The model was used to group customers by geographic proximity.

Multiple K values were tested before selecting K = 5 for the final simple segmentation.

### Competitor Distance

Geographic distance is calculated using the Haversine formula.

This allows the project to compare the locations of customer demand areas with competitor stores.

### Opportunity Score

The screening score is:

```text
Opportunity Score
= 60% Demand Score
+ 40% Lower-Competition Score
```

The score is intended to rank areas for further investigation.

It is not a universal industry formula.

---

## 12. Capacity Assumption

For this case study:

```text
Assumed store capacity = 1,200 orders/day/store
```

This is a planning assumption used only to demonstrate capacity screening.

It should not be presented in an interview as a universal industry benchmark.

---

## 13. SLA and Accessibility Limitation

The project does **not** claim that a particular geographic distance guarantees a 10-minute delivery.

The 10-minute target is only an illustrative case-study service target.

Actual delivery performance depends on:

- Road-network distance
- Traffic
- Rider availability
- Store processing time
- Order batching
- Company operating procedures
- Actual customer SLA

Therefore, the project uses geographic distance only as an **initial accessibility proxy**.

---

## 14. What I Would Improve in a Real Deployment

If this analysis were used in a real business setting, I would add:

- Actual historical customer-order data
- Road-network travel time
- Real-time traffic data
- Rider availability
- Actual company SLA
- Store processing time
- Historical delivery performance
- Store operating hours
- Demand seasonality
- Day-of-week demand
- Capacity by SKU/category
- More detailed competitor service-area information

These additions would make the analysis closer to a production-grade location-planning system.

---

## 15. Limitations

This project has several limitations:

1. The customer-order dataset is a case-study dataset rather than proprietary company order data.
2. Competitor analysis uses the available competitor-location dataset.
3. Store capacity is based on an analytical assumption.
4. Geographic distance is not equal to delivery time.
5. No road-network or traffic data is used.
6. The opportunity score is a transparent screening score rather than a validated commercial optimization model.
7. Final store selection would require additional operational and business constraints.

---

## 16. Interview Deep-Dive Questions

### Why did you use K-Means?

> I used K-Means because the problem was primarily about identifying geographic concentrations of customers. Since the input variables were customer latitude and longitude, clustering provided a simple way to segment the demand geographically.

### Why not simply choose the highest-demand area?

> Because high demand does not automatically mean a good expansion opportunity. There may already be strong competitor coverage in that area. So I combined demand with competitor presence.

### Why did you choose K = 5?

> I tested multiple K values and compared clustering quality using metrics such as inertia and silhouette score. I selected K = 5 because it provided a simple and interpretable segmentation for this case study.

### Why 2 km?

> I used 2 km as a geographic screening radius for comparing demand and competitor presence. It is a case-study assumption, not a universal operating radius. In a real system, I would validate it against actual road travel time and the company's service-area data.

### Why 1,200 orders per day?

> I used 1,200 orders per day as a planning assumption for the capacity calculation. It is not meant to represent a universal industry benchmark. In a real implementation, capacity would come from actual store throughput and operating constraints.

### How did you measure SLA?

> I did not directly measure actual SLA because I did not have road-network travel time, traffic, rider availability or store processing-time data. Instead, I used geographic distance as an accessibility proxy. The 10-minute service target is illustrative only.

### Did you actually optimize the dark-store network?

> I would describe it as a decision-support analysis rather than claiming a full production optimization. The project screens and ranks areas using demand, competition, capacity and accessibility. A production optimization model would need additional constraints and validated business data.

### Is this a real company deployment?

> No. It is a Bengaluru case study built to demonstrate how supply-chain and analytics methods can support dark-store network decisions.

### What was your biggest learning?

> My biggest learning was that supply-chain decisions usually require balancing multiple factors. A location with high demand may still not be attractive if competitor coverage is high or the local operational capacity is not sufficient.

---

## 17. Leadership Principle Mapping for Amazon

### Dive Deep

I used detailed customer-order, geographic and competitor-location analysis rather than relying only on total demand.

### Customer Obsession

The analysis starts from customer demand and geographic accessibility, because the purpose of a dark-store network is to serve customers efficiently.

### Ownership

I structured the project end-to-end, from data exploration and modelling to dashboards and interpretation.

### Learn and Be Curious

I combined supply-chain concepts with Python, SQL, machine learning, geographic analysis, Streamlit and Power BI.

### Invent and Simplify

I created a simple demand + competition screening framework instead of building an unnecessarily complicated optimization model.

### Deliver Results

The final project produces usable outputs, opportunity rankings, capacity checks, and dashboards that communicate the analysis clearly.

---

## 18. GitHub Presentation

For a recruiter or interviewer, the recommended viewing order is:

```text
README.md
   ↓
01_data_exploration.ipynb
   ↓
03_kmeans_clustering.ipynb
   ↓
04_competitor_opportunity_analysis.ipynb
   ↓
05_capacity_accessibility_analysis.ipynb
   ↓
Streamlit Application
   ↓
Power BI Dashboard
```

The README should communicate the business problem before the technical implementation.

---

## 19. Final Project Statement

> **This project is a supply-chain analytics case study that uses customer-demand analysis, K-Means geographic clustering, competitor-location analysis, capacity screening and geographic accessibility analysis to identify potential dark-store opportunity areas in Bengaluru. Python and SQL were used for analysis, Streamlit was used for interactive geographic visualization, and Power BI was used to communicate the business findings.**

---

## 20. One-Line Resume Explanation

> **Developed a Bengaluru quick-commerce dark-store decision-support analysis using SQL, Python, K-Means and competitor-location analytics to identify high-demand, relatively lower-competition opportunity areas and evaluate capacity and geographic accessibility.**
