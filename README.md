# 🚗 BMW Global Sales Dashboard (2018–2025)
### A Complete Interactive Analytics Dashboard built with Python · Dash · Plotly · Pandas

---

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Project Structure](#3-project-structure)
4. [Dataset Reference](#4-dataset-reference)
5. [Quick Start (Step-by-Step)](#5-quick-start-step-by-step)
6. [Dashboard Layout](#6-dashboard-layout)
7. [KPI Cards](#7-kpi-cards)
8. [Filters – How They Work](#8-filters--how-they-work)
9. [Charts Reference](#9-charts-reference)
10. [Callback Architecture](#10-callback-architecture)
11. [CSS Theming & Styling](#11-css-theming--styling)
12. [Code Walkthrough (app.py)](#12-code-walkthrough-apppy)
13. [Common Errors & Fixes](#13-common-errors--fixes)
14. [How to Extend the Dashboard](#14-how-to-extend-the-dashboard)
15. [Glossary](#15-glossary)

---

## 1. Project Overview

This dashboard provides an **end-to-end interactive view** of BMW's global vehicle sales data spanning **2018 to 2025**. It covers four key regions, eight vehicle models, and eleven data dimensions including units sold, revenue, EV adoption, pricing, and macro-economic indicators.

### What you can do with this dashboard
- Compare **region-wise and model-wise** sales performance
- Spot **seasonal trends** by filtering specific months or year ranges
- Track **EV (BEV) adoption** growth across regions over time
- Detect **revenue outliers** and pricing anomalies with box plots
- Understand **correlations** between sales, pricing, GDP, and fuel index
- Instantly **reset all filters** and explore any data slice in seconds

---

## 2. Tech Stack

| Library | Version | Purpose |
|---------|---------|---------|
| `dash` | 2.x | Web app framework, layout, and routing |
| `plotly` | 5.x | Interactive chart rendering |
| `plotly.express` | (included) | High-level chart API |
| `plotly.graph_objects` | (included) | Low-level chart API (used for heatmap) |
| `pandas` | 1.5+ | Data loading, cleaning, filtering, aggregation |
| `CSS3` | — | Custom sidebar and card layout (no Bootstrap needed) |

> **No JavaScript knowledge required.** Dash handles all frontend-backend communication automatically through its callback system.

---

## 3. Project Structure

```
bmw_dashboard/
│
├── app.py                            ← Main application (all Python logic lives here)
│
├── bmw_global_sales_2018_2025.csv    ← Raw dataset (must be placed in this folder)
│
├── assets/
│   └── styles.css                    ← Custom CSS (auto-loaded by Dash)
│
└── README.md                         ← This documentation file
```

> **Important:** Dash automatically loads every file inside the `assets/` folder.
> You do **not** need to import or link `styles.css` manually — just keep it in that folder.

---

## 4. Dataset Reference

**File:** `bmw_global_sales_2018_2025.csv`
**Total rows:** ~3,073 records
**Frequency:** Monthly — one row per Region × Model × Month × Year combination

### Column Definitions

| Column | Data Type | Example Values | Description |
|--------|-----------|---------------|-------------|
| `Year` | `int` | 2018, 2019 … 2025 | Calendar year of the record |
| `Month` | `int` | 1 to 12 | Calendar month (1 = January, 12 = December) |
| `Region` | `category` | Europe, China, USA, RestOfWorld | Global sales region |
| `Model` | `category` | 3 Series, X5, iX, MINI … | BMW vehicle model |
| `Units_Sold` | `int` | 2,000 – 16,000 | Number of vehicles sold that month |
| `Avg_Price_EUR` | `float` | 40,000 – 94,000 | Average selling price in Euros |
| `Revenue_EUR` | `float` | 100M – 1.4B | Total revenue = Units × Avg Price |
| `BEV_Share` | `float` | 0.00 – 0.25 | Battery Electric Vehicle share (0.2 = 20%) |
| `Premium_Share` | `float` | 0.00 – 0.25 | Premium variant share of total sales |
| `GDP_Growth` | `float` | -2.0 to 6.0 | GDP growth rate of the region that month |
| `Fuel_Price_Index` | `float` | 0.9 – 1.5 | Indexed fuel price (1.0 = baseline) |

### Vehicle Models Covered

| Model | Segment | Powertrain |
|-------|---------|-----------|
| 3 Series | Compact executive sedan | ICE / Hybrid |
| 5 Series | Mid-size executive sedan | ICE / Hybrid |
| X3 | Compact SUV | ICE / Hybrid |
| X5 | Mid-size SUV | ICE / Hybrid / PHEV |
| X7 | Full-size luxury SUV | ICE |
| i4 | Compact executive sedan | Full BEV (Electric) |
| iX | Mid-size SUV | Full BEV (Electric) |
| MINI | Subcompact hatchback | ICE / BEV |

### Regions Covered

| Region Code | Markets Included |
|-------------|-----------------|
| `Europe` | Germany, UK, France, Italy and all European markets |
| `China` | Mainland China |
| `USA` | United States of America |
| `RestOfWorld` | APAC, Middle East, Africa, Latin America and all other markets |

---

## 5. Quick Start (Step-by-Step)

### Step 1 — Install Python
Download Python 3.8 or newer from [python.org](https://python.org)

Verify the installation:
```bash
python --version
# Expected output: Python 3.8.x or higher
```

### Step 2 — Install required libraries
Open your terminal (Mac/Linux) or Command Prompt (Windows) and run:
```bash
pip install dash plotly pandas
```
This installs all three required libraries in one command.

### Step 3 — Organise your project folder
Make sure your folder structure looks exactly like this before running:
```
bmw_dashboard/
├── app.py
├── bmw_global_sales_2018_2025.csv    ← dataset must be here
├── assets/
│   └── styles.css
└── README.md
```

> ⚠️ **The CSV file must be in the same directory as `app.py`.**
> If it is stored elsewhere, update line 16 of `app.py`:
> ```python
> df_raw = pd.read_csv("path/to/your/bmw_global_sales_2018_2025.csv")
> ```

### Step 4 — Launch the application
```bash
cd bmw_dashboard
python app.py
```

You will see this confirmation in your terminal:
```
=======================================================
  BMW Global Sales Dashboard
  Open browser → http://127.0.0.1:8050
=======================================================
```

### Step 5 — Open in your browser
Open any browser (Chrome, Firefox, Edge, Safari) and navigate to:
```
http://127.0.0.1:8050
```
The dashboard loads immediately with **all data visible** and filters in their default (none selected) state.

### Step 6 — Stop the server
Press `Ctrl + C` in the terminal window to shut down the server.

---

## 6. Dashboard Layout

```
┌────────────────────────────────────────────────────────────────────┐
│                        Dashboard Wrapper                           │
│                                                                    │
│  ┌───────────────┐  ┌──────────────────────────────────────────┐  │
│  │               │  │  Page Header  (Title + Record Count)     │  │
│  │   SIDEBAR     │  ├──────────────────────────────────────────┤  │
│  │   290px       │  │  KPI Cards  (5 dynamic metric tiles)     │  │
│  │               │  ├──────────────────────────────────────────┤  │
│  │  🌍 Region    │  │  ROW 1:  Bar Chart  |  Line Chart        │  │
│  │  🚗 Model     │  ├──────────────────────────────────────────┤  │
│  │  📅 Year      │  │  ROW 2:  Pie  |  Histogram  |  Box Plot  │  │
│  │  🗓️ Month    │  ├──────────────────────────────────────────┤  │
│  │               │  │  ROW 3:  Scatter Plot  |  Heatmap        │  │
│  │  ↺  Reset     │  ├──────────────────────────────────────────┤  │
│  │               │  │  ROW 4:  Stacked Revenue  |  BEV Trend   │  │
│  │  Active Pills │  │                                          │  │
│  └───────────────┘  └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

| Area | Width | Description |
|------|-------|-------------|
| Sidebar | 290px (fixed) | Dark navy panel holding all four filter controls |
| Main Content | Flexible (fills remaining space) | Page header, 5 KPI cards, and all 9 chart cards |

---

## 7. KPI Cards

Five metric cards sit at the top of the main area and **update instantly** whenever any filter changes.

| # | Icon | KPI Name | How it is Calculated | Display Unit |
|---|------|----------|---------------------|--------------|
| 1 | 📋 | Total Records | `len(filtered_df)` | Count |
| 2 | 🚗 | Total Units Sold | `sum(Units_Sold)` | Millions (M) |
| 3 | 💶 | Total Revenue | `sum(Revenue_EUR)` | Billions EUR (€B) |
| 4 | 🏷️ | Avg Price (EUR) | `mean(Avg_Price_EUR)` | Euros (€) |
| 5 | ⚡ | Avg BEV Share | `mean(BEV_Share) × 100` | Percentage (%) |

Each card also shows a subtitle line with secondary context such as the number of regions and models currently matched by the filters.

### Card colour indicators

| Top-border colour | Card |
|-------------------|------|
| 🔵 Blue | Total Records, BEV Share |
| 🟢 Green | Total Units Sold |
| 🟠 Amber | Total Revenue |
| 🟣 Purple | Average Price |

---

## 8. Filters — How They Work

All four filters live in the left sidebar. They operate **in combination** — every chart and KPI responds to the combined state of all active filters simultaneously.

### Filter 1 — Region (Multi-select Dropdown)
- **Component ID:** `filter-region`
- Options: `Europe`, `China`, `USA`, `RestOfWorld`
- Select one or more regions; leave blank to include all regions
- **Linked output:** When Region changes, the **Model dropdown options automatically narrow** to only models sold in those regions

### Filter 2 — Model (Multi-select Dropdown)
- **Component ID:** `filter-model`
- Options: 8 BMW models (dynamic list based on Region selection)
- Select one or more models; leave blank to include all models
- **Depends on:** Region filter (options update when Region changes)
- Clearing the Region filter restores all 8 model options

### Filter 3 — Year Range (Range Slider)
- **Component ID:** `filter-year`
- Drag the left handle to set start year; drag right handle to set end year
- Default state: full range `2018 → 2025`
- **Linked output:** When Year range changes, the **Month dropdown options automatically update** to show only months available within the selected years

### Filter 4 — Month (Multi-select Dropdown)
- **Component ID:** `filter-month`
- Options: Jan through Dec (dynamic based on Year selection)
- Select specific months; leave blank to include all months
- **Depends on:** Year range filter

### Reset Button
- **Component ID:** `btn-reset`
- One click clears Region, Model, and Month selections and resets Year slider to `2018–2025`
- All charts and KPIs immediately refresh to show the full dataset

### Active Filter Pills
Small colour-coded badges appear below the Reset button showing which filters are currently active. When nothing is selected they display "All data".

---

## 9. Charts Reference

### Row 1 — Sales Overview

#### Chart 1: Region-Wise Units Sold (Horizontal Stacked Bar)
- **Component ID:** `chart-bar-region`
- X-axis: Units Sold (cumulative total)
- Y-axis: Region names
- Colour segments: Vehicle Model
- Logic: Groups by `Region` + `Model`, sums `Units_Sold`
- Purpose: Compare how much each region contributes and which models dominate within each region

#### Chart 2: Monthly Sales Trend (Multi-Line)
- **Component ID:** `chart-line-trend`
- X-axis: Year-Month period (e.g., "2022-06")
- Y-axis: Total units sold
- Colour: Year — each year is a separate line
- Logic: Groups by `Year` + `Month`, sums `Units_Sold`, sorts chronologically
- Purpose: Observe how sales volumes move through the calendar year and compare year-over-year

---

### Row 2 — Distribution & Spread

#### Chart 3: Model Market Share (Donut Pie)
- **Component ID:** `chart-pie-model`
- Segments: One per model
- Values: Total `Units_Sold` per model
- Logic: Groups by `Model`, sums units
- Purpose: Understand which models drive the most volume in the filtered selection

#### Chart 4: Units Sold Distribution (Histogram)
- **Component ID:** `chart-hist-units`
- X-axis: Units Sold per record
- Y-axis: Frequency (number of records in each bin)
- Bins: 40
- Logic: Plots raw `Units_Sold` column directly with no aggregation
- Purpose: See whether monthly unit counts are normally distributed or skewed

#### Chart 5: Revenue Box Plot
- **Component ID:** `chart-box-revenue`
- X-axis: Region
- Y-axis: Revenue per record (EUR)
- Shows: Minimum, Q1, Median, Q3, Maximum, and outlier dots; mean line also displayed
- Logic: Raw `Revenue_EUR` values grouped by `Region`
- Purpose: Identify regions with unusually high or low revenue months and spot outliers

---

### Row 3 — Relationships & Correlations

#### Chart 6: Avg Price vs Revenue (Bubble Scatter)
- **Component ID:** `chart-scatter`
- X-axis: Average Price (EUR)
- Y-axis: Revenue (EUR)
- Bubble size: Units Sold (larger bubble = more units)
- Colour: Region
- Hover details: Model, Year, Month name
- Performance note: Randomly samples a maximum of 2,000 rows for large datasets to maintain speed
- Purpose: Discover whether higher-priced models generate proportionally more revenue

#### Chart 7: Correlation Heatmap
- **Component ID:** `chart-heatmap`
- Variables: `Units_Sold`, `Avg_Price_EUR`, `Revenue_EUR`, `BEV_Share`, `GDP_Growth`, `Fuel_Price_Index`
- Colour scale: RdBu — Red = strong negative correlation, Blue = strong positive, White = no correlation
- Values displayed: Pearson r rounded to 2 decimal places
- Logic: `pandas .corr()` method on the filtered DataFrame
- Purpose: Understand which numeric variables move together across the dataset

---

### Row 4 — Revenue & EV Insights

#### Chart 8: Annual Revenue by Region (Stacked Bar)
- **Component ID:** `chart-revenue-stacked`
- X-axis: Year
- Y-axis: Total revenue in Billions EUR
- Colour segments: Region
- Logic: Groups by `Year` + `Region`, sums `Revenue_EUR`, divides by 1,000,000,000
- Purpose: Track year-over-year revenue growth and regional contribution trends

#### Chart 9: BEV Share Trend (Multi-Line)
- **Component ID:** `chart-bev-trend`
- X-axis: Year
- Y-axis: Average BEV Share (%)
- Colour: Region — one line per region
- Logic: Groups by `Year` + `Region`, averages `BEV_Share`, multiplies by 100
- Purpose: Monitor how electric vehicle adoption has grown in each market from 2018 to 2025

---

## 10. Callback Architecture

Dash callbacks are Python functions that execute automatically whenever a filter input changes. Below is the complete dependency map for this dashboard.

```
INPUTS (what triggers the update)        OUTPUTS (what gets updated)
─────────────────────────────────────────────────────────────────────
btn-reset (n_clicks)              →      filter-region value
                                  →      filter-model value
                                  →      filter-year value
                                  →      filter-month value

filter-region (value)             →      filter-model options list

filter-year (value)               →      filter-month options list

filter-region   ┐                 →      active-filter-info (pills)
filter-model    ├─ all 4 filters  →      record-count-badge
filter-year     │
filter-month    ┘

filter-region   ┐                 →      kpi-section (5 KPI cards)
filter-model    ├─ all 4 filters  →      chart-bar-region
filter-year     │                 →      chart-line-trend
filter-month    ┘                 →      chart-pie-model
                                  →      chart-hist-units
                                  →      chart-box-revenue
                                  →      chart-scatter
                                  →      chart-heatmap
                                  →      chart-revenue-stacked
                                  →      chart-bev-trend
```

### The shared `apply_filters()` function

Every chart and KPI callback passes through this single helper function to guarantee consistent results:

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

Using one shared function means all 11 chart and KPI outputs always reflect **identical filter logic** — no inconsistencies between cards.

---

## 11. CSS Theming & Styling

The file `assets/styles.css` controls the entire visual appearance of the dashboard. Design tokens are defined as CSS variables at the top of the file so the whole theme can be changed by editing a single block.

```css
:root {
  --bmw-blue:   #1C69D4;   /* Primary brand blue — buttons, sliders, highlights */
  --bmw-dark:   #0D1B2A;   /* Sidebar background */
  --bmw-mid:    #1A2E44;   /* Dropdown menu panels */
  --bmw-light:  #F4F7FB;   /* Page background */
  --bmw-card:   #FFFFFF;   /* Chart and KPI card background */
  --bmw-border: #DDE3EC;   /* Card borders and input borders */
  --bmw-text:   #1E2A38;   /* Primary text colour */
  --bmw-muted:  #6B7A8D;   /* Subtitle and label text */
  --bmw-accent: #E8931A;   /* Amber — Revenue KPI card */
  --bmw-green:  #18A97B;   /* Green — Units Sold KPI card */
  --bmw-red:    #E03535;   /* Red — Reset button hover state */
  --sidebar-w:  290px;     /* Sidebar fixed width */
  --radius:     10px;      /* Border radius for all cards */
}
```

### CSS Sections Summary

| CSS Class / Selector | What It Styles |
|----------------------|---------------|
| `.dashboard-wrapper` | Root flex container (sidebar + main side by side) |
| `.sidebar` | Dark fixed-width panel, sticky, scrollable |
| `.sidebar-logo` | BMW badge and subtitle at the top of the sidebar |
| `.filter-block` | Spacing wrapper around each individual filter |
| `.filter-label` | Icon plus text label row above each dropdown |
| `.dash-dropdown .Select-*` | Full visual override of Dash's dropdown for the dark theme |
| `.rc-slider-*` | Year range slider — track colour, handle, tooltip |
| `.reset-btn` | Ghost button with red hover state |
| `.active-pill` | Blue pill badges showing active filter values |
| `.kpi-card` | White metric tile with a coloured top accent border |
| `.chart-card` | White chart container with subtle shadow |
| `.charts-grid` | CSS Grid rules for each chart row layout |
| `@media` rules | Responsive — stacks to single column below 820px and 1100px |

### Changing the colour theme
To swap the primary colour from BMW blue to any other brand colour, change only this one variable:
```css
--bmw-blue: #FF0000;  /* example: change to red */
```
All buttons, sliders, dropdown selection highlights, and KPI card accents update automatically.

---

## 12. Code Walkthrough (app.py)

The file is divided into 7 clearly labelled sections with comment headers:

```
Section 1  ─  Load & Clean Data
Section 2  ─  Colour Palette & Shared Chart Layout Settings
Section 3  ─  Dash App Initialisation
Section 4  ─  Helper Functions (dropdown option list builders)
Section 5  ─  Layout  (full HTML structure using Dash components)
Section 6  ─  Callbacks  (labelled A through O — 15 callbacks total)
Section 7  ─  Run Server
```

### Section 1 — Data Loading and Cleaning
```python
df_raw = pd.read_csv("bmw_global_sales_2018_2025.csv")
df_raw.dropna(subset=["Units_Sold", "Revenue_EUR"], inplace=True)
df_raw.fillna({"BEV_Share": 0, "Premium_Share": 0, ...}, inplace=True)
df_raw["Year"]   = df_raw["Year"].astype(int)
df_raw["Region"] = df_raw["Region"].astype("category")
```
Any row missing `Units_Sold` or `Revenue_EUR` is dropped as these are critical columns. Optional numeric columns get zero-filled so chart math never fails.

### Section 2 — Shared Colour and Layout Settings
```python
COLOR_SEQ    = px.colors.qualitative.Set2
CHART_LAYOUT = dict(paper_bgcolor=..., font=..., margin=..., legend=..., ...)
```
`CHART_LAYOUT` is spread with `**` into every chart's `fig.update_layout()` call so all nine charts share the same transparent background, font, grid colour, and legend styling.

### Section 5 — Layout
The layout is pure Python using Dash's `html.*` and `dcc.*` classes. No HTML files are needed. Key structural choices:
- `html.Aside(className="sidebar")` contains all filter controls
- `html.Main(className="main-content")` contains the header, KPIs, and charts
- `html.Div(id="kpi-section")` is an empty placeholder — its children are injected by a callback
- `dcc.Graph(id="chart-*")` components are empty shells — figures are injected by callbacks

### Section 6 — Callbacks (15 total)

| Label | Trigger | What it produces |
|-------|---------|-----------------|
| 6-A | Reset button click | Clears all four filter values simultaneously |
| 6-B | Region filter changes | Rebuilds the Model dropdown options list |
| 6-C | Year slider changes | Rebuilds the Month dropdown options list |
| 6-D | (shared helper function, not a callback) | Returns filtered DataFrame |
| 6-E | Any filter changes | Updates filter pills + record count badge |
| 6-F | Any filter changes | Renders the 5 KPI cards |
| 6-G | Any filter changes | Horizontal stacked bar chart |
| 6-H | Any filter changes | Multi-line monthly trend chart |
| 6-I | Any filter changes | Donut pie chart |
| 6-J | Any filter changes | Units sold histogram |
| 6-K | Any filter changes | Revenue box plot |
| 6-L | Any filter changes | Bubble scatter plot |
| 6-M | Any filter changes | Correlation heatmap |
| 6-N | Any filter changes | Annual stacked revenue bar |
| 6-O | Any filter changes | BEV share trend lines |

---

## 13. Common Errors & Fixes

| Error Message | Most Likely Cause | Solution |
|---------------|-------------------|----------|
| `FileNotFoundError: bmw_global_sales_2018_2025.csv` | CSV is not in the same folder as `app.py` | Move the CSV file into the `bmw_dashboard/` folder |
| `ModuleNotFoundError: No module named 'dash'` | Required libraries are not installed | Run `pip install dash plotly pandas` in your terminal |
| `OSError: [Errno 98] Address already in use` | Port 8050 is already in use by another process | Add `port=8051` to the `app.run(...)` call on the last line, then open `http://127.0.0.1:8051` |
| `KeyError: 'BEV_Share'` | Column name mismatch — the CSV has a different header | Open the CSV in a text editor and check the exact column names match what the code expects |
| Dashboard loads but all charts are empty | The filter combination matches zero records | Click the Reset button to restore all data |
| Page loads with no styling at all | The `styles.css` file is not inside the `assets/` folder | Confirm the file path is exactly `bmw_dashboard/assets/styles.css` |
| Dropdown options do not update | Browser has cached the previous state | Hard-refresh with `Ctrl + Shift + R` (Windows/Linux) or `Cmd + Shift + R` (Mac) |
| Charts load slowly on large selections | Too many data points being plotted | The scatter chart auto-samples to 2,000 rows; other charts aggregate before plotting |

---

## 14. How to Extend the Dashboard

### Add a new chart
1. Add a `dcc.Graph(id="chart-myname")` somewhere in the layout section (Section 5)
2. Write a new callback in Section 6:

```python
@app.callback(
    Output("chart-myname", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_myname(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    fig = px.bar(d, x="Model", y="Units_Sold", color="Region")
    fig.update_layout(**CHART_LAYOUT, height=320)
    return fig
```

### Add a new KPI card
Inside the `update_kpis()` callback, add a new `card(...)` entry to the returned list:
```python
card("🎯", "Your KPI Label", f"{your_value:,.0f}", "description", "blue")
```

### Add a new sidebar filter
1. Add a `dcc.Dropdown(id="filter-new", ...)` block in the sidebar section
2. Add `Input("filter-new", "value")` to every callback that currently reads the four filters
3. Update the `apply_filters()` function to accept and apply the new parameter

### Swap the colour palette
Replace `COLOR_SEQ` in Section 2 with any Plotly qualitative palette:
```python
COLOR_SEQ = px.colors.qualitative.Plotly   # or D3, G10, T10, Dark24, Light24
```

### Deploy online
To make the dashboard publicly accessible, change the last two lines of `app.py`:
```python
app.run(debug=False, host="0.0.0.0", port=8050)
```
Then deploy to any of these platforms:

| Platform | Difficulty | Notes |
|----------|-----------|-------|
| Render.com | Easy | Free tier available; supports Python natively |
| Railway.app | Easy | Free tier with GitHub integration |
| Heroku | Medium | Requires `Procfile` and `requirements.txt` |
| AWS / GCP / Azure | Advanced | For production-scale and enterprise deployments |

---

## 15. Glossary

| Term | Definition |
|------|-----------|
| **Dash** | A Python web framework by Plotly for building data dashboards without writing HTML or JavaScript |
| **Callback** | A Python function that Dash calls automatically when a UI component's value changes |
| **dcc** | `dash.dcc` — Dash Core Components library (Dropdown, Graph, Slider, RangeSlider, etc.) |
| **html** | `dash.html` — HTML elements expressed as Python classes (Div, Label, Button, Aside, etc.) |
| **Plotly Express** | High-level Plotly API: `px.bar()`, `px.line()`, `px.scatter()`, `px.pie()`, etc. |
| **graph_objects** | Low-level Plotly API: used for the heatmap (`go.Heatmap`) which Express does not support as flexibly |
| **BEV** | Battery Electric Vehicle — a fully electric car with no internal combustion engine |
| **PHEV** | Plug-in Hybrid Electric Vehicle — combines electric motor with a petrol/diesel engine |
| **ICE** | Internal Combustion Engine — a traditional petrol or diesel powered vehicle |
| **KPI** | Key Performance Indicator — a single headline metric (total units, revenue, etc.) |
| **Pearson r** | A correlation coefficient from -1.0 (perfect negative) through 0 (none) to +1.0 (perfect positive) |
| **Box Plot** | A chart showing minimum, Q1, median, Q3, maximum, and outlier dots for a distribution |
| **Histogram** | A chart showing how frequently values fall into equal-width bins |
| **`assets/` folder** | A special Dash convention — any CSS or JS file placed here is automatically served to the browser |
| **RestOfWorld** | Dashboard shorthand for all markets outside Europe, China, and the USA |
| **`apply_filters()`** | A shared Python helper function used by every callback to apply consistent filtering logic |

---

## 📞 Quick Reference Card

```
─────────────────────────────────────────────────────
  SETUP
  pip install dash plotly pandas

  RUN
  cd bmw_dashboard
  python app.py

  OPEN
  http://127.0.0.1:8050

  STOP
  Ctrl + C  (in terminal)
─────────────────────────────────────────────────────
  FILES
  app.py            ← all Python + Dash logic
  assets/styles.css ← auto-loaded CSS (do not move)
  *.csv             ← must be next to app.py
─────────────────────────────────────────────────────
  FILTERS
  Region   → narrows Model options
  Year     → narrows Month options
  Reset    → restores everything to defaults
  All 9 charts update within ~200ms of any change
─────────────────────────────────────────────────────
```

---

*Built with Python · Dash · Plotly Express · Pandas · Pure CSS*
