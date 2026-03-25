# 🚗 BMW Global Sales Dashboard (2018–2025)

An interactive analytics dashboard built with **Plotly Dash** + **Pandas**.

---

## 📁 Project Structure

```
bmw_dashboard/
├── app.py                          ← Main Python / Dash application
├── bmw_global_sales_2018_2025.csv  ← Dataset (place here)
├── assets/
│   └── styles.css                  ← Custom CSS (auto-loaded by Dash)
└── README.md
```

---

## ⚡ Quick Start

### 1. Install dependencies
```bash
pip install dash plotly pandas
```

### 2. Place your CSV in the same folder as app.py
```
bmw_dashboard/
├── app.py
├── bmw_global_sales_2018_2025.csv   ← here
```

### 3. Run the app
```bash
cd bmw_dashboard
python app.py
```

### 4. Open in browser
```
http://127.0.0.1:8050
```

---

## 🔹 Features

### KPI Cards (dynamic)
| KPI | Description |
|-----|-------------|
| Total Records | Count of matched rows |
| Total Units Sold | Sum of Units_Sold (in millions) |
| Total Revenue | Sum of Revenue_EUR (in billions) |
| Avg Price | Mean of Avg_Price_EUR |
| Avg BEV Share | Mean EV adoption % |

### Charts
| # | Chart | Insight |
|---|-------|---------|
| 1 | Horizontal Stacked Bar | Region × Model unit breakdown |
| 2 | Multi-line trend | Monthly units over years |
| 3 | Donut Pie | Model market share |
| 4 | Histogram | Unit record distribution |
| 5 | Box Plot | Revenue spread & outliers by region |
| 6 | Bubble Scatter | Avg Price vs Revenue, sized by units |
| 7 | Heatmap | Pearson correlation matrix |
| 8 | Stacked Bar | Annual revenue by region |
| 9 | Line | BEV (EV) share trend by region |

### Filters (Left Sidebar)
| Filter | Type | Linked To |
|--------|------|-----------|
| Region | Multi-select | Updates Model options |
| Model | Multi-select | Depends on Region |
| Year | Range Slider | Updates Month options |
| Month | Multi-select | Depends on Year range |
| Reset | Button | Clears all filters |

---

## 🛠 Tech Stack
- **Dash** 2.x — Web framework
- **Plotly Express** — Charts
- **Pandas** — Data manipulation
- **CSS** — Custom layout & theming (no Bootstrap needed)

---

## 📊 Dataset Columns
| Column | Type | Description |
|--------|------|-------------|
| Year | int | 2018–2025 |
| Month | int | 1–12 |
| Region | category | Europe, China, USA, RestOfWorld |
| Model | category | 3 Series, 5 Series, X3, X5, X7, i4, iX, MINI |
| Units_Sold | int | Monthly units sold |
| Avg_Price_EUR | float | Average price in EUR |
| Revenue_EUR | float | Total revenue in EUR |
| BEV_Share | float | EV share (0.0–1.0) |
| Premium_Share | float | Premium share |
| GDP_Growth | float | GDP growth index |
| Fuel_Price_Index | float | Fuel price index |
