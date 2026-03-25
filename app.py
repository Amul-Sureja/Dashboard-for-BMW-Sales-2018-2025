# =============================================================
#  BMW Global Sales Dashboard  (2018 – 2025)
#  Tech: Dash + Plotly Express + Pandas
#  Run :  pip install dash plotly pandas
#          python app.py
# =============================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback_context

# ─────────────────────────────────────────────
# 1.  LOAD & CLEAN DATA
# ─────────────────────────────────────────────
df_raw = pd.read_csv("bmw_global_sales_2018_2025.csv")

# Handle missing values
df_raw.dropna(subset=["Units_Sold", "Revenue_EUR"], inplace=True)
df_raw.fillna({"BEV_Share": 0, "Premium_Share": 0,
                "GDP_Growth": 0, "Fuel_Price_Index": 1}, inplace=True)

# Correct data types
df_raw["Year"]   = df_raw["Year"].astype(int)
df_raw["Month"]  = df_raw["Month"].astype(int)
df_raw["Region"] = df_raw["Region"].astype("category")
df_raw["Model"]  = df_raw["Model"].astype("category")

# Month number → name mapping
MONTH_NAMES = {
    1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
    7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"
}
df_raw["Month_Name"] = df_raw["Month"].map(MONTH_NAMES)

# Handy lists
ALL_REGIONS = sorted(df_raw["Region"].unique().tolist())
ALL_MODELS  = sorted(df_raw["Model"].unique().tolist())
ALL_YEARS   = sorted(df_raw["Year"].unique().tolist())
ALL_MONTHS  = list(range(1, 13))

# ─────────────────────────────────────────────
# 2.  COLOUR PALETTE (shared across charts)
# ─────────────────────────────────────────────
COLOR_SEQ   = px.colors.qualitative.Set2
BMW_BLUE    = "#1C69D4"
CHART_FONT  = dict(family="Inter, Arial, sans-serif", size=12, color="#1E2A38")

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=CHART_FONT,
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#DDE3EC",
        borderwidth=1,
        font=dict(size=11)
    ),
    xaxis=dict(gridcolor="#EEF1F6", zerolinecolor="#EEF1F6"),
    yaxis=dict(gridcolor="#EEF1F6", zerolinecolor="#EEF1F6"),
)

# ─────────────────────────────────────────────
# 3.  DASH APP INITIALISATION
# ─────────────────────────────────────────────
app = Dash(
    __name__,
    title="BMW Sales Dashboard",
    suppress_callback_exceptions=True
)

# ─────────────────────────────────────────────
# 4.  HELPER: dropdown option builders
# ─────────────────────────────────────────────
def make_opts(lst):
    return [{"label": str(v), "value": v} for v in lst]

def make_month_opts(months):
    return [{"label": MONTH_NAMES[m], "value": m} for m in months]

