# 🛒 E-Commerce Sales Pipeline — Medallion Architecture

### A production-style ETL pipeline built on the Bronze → Silver → Gold data architecture, powering a modular Streamlit analytics dashboard.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" />
  <img src="https://img.shields.io/badge/Azure%20Data%20Lake-Gen2-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" />
</p>

---

## 📌 Overview

This project simulates a **real-world e-commerce data platform**, taking raw transactional data from a single CSV file all the way through to a fully interactive business intelligence dashboard — following the **Medallion (Bronze / Silver / Gold) Architecture** used widely across modern data engineering teams (Databricks, Azure, and Lakehouse-style systems).

The goal isn't just to clean data — it's to demonstrate an **end-to-end, production-minded data engineering workflow**: raw ingestion, validated cleaning, business-ready aggregation, and a decision-support dashboard, with data quality tracked at every stage.

---

## 🏗️ Architecture Flow

```
        ┌─────────────────────┐
        │   Kaggle CSV Data    │
        │ (Online Sales Data)  │
        └──────────┬───────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │  Azure Data Lake Gen2        │
        │  Bronze Folder (Cloud Raw)   │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │  🥉 BRONZE LAYER (SQLite)    │
        │  bronze_orders — 240 rows    │
        │  Raw, unmodified + timestamp │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │  🥈 SILVER LAYER (SQLite)    │
        │  silver_orders — 221 rows    │
        │  Cleaned, validated, typed   │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │  🥇 GOLD LAYER (SQLite)      │
        │  gold_summary — aggregated   │
        │  KPIs + performance tags     │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │  📊 Streamlit Dashboard      │
        │  Modular · Plotly · Themed   │
        └──────────┬───────────────────┘
                   │
                   ▼
        ┌─────────────────────────────┐
        │   💼 Business Decisions      │
        └─────────────────────────────┘
```

---

## 🥉🥈🥇 Medallion Layers — Bronze vs Silver vs Gold

| Aspect | 🥉 Bronze | 🥈 Silver | 🥇 Gold |
|---|---|---|---|
| **Purpose** | Raw ingestion | Cleaning & validation | Aggregation & KPIs |
| **Source** | Raw CSV | `bronze_orders` | `silver_orders` |
| **Row Count** | 240 | 221 | Aggregated summary |
| **Transformations** | None (raw copy) | Nulls filled, duplicates aggregated, types fixed, outliers removed | Grouped by dimensions, KPIs calculated |
| **Null Handling** | Not handled | Median (numeric) / Mode (categorical) | N/A |
| **Duplicates** | Not handled | Aggregated (summed/averaged) — not dropped | N/A |
| **Outliers** | Not handled | Removed using IQR method | N/A |
| **Timestamp Added** | `ingested_at` | `cleaned_at` | `aggregated_at` |
| **Table Name** | `bronze_orders` | `silver_orders` | `gold_summary` |
| **Consumer** | Silver layer | Gold layer | Dashboard / Business users |

---

## 📊 Data Quality Report

Data quality is measured and logged automatically at every pipeline run via `data_quality_report.py`.

| Metric | Value |
|---|---|
| 🥉 Bronze Rows (Raw) | 240 |
| 🥈 Silver Rows (Clean) | 221 |
| ❌ Rows Removed (Outliers via IQR) | 19 |
| ✅ Data Quality Pass Rate | **92.08%** |
| 📄 Report Output | `data_quality_report.txt` |

> Duplicate records were **not discarded** — they were intentionally aggregated (units summed, prices averaged, revenue summed) to preserve transactional integrity instead of silently losing data.

---

## 📁 Project Structure

```
ECOMMERCE_PROJECT/
│
├── dashboard/
│   └── dashboard_v1/
│       ├── assets/
│       │   ├── logo.png
│       │   └── style.css
│       │
│       ├── utils/
│       │   ├── charts.py
│       │   ├── database.py
│       │   ├── filters.py
│       │   ├── helpers.py
│       │   └── theme.py
│       │
│       ├── dashboard.py
│       └── README.md
│
├── raw_data/
│   └── Online Sales Data.csv
│
├── bronze_layer.py
├── data_quality_report.py
├── data_quality_report.txt
├── ecommerce.db
├── gold_layer.py
├── pipeline.py
├── silver_layer.py
└── test.py
```

### 📂 Folder Breakdown

| Path | Responsibility |
|---|---|
| `dashboard/dashboard_v1/` | Complete, self-contained Streamlit frontend |
| `dashboard/dashboard_v1/assets/` | Logo and custom CSS for dark theme styling |
| `dashboard/dashboard_v1/utils/charts.py` | All Plotly chart-building functions |
| `dashboard/dashboard_v1/utils/database.py` | SQLite connection handling and queries |
| `dashboard/dashboard_v1/utils/filters.py` | Sidebar filter logic (Region, Category, etc.) |
| `dashboard/dashboard_v1/utils/helpers.py` | Reusable helper/utility functions |
| `dashboard/dashboard_v1/utils/theme.py` | Dark theme and color configuration |
| `raw_data/` | Original Kaggle source CSV |
| `bronze_layer.py` | Raw data ingestion into SQLite |
| `silver_layer.py` | Cleaning, validation, deduplication |
| `gold_layer.py` | Aggregation and KPI generation |
| `pipeline.py` | Orchestrates all three layers in sequence |
| `data_quality_report.py` | Generates the data quality summary |
| `ecommerce.db` | SQLite database containing all three layers |

