# Supply Chain Routing Efficiency & Anomaly Detection Pipeline

## 🚀 Project Overview
This project delivers an end-to-end data engineering and analytics pipeline designed to identify operational waste and routing anomalies in logistics networks. Processing a dataset of **50,000 global delivery orders**, the pipeline calculates structural inefficiencies by comparing actual delivery routes against straight-line geodetic distances, dynamically cleans backend anomalies, and serves the refined data to an interactive executive dashboard.

---

## 🛠️ Tech Stack & Architecture
* **Data Processing & Engineering:** Python (`Pandas`, `NumPy`, `Geopy`)
* **Storage Engine:** PostgreSQL
* **Business Intelligence & Visualization:** Power BI

---

## ⚙️ Core Pipeline Features

### 1. Geospatial Feature Engineering
* Calculated precise distance metrics across coordinate profiles ($Latitude$/$Longitude$) using geodetic tracking formulas.
* Established a **Distance Delta** metric ($Route\ Distance - Straight\ Line\ Distance$) to serve as an automated anomaly flag for identifying highly inefficient delivery routes.

### 2. Defensive Data Cleaning
* Engineered an automated backend filtering layer that catches and isolates database traps—such as unassigned orders (null `hub_id` values) or corrupted metrics (negative distances/weights).
* Safely handled floating-point precision constraints by maintaining raw, unrounded coordinates through database storage to prevent compounding truncation errors.

### 3. Interactive Executive Dashboard
* Designed a high-density Power BI map visual tracking regional logistics footprints.
* Implemented conditional formatting gradients based on the engineered *Distance Delta* metric, instantly highlighting underperforming fulfillment hubs.
* Built dynamic slicing features allowing stakeholder deep-dives into individual hub performance metrics and delivery volume distribution.

---

## 📈 Impact & Business Value
* **Proactive Waste Tracking:** Replaces manual auditing with an automated system that surfaces routing outliers instantly.
* **Data Integrity:** Ensures frontend visualizations are backed by mathematically precise calculations, filtering out dirty database entries before they corrupt corporate reporting metrics.