# ─────────────────────────────────────────────
# 5.  LAYOUT
# ─────────────────────────────────────────────
app.layout = html.Div(className="dashboard-wrapper", children=[

    # ── SIDEBAR ──────────────────────────────
    html.Aside(className="sidebar", children=[

        # Logo
        html.Div(className="sidebar-logo", children=[
            html.Div("BMW", className="logo-badge"),
            html.Div([
                html.Div("Sales Dashboard", className="logo-text"),
                html.Div("2018 – 2025 · Global", className="logo-sub"),
            ])
        ]),

        html.Div("Filters", className="sidebar-section-title"),

        # ── Region ──
        html.Div(className="filter-block", children=[
            html.Label([html.Span("🌍", className="filter-icon"), " Region"],
                       className="filter-label"),
            dcc.Dropdown(
                id="filter-region",
                options=make_opts(ALL_REGIONS),
                multi=True,
                placeholder="All regions…",
                clearable=True
            ),
        ]),

        # ── Model ──
        html.Div(className="filter-block", children=[
            html.Label([html.Span("🚗", className="filter-icon"), " Model"],
                       className="filter-label"),
            dcc.Dropdown(
                id="filter-model",
                options=make_opts(ALL_MODELS),
                multi=True,
                placeholder="All models…",
                clearable=True
            ),
        ]),

        # ── Year (range slider) ──
        html.Div(className="filter-block", children=[
            html.Label([html.Span("📅", className="filter-icon"), " Year Range"],
                       className="filter-label"),
            html.Div(className="year-slider-wrap", children=[
                dcc.RangeSlider(
                    id="filter-year",
                    min=min(ALL_YEARS), max=max(ALL_YEARS),
                    step=1,
                    value=[min(ALL_YEARS), max(ALL_YEARS)],
                    marks={y: str(y) for y in ALL_YEARS},
                    tooltip={"always_visible": False, "placement": "bottom"},
                    allowCross=False
                ),
            ]),
        ]),

        # ── Month ──
        html.Div(className="filter-block", children=[
            html.Label([html.Span("🗓️", className="filter-icon"), " Month"],
                       className="filter-label"),
            dcc.Dropdown(
                id="filter-month",
                options=make_month_opts(ALL_MONTHS),
                multi=True,
                placeholder="All months…",
                clearable=True
            ),
        ]),

        html.Div(className="sidebar-sep"),

        # Reset button
        html.Button(
            ["↺  Reset Filters"],
            id="btn-reset",
            className="reset-btn",
            n_clicks=0
        ),

        # Active filter count indicator
        html.Div(id="active-filter-info", className="active-filters"),
    ]),

    # ── MAIN CONTENT ──────────────────────────
    html.Main(className="main-content", children=[

        # Header
        html.Div(className="page-header", children=[
            html.Div([
                html.Div("BMW Global Sales Analytics", className="page-title"),
                html.Div("Interactive performance dashboard · Units, Revenue & Market Trends",
                         className="page-subtitle"),
            ]),
            html.Div(id="record-count-badge", className="last-updated"),
        ]),

        # ── KPI CARDS ────────────────────────
        html.Div(id="kpi-section", className="kpi-section"),

        # ── CHARTS ROW 1 : Bar + Line ─────────
        html.Div("Sales Overview", className="chart-section-title"),
        html.Div(className="charts-grid charts-row-2", children=[

            html.Div(className="chart-card", children=[
                html.Div("🌍  Region-Wise Units Sold", className="chart-card-title"),
                html.Div("Total units per region for selected filters",
                         className="chart-card-desc"),
                dcc.Graph(id="chart-bar-region", config={"displayModeBar": False}),
            ]),

            html.Div(className="chart-card", children=[
                html.Div("📈  Monthly Sales Trend", className="chart-card-title"),
                html.Div("Units sold over time, grouped by year",
                         className="chart-card-desc"),
                dcc.Graph(id="chart-line-trend", config={"displayModeBar": False}),
            ]),
        ]),

        # ── CHARTS ROW 2 : Pie + Histogram + Box ─
        html.Div("Distribution & Spread", className="chart-section-title mt-16"),
        html.Div(className="charts-grid charts-row-3", children=[

            html.Div(className="chart-card", children=[
                html.Div("🥧  Model Market Share", className="chart-card-title"),
                html.Div("Share of total units by model", className="chart-card-desc"),
                dcc.Graph(id="chart-pie-model", config={"displayModeBar": False}),
            ]),

            html.Div(className="chart-card", children=[
                html.Div("📊  Units Sold Distribution", className="chart-card-title"),
                html.Div("Histogram of monthly unit records",
                         className="chart-card-desc"),
                dcc.Graph(id="chart-hist-units", config={"displayModeBar": False}),
            ]),

            html.Div(className="chart-card", children=[
                html.Div("📦  Revenue Box Plot", className="chart-card-title"),
                html.Div("Revenue spread & outliers by region",
                         className="chart-card-desc"),
                dcc.Graph(id="chart-box-revenue", config={"displayModeBar": False}),
            ]),
        ]),

        # ── CHARTS ROW 3 : Scatter + Heatmap ─
        html.Div("Relationships & Correlations", className="chart-section-title mt-16"),
        html.Div(className="charts-grid charts-row-3-1", children=[

            html.Div(className="chart-card", children=[
                html.Div("🔵  Avg Price vs Revenue (Scatter)", className="chart-card-title"),
                html.Div("Each point = one record; colour by Region",
                         className="chart-card-desc"),
                dcc.Graph(id="chart-scatter", config={"displayModeBar": False}),
            ]),

            html.Div(className="chart-card", children=[
                html.Div("🔥  Correlation Heatmap", className="chart-card-title"),
                html.Div("Pearson r between numeric columns",
                         className="chart-card-desc"),
                dcc.Graph(id="chart-heatmap", config={"displayModeBar": False}),
            ]),
        ]),

        # ── CHARTS ROW 4 : Revenue stacked + BEV ─
        html.Div("Revenue & EV Insights", className="chart-section-title mt-16"),
        html.Div(className="charts-grid charts-row-2", children=[

            html.Div(className="chart-card", children=[
                html.Div("💰  Annual Revenue by Region (Stacked)",
                         className="chart-card-title"),
                html.Div("Total EUR revenue per year, stacked by region",
                         className="chart-card-desc"),
                dcc.Graph(id="chart-revenue-stacked", config={"displayModeBar": False}),
            ]),

            html.Div(className="chart-card", children=[
                html.Div("⚡  BEV Share Trend by Region", className="chart-card-title"),
                html.Div("Average EV adoption share over years",
                         className="chart-card-desc"),
                dcc.Graph(id="chart-bev-trend", config={"displayModeBar": False}),
            ]),
        ]),

    ]),  # end main-content
])  # end dashboard-wrapper