---

## 🧩 Why the Dashboard Lives in Its Own Folder

The dashboard is intentionally isolated inside `dashboard/dashboard_v1/` rather than sitting alongside the pipeline scripts. This mirrors how real data teams structure repositories:

- **Separation of concerns** — the ETL pipeline (data engineering) and the dashboard (data presentation) are independent systems that can be developed, tested, and deployed on their own timelines.
- **Versioning the dashboard independently** — the `_v1` suffix leaves room for `dashboard_v2`, `dashboard_v3`, etc. without ever touching pipeline code.
- **Reusability** — the same Gold-layer database could power multiple frontends (Streamlit today, Power BI tomorrow) without restructuring the pipeline.
- **Cleaner collaboration** — a data engineer working on `silver_layer.py` and a frontend-focused contributor working on `dashboard.py` never collide on files.
- **Production realism** — this is exactly how pipeline and BI-layer code is separated in Azure Data Factory + Power BI or Databricks + dashboarding setups.

---

## 📈 Dashboard Features

Built with **Streamlit + Plotly**, fully modularized across `utils/`, with a custom dark theme and branded logo.

**KPI Cards (top row):**
- 💰 Total Revenue
- 📦 Total Orders
- 📊 Units Sold
- 🧾 Average Order Value

**Sidebar Filters:**
- 🌍 Region
- 🏷️ Product Category
- 💳 Payment Method
- 📅 Month

**Visualizations:**
- 📊 Revenue by Product Category (bar chart)
- 📉 Revenue by Region (horizontal bar chart)
- 📈 Monthly Revenue Trend (line chart)
- 🥧 Payment Method Distribution (pie chart)
- 🏆 Top 10 Products by Revenue (bar chart)
- 🎯 Performance Tag Distribution (chart)
- 📋 Full Gold-layer data table (bottom, filterable)

---

## 🎯 Gold-Layer KPIs Explained

| KPI | Description |
|---|---|
| `total_revenue` | Sum of revenue for the grouped dimension |
| `total_units` | Sum of units sold |
| `order_count` | Number of orders in the group |
| `avg_unit_price` | Average unit price across orders |
| `min_price` / `max_price` | Price range within the group |
| `revenue_per_unit` | Total revenue divided by total units sold |
| `avg_order_value` | Average revenue generated per order |
| `revenue_contribution_%` | This group's share of total overall revenue |
| `performance_tag` | Categorical tag — **Low / Medium / High / Top** — based on revenue contribution |

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Data Processing | Pandas |
| Database | SQLite3 |
| Cloud Storage | Azure Data Lake Gen2 |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Architecture Diagram | draw.io |
| Version Control | GitHub |

---

## 🚀 How To Run

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/ecommerce-sales-pipeline.git
cd ecommerce-sales-pipeline
```

### 2️⃣ Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS / Linux
```

### 3️⃣ Install dependencies
```bash
pip install pandas streamlit plotly
```

### 4️⃣ Run the full pipeline (Bronze → Silver → Gold)
```bash
python pipeline.py
```

### 5️⃣ Generate the data quality report
```bash
python data_quality_report.py
```

### 6️⃣ Launch the dashboard
```bash
cd dashboard/dashboard_v1
streamlit run dashboard.py
```

---

## 🧠 Project Learnings

- Designing a Medallion Architecture end-to-end deepened my understanding of **why** raw data should never be modified in place — Bronze exists precisely to preserve an unaltered source of truth.
- Handling duplicates through **aggregation instead of deletion** taught me to think about data integrity from a business perspective, not just a "clean the DataFrame" perspective.
- Using the **IQR method** for outlier detection reinforced the importance of statistically justified cleaning decisions over arbitrary thresholds.
- Structuring the dashboard as a **separate, modular application** clarified how real teams decouple pipeline and presentation layers for scalability and maintainability.
- Writing an automated **data quality report** made me appreciate that a pipeline isn't "done" when it runs — it's done when its output is *trustworthy and measurable*.

---

## 🔭 What's Next

- 🔄 **Azure Data Factory** — for cloud-native orchestration of the pipeline
- ⏱️ **Apache Airflow** — for scheduling and dependency-based execution
- ⚡ **Databricks + PySpark** — to scale the pipeline to big data volumes
- 🗂️ **Delta Lake** — for data versioning and time travel
- 📊 **Power BI** — for enterprise-grade reporting on top of the Gold layer
- ✅ **Unit Tests** — for each pipeline layer (Bronze, Silver, Gold) to ensure reliability

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">Built with ☕ and a genuine curiosity for how data platforms are engineered.</p>