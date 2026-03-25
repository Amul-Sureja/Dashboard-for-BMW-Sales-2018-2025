# 🚗 BMW Global Sales Dashboard (2018 – 2025)

> **An interactive analytics dashboard built with Python · Dash · Plotly · Pandas**

---

## 📸 Dashboard Preview

> **Default view — no filters applied. All 3,072 records visible.**

![BMW Global Sales Dashboard](assets/dashboard_preview.png)

*The screenshot above shows the full dashboard on load: 5 KPI cards at the top, Sales Overview charts (Region bar + Monthly trend), Distribution & Spread section (Pie, Histogram, Box Plot), and more sections below.*

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [Dataset Reference](#4-dataset-reference)
5. [Quick Start — Step by Step](#5-quick-start--step-by-step)
6. [Dashboard Layout](#6-dashboard-layout)
7. [KPI Cards](#7-kpi-cards)
8. [Filters — How They Work](#8-filters--how-they-work)
9. [Charts Reference](#9-charts-reference)
10. [Callback Architecture](#10-callback-architecture)
11. [CSS Theming & Styling](#11-css-theming--styling)
12. [Code Walkthrough — app.py](#12-code-walkthrough--apppy)
13. [Common Errors & Fixes](#13-common-errors--fixes)
14. [How to Extend the Dashboard](#14-how-to-extend-the-dashboard)
15. [Glossary](#15-glossary)

---

## 1. Project Overview

This dashboard provides an **end-to-end interactive view** of BMW's global vehicle sales data spanning **2018 to 2025**. It covers four key regions, eight vehicle models, and eleven data dimensions — including units sold, revenue, EV adoption, pricing, and macro-economic indicators.

### ✅ What You Can Do

| Action | How |
|--------|-----|
| Compare region & model sales | Region-wise stacked bar chart |
| Spot seasonal trends | Monthly line trend filtered by year |
| Track EV adoption growth | BEV Share trend by region |
| Detect revenue outliers | Box plot per region |
| Understand variable relationships | Correlation heatmap |
| Explore any data slice | Combined sidebar filters + Reset button |

### 📊 Dashboard at a Glance (Default View — No Filters)

When you first open the dashboard **with no filters applied**, you see:

| KPI Card | Value |
|----------|-------|
| Total Records | **3,072** |
| Total Units Sold | **24.52M** |
| Total Revenue | **€1,571.02B** |
| Avg Price (EUR) | **€63,855** |
| Avg BEV Share | **10.8%** |

> These numbers update dynamically whenever you apply any filter.

---

## 2. Tech Stack

| Library | Version | Role |
|---------|---------|------|
| `dash` | 2.x | Web framework — layout, routing, callbacks |
| `plotly` | 5.x | Interactive chart engine |
| `plotly.express` | included | High-level chart API (bar, line, pie, scatter…) |
| `plotly.graph_objects` | included | Low-level API — used for Heatmap |
| `pandas` | 1.5+ | Data loading, cleaning, filtering, aggregation |
| `CSS3` | — | Custom sidebar + card layout (no Bootstrap) |

> 💡 **No JavaScript required.** Dash handles all frontend–backend communication through its reactive callback system.

---

## 3. Project Structure

```
bmw_dashboard/
│
├── app.py                              ← All Python logic — layout + callbacks
│
├── bmw_global_sales_2018_2025.csv      ← Dataset (must sit next to app.py)
│
├── assets/
│   ├── styles.css                      ← Custom CSS (auto-loaded by Dash)
│   └── dashboard_preview.png          ← Dashboard screenshot (used in README)
│
└── README.md                           ← This file
```

> **📌 Key rule:** Dash automatically serves every file inside `assets/`.  
> Do **not** import or link `styles.css` manually — just keep it in that folder.

---

## 4. Dataset Reference

**File:** `bmw_global_sales_2018_2025.csv`  
**Rows:** 3,073 records  
**Granularity:** One row per `Region × Model × Year × Month` combination

### Column Definitions

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `Year` | `int` | 2021 | Calendar year |
| `Month` | `int` | 6 | Month number (1 = Jan, 12 = Dec) |
| `Region` | `category` | Europe | Sales region |
| `Model` | `category` | X5 | BMW vehicle model |
| `Units_Sold` | `int` | 8,420 | Vehicles sold that month |
| `Avg_Price_EUR` | `float` | 68,500 | Average sale price in Euros |
| `Revenue_EUR` | `float` | 576,770,000 | Total revenue = Units × Avg Price |
| `BEV_Share` | `float` | 0.18 | EV share (0.18 = 18%) |
| `Premium_Share` | `float` | 0.21 | Premium variant share |
| `GDP_Growth` | `float` | 3.4 | Regional GDP growth rate |
| `Fuel_Price_Index` | `float` | 1.25 | Indexed fuel price (1.0 = baseline) |

### Vehicle Models

| Model | Segment | Powertrain |
|-------|---------|-----------|
| 3 Series | Compact executive sedan | ICE / Hybrid |
| 5 Series | Mid-size executive sedan | ICE / Hybrid |
| X3 | Compact SUV | ICE / Hybrid |
| X5 | Mid-size SUV | ICE / PHEV |
| X7 | Full-size luxury SUV | ICE |
| i4 | Compact electric sedan | ⚡ Full BEV |
| iX | Mid-size electric SUV | ⚡ Full BEV |
| MINI | Subcompact hatchback | ICE / BEV |

### Regions

| Code | Markets Included |
|------|-----------------|
| `Europe` | Germany, UK, France, Italy + rest of Europe |
| `China` | Mainland China |
| `USA` | United States of America |
| `RestOfWorld` | APAC, Middle East, Africa, Latin America |

---

## 5. Quick Start — Step by Step

### Step 1 — Install Python
Download Python 3.8 or newer → [python.org](https://python.org)

```bash
python --version
# Python 3.8.x or higher ✓
```

### Step 2 — Install dependencies

```bash
pip install dash plotly pandas
```

### Step 3 — Arrange your project folder

```
bmw_dashboard/
├── app.py
├── bmw_global_sales_2018_2025.csv   ← must be here
├── assets/
│   └── styles.css
```

> ⚠️ If the CSV is in a different location, update **line 16** of `app.py`:
> ```python
> df_raw = pd.read_csv("your/path/to/file.csv")
> ```

### Step 4 — Run the app

```bash
cd bmw_dashboard
python app.py
```

Terminal output:
```
=======================================================
  BMW Global Sales Dashboard
  Open browser → http://127.0.0.1:8050
=======================================================
```

### Step 5 — Open in browser

```
http://127.0.0.1:8050
```

The dashboard loads with **all 3,072 records** visible (as shown in the screenshot above).

### Step 6 — Stop the server

```bash
Ctrl + C
```

---

## 6. Dashboard Layout

```
┌────────────────────────────────────────────────────────────────────────┐
│                          Dashboard Wrapper                             │
│                                                                        │
│  ┌─────────────────┐  ┌──────────────────────────────────────────────┐│
│  │                 │  │  BMW Global Sales Analytics  [3,072 matched] ││
│  │    SIDEBAR      │  ├──────────────────────────────────────────────┤│
│  │    290 px       │  │  📋 3,072  🚗 24.52M  💶 €1,571B  🏷 €63,855  ⚡10.8% ││
│  │                 │  ├──────────────────────────────────────────────┤│
│  │  🌍 Region      │  │  SALES OVERVIEW                              ││
│  │  🚗 Model       │  │  ┌─────────────────┐  ┌──────────────────┐  ││
│  │  📅 Year Range  │  │  │  Region Bar     │  │  Monthly Trend   │  ││
│  │  🗓️ Month      │  │  └─────────────────┘  └──────────────────┘  ││
│  │                 │  ├──────────────────────────────────────────────┤│
│  │  ↺ Reset        │  │  DISTRIBUTION & SPREAD                      ││
│  │                 │  │  ┌───────┐  ┌───────────┐  ┌────────────┐  ││
│  │  [All data]     │  │  │  Pie  │  │ Histogram │  │  Box Plot  │  ││
│  └─────────────────┘  │  └───────┘  └───────────┘  └────────────┘  ││
│                       ├──────────────────────────────────────────────┤│
│                       │  RELATIONSHIPS & CORRELATIONS                ││
│                       │  ┌────────────────────────┐  ┌───────────┐  ││
│                       │  │  Scatter Plot          │  │  Heatmap  │  ││
│                       │  └────────────────────────┘  └───────────┘  ││
│                       ├──────────────────────────────────────────────┤│
│                       │  REVENUE & EV INSIGHTS                      ││
│                       │  ┌──────────────────────┐  ┌────────────┐  ││
│                       │  │  Stacked Revenue Bar  │  │ BEV Trend  │  ││
│                       │  └──────────────────────┘  └────────────┘  ││
│                       └──────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────┘
```

---

## 7. KPI Cards

Five metric tiles sit at the top of the main area and **update instantly** on every filter change.

| # | Icon | Label | Formula | Unit |
|---|------|-------|---------|------|
| 1 | 📋 | Total Records | `len(filtered_df)` | Count |
| 2 | 🚗 | Total Units Sold | `sum(Units_Sold)` | Millions (M) |
| 3 | 💶 | Total Revenue | `sum(Revenue_EUR)` | Billions € (B) |
| 4 | 🏷️ | Avg Price (EUR) | `mean(Avg_Price_EUR)` | Euros (€) |
| 5 | ⚡ | Avg BEV Share | `mean(BEV_Share) × 100` | Percent (%) |

### Card colour accent bars

| Colour | Cards |
|--------|-------|
| 🔵 Blue | Total Records, Avg BEV Share |
| 🟢 Green | Total Units Sold |
| 🟠 Amber | Total Revenue |
| 🟣 Purple | Avg Price |

---

## 8. Filters — How They Work

All four filters sit in the **left sidebar** and work together — every chart and KPI reflects the combined state of all active filters simultaneously.

### Filter Dependency Map

```
Region selected
    └──► Model dropdown options narrow to matched region(s)

Year range moved
    └──► Month dropdown options narrow to matched year(s)

Any filter changes
    └──► All 9 charts + 5 KPI cards update instantly
```

### Filter Details

| Filter | Component ID | Type | Default | Linked To |
|--------|-------------|------|---------|-----------|
| Region | `filter-region` | Multi-select dropdown | All regions | Updates Model options |
| Model | `filter-model` | Multi-select dropdown | All models | Depends on Region |
| Year Range | `filter-year` | Range slider (2018–2025) | Full range | Updates Month options |
| Month | `filter-month` | Multi-select dropdown | All months | Depends on Year range |
| Reset | `btn-reset` | Button | — | Clears all four filters |

### Active Filter Pills
Below the Reset button, **blue pill badges** show which filters are currently active.  
When nothing is selected they show: `All data`

---

## 9. Charts Reference

### 📊 Section 1 — Sales Overview

#### Chart 1 · Region-Wise Units Sold (Horizontal Stacked Bar)
- **ID:** `chart-bar-region`
- X-axis → Units Sold | Y-axis → Region | Colour → Model
- Each bar is split by model so you can see both region totals and model breakdown at once
- Insight: *Compare how much each region contributes and which models lead within it*

#### Chart 2 · Monthly Sales Trend (Multi-Line)
- **ID:** `chart-line-trend`
- X-axis → Year-Month period | Y-axis → Total units sold | Colour → Year
- Each year becomes a separate line, making year-over-year comparison easy
- Insight: *Spot seasonal peaks and compare years side by side*

---

### 📊 Section 2 — Distribution & Spread

#### Chart 3 · Model Market Share (Donut Pie)
- **ID:** `chart-pie-model`
- Segments → Models | Values → Total `Units_Sold` per model
- Hole in the centre shows total units cleanly
- Insight: *See which models dominate the selected market*

#### Chart 4 · Units Sold Distribution (Histogram)
- **ID:** `chart-hist-units`
- X-axis → Units Sold per row | Y-axis → Frequency | Bins → 40
- Plots raw values — no aggregation — to reveal the true distribution
- Insight: *Is the distribution normal, right-skewed, or bimodal?*

#### Chart 5 · Revenue Box Plot
- **ID:** `chart-box-revenue`
- X-axis → Region | Y-axis → Revenue (EUR) per record
- Shows min / Q1 / Median / Q3 / Max + outlier dots + mean line
- Insight: *Find regions with unusually high or low revenue months*

---

### 📊 Section 3 — Relationships & Correlations

#### Chart 6 · Avg Price vs Revenue (Bubble Scatter)
- **ID:** `chart-scatter`
- X → Avg Price (EUR) | Y → Revenue (EUR) | Size → Units Sold | Colour → Region
- Hover reveals Model, Year, Month
- Samples max 2,000 rows for performance on large selections
- Insight: *Do higher-priced models always generate more revenue?*

#### Chart 7 · Correlation Heatmap
- **ID:** `chart-heatmap`
- Variables: `Units_Sold`, `Avg_Price_EUR`, `Revenue_EUR`, `BEV_Share`, `GDP_Growth`, `Fuel_Price_Index`
- Colour scale: RdBu — 🔴 strong negative · ⚪ none · 🔵 strong positive
- Values: Pearson r rounded to 2 decimal places
- Insight: *Which variables move together? Does GDP growth affect sales volumes?*

---

### 📊 Section 4 — Revenue & EV Insights

#### Chart 8 · Annual Revenue by Region (Stacked Bar)
- **ID:** `chart-revenue-stacked`
- X-axis → Year | Y-axis → Revenue (€B) | Colour segments → Region
- Insight: *Track revenue growth year-over-year and see regional contributions*

#### Chart 9 · BEV Share Trend by Region (Multi-Line)
- **ID:** `chart-bev-trend`
- X-axis → Year | Y-axis → Avg BEV Share (%) | Colour → Region
- Insight: *Which markets are leading EV adoption? How fast is it growing?*

---

## 10. Callback Architecture

```
TRIGGER (Input)               →    EFFECT (Output)
──────────────────────────────────────────────────────────────────
btn-reset click               →    Clear: region, model, year, month

filter-region changes         →    Rebuild model dropdown options
filter-year changes           →    Rebuild month dropdown options

Any of the 4 filters change   →    active-filter-info  (pills)
                              →    record-count-badge  (header)
                              →    kpi-section         (5 KPI cards)
                              →    chart-bar-region
                              →    chart-line-trend
                              →    chart-pie-model
                              →    chart-hist-units
                              →    chart-box-revenue
                              →    chart-scatter
                              →    chart-heatmap
                              →    chart-revenue-stacked
                              →    chart-bev-trend
```

### The `apply_filters()` helper

Every chart and KPI callback passes through **one shared function** to guarantee identical filtering:

```python
def apply_filters(regions, models, year_range, months):
    d = df_raw.copy()
    if regions:
        d = d[d["Region"].isin(regions)]
    if models:
        d = d[d["Model"].isin(models)]
    if year_range:
        d = d[d["Year"].between(year_range[0], year_range[1])]
    if months:
        d = d[d["Month"].isin(months)]
    return d
```

---

## 11. CSS Theming & Styling

All design tokens are defined as CSS variables at the top of `assets/styles.css`:

```css
:root {
  --bmw-blue:   #1C69D4;   /* Primary blue — buttons, sliders, highlights */
  --bmw-dark:   #0D1B2A;   /* Sidebar background */
  --bmw-mid:    #1A2E44;   /* Dropdown menu panel */
  --bmw-light:  #F4F7FB;   /* Page background */
  --bmw-card:   #FFFFFF;   /* Chart / KPI card background */
  --bmw-border: #DDE3EC;   /* Card and input borders */
  --bmw-text:   #1E2A38;   /* Primary text */
  --bmw-muted:  #6B7A8D;   /* Label / subtitle text */
  --bmw-accent: #E8931A;   /* Amber — Revenue card */
  --bmw-green:  #18A97B;   /* Green — Units card */
  --bmw-red:    #E03535;   /* Red — Reset button hover */
  --sidebar-w:  290px;     /* Sidebar fixed width */
  --radius:     10px;      /* Card corner radius */
}
```

### Year Slider Label Colour
The year mark labels on the range slider use `#5BB8FF` (bright sky-blue) applied as **inline styles** directly on each mark — this overrides rc-slider's own inline styles which CSS classes alone cannot beat:

```python
marks={
    y: {
        "label": str(y),
        "style": {
            "color": "#5BB8FF",    # bright sky-blue
            "fontWeight": "600",
            "fontSize": "10.5px",
        }
    }
    for y in ALL_YEARS
}
```

### To change the primary theme colour
Edit one line in `styles.css`:
```css
--bmw-blue: #YOUR_COLOR;
```
All buttons, sliders, and highlights update automatically.

---

## 12. Code Walkthrough — app.py

The file is split into **7 clearly labelled sections**:

```
Section 1  ──  Load & Clean Data
Section 2  ──  Colour Palette & Shared Chart Layout
Section 3  ──  Dash App Initialisation
Section 4  ──  Helper Functions  (dropdown option builders)
Section 5  ──  Layout            (full page structure)
Section 6  ──  Callbacks         (A through O — 15 total)
Section 7  ──  Run Server
```

### Section 1 — Data Cleaning Logic

```python
df_raw = pd.read_csv("bmw_global_sales_2018_2025.csv")

# Drop rows where critical columns are missing
df_raw.dropna(subset=["Units_Sold", "Revenue_EUR"], inplace=True)

# Fill optional columns with safe defaults
df_raw.fillna({"BEV_Share": 0, "Premium_Share": 0,
               "GDP_Growth": 0, "Fuel_Price_Index": 1}, inplace=True)

# Enforce correct data types
df_raw["Year"]   = df_raw["Year"].astype(int)
df_raw["Month"]  = df_raw["Month"].astype(int)
df_raw["Region"] = df_raw["Region"].astype("category")
df_raw["Model"]  = df_raw["Model"].astype("category")
```

### Section 2 — Shared Chart Styling

```python
COLOR_SEQ = px.colors.qualitative.Set2   # consistent 8-colour palette

CHART_LAYOUT = dict(
    paper_bgcolor = "rgba(0,0,0,0)",     # transparent background
    plot_bgcolor  = "rgba(0,0,0,0)",
    font          = dict(family="Inter, Arial", size=12),
    margin        = dict(l=40, r=20, t=40, b=40),
    ...
)
```
`**CHART_LAYOUT` is spread into every chart so all nine share identical fonts, backgrounds, and grid colours.

### Section 6 — Callback Summary

| ID | Trigger | Produces |
|----|---------|---------|
| 6-A | Reset click | Clears all 4 filter values |
| 6-B | Region changes | Rebuilt Model options |
| 6-C | Year changes | Rebuilt Month options |
| 6-E | Any filter | Filter pills + record badge |
| 6-F | Any filter | 5 KPI cards |
| 6-G | Any filter | Region stacked bar |
| 6-H | Any filter | Monthly trend line |
| 6-I | Any filter | Model donut pie |
| 6-J | Any filter | Units histogram |
| 6-K | Any filter | Revenue box plot |
| 6-L | Any filter | Scatter plot |
| 6-M | Any filter | Correlation heatmap |
| 6-N | Any filter | Annual revenue bar |
| 6-O | Any filter | BEV trend line |

---

## 13. Common Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError: bmw_global_sales_2018_2025.csv` | CSV not beside `app.py` | Move CSV into `bmw_dashboard/` folder |
| `ModuleNotFoundError: No module named 'dash'` | Libraries not installed | `pip install dash plotly pandas` |
| `OSError: Address already in use` | Port 8050 in use | Add `port=8051` to `app.run(...)` |
| `KeyError: 'BEV_Share'` | Column name mismatch | Check CSV headers match code exactly |
| All charts blank after filter | Zero records matched | Click ↺ Reset to restore data |
| No styling at all | `styles.css` not in `assets/` | Confirm exact path: `assets/styles.css` |
| Year labels invisible on slider | rc-slider inline style conflict | Use `marks={y: {"label": ..., "style": {...}}}` dict form |

---

## 14. How to Extend the Dashboard

### Add a new chart

```python
# 1. Add to layout (Section 5)
dcc.Graph(id="chart-new")

# 2. Add callback (Section 6)
@app.callback(
    Output("chart-new", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_new(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    fig = px.bar(d, x="Model", y="Units_Sold", color="Region")
    fig.update_layout(**CHART_LAYOUT, height=320)
    return fig
```

### Add a new KPI card
Inside `update_kpis()`, add to the return list:
```python
card("🎯", "My Metric", f"{value:,.0f}", "subtitle text", "blue")
```

### Swap the chart colour palette
```python
# Options: Plotly, D3, G10, T10, Dark24, Light24, Alphabet
COLOR_SEQ = px.colors.qualitative.D3
```

### Deploy online

| Platform | Difficulty | Notes |
|----------|-----------|-------|
| Render.com | ⭐ Easy | Free tier, Python native |
| Railway.app | ⭐ Easy | GitHub integration |
| Heroku | ⭐⭐ Medium | Needs `Procfile` + `requirements.txt` |
| AWS / GCP | ⭐⭐⭐ Advanced | Production scale |

For any deployment, update the last line of `app.py`:
```python
app.run(debug=False, host="0.0.0.0", port=8050)
```

---

## 15. Glossary

| Term | Definition |
|------|-----------|
| **Dash** | Python framework by Plotly — builds web dashboards without writing HTML or JS |
| **Callback** | Python function Dash calls automatically when a UI component changes |
| **dcc** | `dash.dcc` — Core Components (Dropdown, Graph, RangeSlider…) |
| **html** | `dash.html` — HTML tags as Python classes (Div, Label, Button…) |
| **Plotly Express** | High-level chart API: `px.bar()`, `px.line()`, `px.scatter()`… |
| **BEV** | Battery Electric Vehicle — fully electric, no combustion engine |
| **PHEV** | Plug-in Hybrid Electric Vehicle |
| **ICE** | Internal Combustion Engine — petrol or diesel |
| **KPI** | Key Performance Indicator — a single top-level metric |
| **Pearson r** | Correlation coefficient: −1 = perfect negative, 0 = none, +1 = perfect positive |
| **Box Plot** | Chart showing min, Q1, median, Q3, max, and outlier dots |
| **`assets/` folder** | Dash convention — CSS/JS files here are auto-served to the browser |
| **`apply_filters()`** | Shared helper function used by every callback for consistent data filtering |
| **rc-slider** | The React slider library Dash's `RangeSlider` uses internally |
| **RestOfWorld** | All markets outside Europe, China, and USA |

---

## ⚡ Quick Reference Card

```
╔══════════════════════════════════════════════════╗
║           BMW SALES DASHBOARD — CHEATSHEET       ║
╠══════════════════════════════════════════════════╣
║  INSTALL    pip install dash plotly pandas       ║
║  RUN        python app.py                        ║
║  OPEN       http://127.0.0.1:8050                ║
║  STOP       Ctrl + C                             ║
╠══════════════════════════════════════════════════╣
║  FILES                                           ║
║  app.py            → all Python + Dash logic     ║
║  assets/styles.css → auto-loaded by Dash         ║
║  *.csv             → must sit next to app.py     ║
╠══════════════════════════════════════════════════╣
║  FILTERS                                         ║
║  Region  → narrows Model options                 ║
║  Year    → narrows Month options                 ║
║  Reset   → restores all defaults                 ║
║  All 9 charts + 5 KPIs update on every change    ║
╚══════════════════════════════════════════════════╝
```

---

*Built with Python · Dash · Plotly Express · Pandas · Pure CSS*