# ─────────────────────────────────────────────
# 6.  CALLBACKS
# ─────────────────────────────────────────────

# ── 6-A  Reset all filters ────────────────────
@app.callback(
    Output("filter-region", "value"),
    Output("filter-model",  "value"),
    Output("filter-year",   "value"),
    Output("filter-month",  "value"),
    Input("btn-reset", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(_n):
    return None, None, [min(ALL_YEARS), max(ALL_YEARS)], None


# ── 6-B  Model options depend on Region ───────
@app.callback(
    Output("filter-model", "options"),
    Input("filter-region", "value"),
)
def update_model_options(regions):
    if not regions:
        return make_opts(ALL_MODELS)
    filtered = df_raw[df_raw["Region"].isin(regions)]["Model"].unique().tolist()
    return make_opts(sorted(filtered))


# ── 6-C  Month options depend on Year range ───
@app.callback(
    Output("filter-month", "options"),
    Input("filter-year", "value"),
)
def update_month_options(year_range):
    if not year_range:
        return make_month_opts(ALL_MONTHS)
    lo, hi = year_range
    months = df_raw[df_raw["Year"].between(lo, hi)]["Month"].unique().tolist()
    return make_month_opts(sorted(months))


# ── 6-D  MASTER FILTER → produces filtered df ─
def apply_filters(regions, models, year_range, months):
    """Return a filtered copy of df_raw based on sidebar selections."""
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


# ── 6-E  Active filter info badge ─────────────
@app.callback(
    Output("active-filter-info",   "children"),
    Output("record-count-badge",   "children"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def update_filter_info(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    n = len(d)
    pills = []
    if regions:
        for r in regions:
            pills.append(html.Span(r, className="active-pill"))
    if models:
        for m in models:
            pills.append(html.Span(m, className="active-pill"))
    if year_range and year_range != [min(ALL_YEARS), max(ALL_YEARS)]:
        pills.append(html.Span(f"{year_range[0]}–{year_range[1]}",
                               className="active-pill"))
    if months:
        for mo in months:
            pills.append(html.Span(MONTH_NAMES[mo], className="active-pill"))
    if not pills:
        pills = [html.Span("All data", className="active-pill")]

    badge = f"📋 {n:,} records matched"
    return pills, badge


# ── 6-F  KPI CARDS ────────────────────────────
@app.callback(
    Output("kpi-section", "children"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def update_kpis(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)

    total_records  = len(d)
    total_units    = d["Units_Sold"].sum()
    total_revenue  = d["Revenue_EUR"].sum()
    avg_price      = d["Avg_Price_EUR"].mean() if len(d) else 0
    avg_bev        = d["BEV_Share"].mean() * 100 if len(d) else 0
    unique_regions = d["Region"].nunique()
    unique_models  = d["Model"].nunique()
    avg_units_mo   = d.groupby(["Year","Month"])["Units_Sold"].sum().mean() if len(d) else 0

    def card(icon, label, value, sub, color):
        return html.Div(className=f"kpi-card {color}", children=[
            html.Span(icon, className="kpi-icon"),
            html.Div(label,  className="kpi-label"),
            html.Div(value,  className="kpi-value"),
            html.Div(sub,    className="kpi-sub"),
        ])

    return [
        card("📋", "Total Records",
             f"{total_records:,}",
             f"{unique_regions} regions · {unique_models} models", "blue"),
        card("🚗", "Total Units Sold",
             f"{total_units/1e6:.2f}M",
             f"Avg {avg_units_mo:,.0f} units / month", "green"),
        card("💶", "Total Revenue",
             f"€{total_revenue/1e9:.2f}B",
             "EUR Revenue", "accent"),
        card("🏷️", "Avg Price (EUR)",
             f"€{avg_price:,.0f}",
             "Average across selection", "purple"),
        card("⚡", "Avg BEV Share",
             f"{avg_bev:.1f}%",
             "Electric vehicle share", "blue"),
    ]


# ── 6-G  BAR CHART – Region vs Units ──────────
@app.callback(
    Output("chart-bar-region", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_bar_region(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    agg = (d.groupby(["Region","Model"], observed=True)["Units_Sold"]
             .sum().reset_index()
             .sort_values("Units_Sold", ascending=True))
    fig = px.bar(
        agg, x="Units_Sold", y="Region", color="Model",
        orientation="h",
        color_discrete_sequence=COLOR_SEQ,
        labels={"Units_Sold": "Units Sold", "Region": ""}
    )
    fig.update_layout(**CHART_LAYOUT, height=300,
                      barmode="stack", showlegend=True)
    fig.update_traces(marker_line_width=0)
    return fig


# ── 6-H  LINE CHART – Monthly trend ───────────
@app.callback(
    Output("chart-line-trend", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_line_trend(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    agg = (d.groupby(["Year","Month"], observed=True)["Units_Sold"]
             .sum().reset_index())
    agg["Period"] = agg["Year"].astype(str) + "-" + agg["Month"].astype(str).str.zfill(2)
    agg.sort_values("Period", inplace=True)

    fig = px.line(
        agg, x="Period", y="Units_Sold", color="Year",
        color_discrete_sequence=COLOR_SEQ,
        markers=True,
        labels={"Units_Sold": "Units Sold", "Period": "Month"}
    )
    fig.update_layout(**CHART_LAYOUT, height=300,
                      xaxis_tickangle=-45, showlegend=True)
    fig.update_traces(line_width=2, marker_size=4)
    return fig


# ── 6-I  PIE CHART – Model share ──────────────
@app.callback(
    Output("chart-pie-model", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_pie_model(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    agg = d.groupby("Model", observed=True)["Units_Sold"].sum().reset_index()
    fig = px.pie(
        agg, names="Model", values="Units_Sold",
        color_discrete_sequence=COLOR_SEQ,
        hole=0.4
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=CHART_FONT,
        margin=dict(l=10, r=10, t=20, b=10),
        height=290,
        legend=dict(font=dict(size=11))
    )
    fig.update_traces(textposition="inside", textinfo="percent+label",
                      textfont_size=10)
    return fig


# ── 6-J  HISTOGRAM – Units distribution ───────
@app.callback(
    Output("chart-hist-units", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_hist(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    fig = px.histogram(
        d, x="Units_Sold", nbins=40,
        color_discrete_sequence=[BMW_BLUE],
        labels={"Units_Sold": "Units Sold", "count": "Frequency"}
    )
    fig.update_layout(**CHART_LAYOUT, height=290, showlegend=False)
    fig.update_traces(marker_line_color="white", marker_line_width=0.5)
    return fig


# ── 6-K  BOX PLOT – Revenue by Region ─────────
@app.callback(
    Output("chart-box-revenue", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_box(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    fig = px.box(
        d, x="Region", y="Revenue_EUR", color="Region",
        color_discrete_sequence=COLOR_SEQ,
        labels={"Revenue_EUR": "Revenue (EUR)", "Region": ""}
    )
    fig.update_layout(**CHART_LAYOUT, height=290, showlegend=False)
    fig.update_traces(boxmean=True)
    return fig


# ── 6-L  SCATTER – Avg Price vs Revenue ───────
@app.callback(
    Output("chart-scatter", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_scatter(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    # Sample max 2000 rows for perf
    sample = d.sample(min(2000, len(d)), random_state=42) if len(d) > 0 else d
    fig = px.scatter(
        sample,
        x="Avg_Price_EUR", y="Revenue_EUR",
        color="Region", size="Units_Sold",
        size_max=18,
        color_discrete_sequence=COLOR_SEQ,
        hover_data=["Model", "Year", "Month_Name"],
        labels={
            "Avg_Price_EUR": "Avg Price (EUR)",
            "Revenue_EUR": "Revenue (EUR)"
        },
        opacity=0.75
    )
    fig.update_layout(**CHART_LAYOUT, height=320)
    return fig


# ── 6-M  HEATMAP – Correlation matrix ─────────
@app.callback(
    Output("chart-heatmap", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_heatmap(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    num_cols = ["Units_Sold","Avg_Price_EUR","Revenue_EUR",
                "BEV_Share","GDP_Growth","Fuel_Price_Index"]
    corr = d[num_cols].corr().round(2)

    labels = ["Units\nSold","Avg\nPrice","Revenue",
              "BEV\nShare","GDP\nGrowth","Fuel\nIdx"]

    fig = go.Figure(go.Heatmap(
        z=corr.values,
        x=labels, y=labels,
        colorscale="RdBu",
        zmid=0,
        text=corr.values,
        texttemplate="%{text}",
        textfont={"size": 11},
        hovertemplate="%{x} vs %{y}: %{z}<extra></extra>"
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor ="rgba(0,0,0,0)",
        font=CHART_FONT,
        margin=dict(l=60, r=20, t=20, b=60),
        height=320,
    )
    return fig


# ── 6-N  STACKED BAR – Annual Revenue by Region
@app.callback(
    Output("chart-revenue-stacked", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_revenue_stacked(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    agg = (d.groupby(["Year","Region"], observed=True)["Revenue_EUR"]
             .sum().reset_index())
    agg["Revenue_B"] = agg["Revenue_EUR"] / 1e9
    fig = px.bar(
        agg, x="Year", y="Revenue_B", color="Region",
        color_discrete_sequence=COLOR_SEQ,
        labels={"Revenue_B": "Revenue (€B)", "Year": "Year"}
    )
    fig.update_layout(**CHART_LAYOUT, height=310,
                      barmode="stack", xaxis_type="category")
    fig.update_traces(marker_line_width=0)
    return fig


# ── 6-O  LINE – BEV Share trend by Region ─────
@app.callback(
    Output("chart-bev-trend", "figure"),
    Input("filter-region", "value"),
    Input("filter-model",  "value"),
    Input("filter-year",   "value"),
    Input("filter-month",  "value"),
)
def chart_bev_trend(regions, models, year_range, months):
    d = apply_filters(regions, models, year_range, months)
    agg = (d.groupby(["Year","Region"], observed=True)["BEV_Share"]
             .mean().reset_index())
    agg["BEV_Pct"] = agg["BEV_Share"] * 100
    fig = px.line(
        agg, x="Year", y="BEV_Pct", color="Region",
        color_discrete_sequence=COLOR_SEQ,
        markers=True,
        labels={"BEV_Pct": "BEV Share (%)", "Year": "Year"}
    )
    fig.update_layout(**CHART_LAYOUT, height=310,
                      xaxis_type="category")
    fig.update_traces(line_width=2.5, marker_size=6)
    return fig


# ─────────────────────────────────────────────
# 7.  RUN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*55)
    print("  BMW Global Sales Dashboard")
    print("  Open browser → http://127.0.0.1:8050")
    print("="*55 + "\n")
    app.run(debug=False, host="0.0.0.0", port=8050)
