"""
NSW Crime Intelligence Dashboard — Data Narrative
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import requests
import json

st.set_page_config(
    page_title="NSW Crime Intelligence | Data Narrative",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #FFFFFF;
}

.block-container {
    padding-top: 0.8rem;
    padding-bottom: 2.5rem;
}

.filter-title {
    font-size: 1.7rem;
    font-weight: 800;
    color: #E63946;
    margin-bottom: 1rem;
}

.hero-banner {
    background: linear-gradient(135deg, #F8FBFF 0%, #EEF5FF 50%, #FFFFFF 100%);
    border: 1px solid #D7E6FA;
    border-radius: 18px;
    padding: 42px 48px 38px;
    margin-bottom: 22px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 28px rgba(15, 67, 130, 0.08);
}

.hero-banner::after {
    content: '';
    position: absolute;
    right: -80px;
    top: -30px;
    width: 420px;
    height: 420px;
    background: radial-gradient(
        circle,
        rgba(37,99,235,.12) 0%,
        rgba(37,99,235,.05) 45%,
        transparent 75%
    );
    pointer-events: none;
}

.hero-title {
    font-size: 2.9rem;
    font-weight: 800;
    color: #0B2A5B;
    margin: 0;
    letter-spacing: -.03em;
}

.hero-title span {
    color: #2563EB;
}

.hero-sub {
    color: #163B6D;
    font-size: 1.08rem;
    margin: 16px 0 0;
    max-width: 760px;
    line-height: 1.7;
}

.kpi-card {
    background: #FFFFFF;
    border: 1px solid #D9E8FA;
    border-radius: 16px;
    padding: 24px;
    min-height: 165px;
    box-shadow: 0 10px 28px rgba(15, 67, 130, 0.08);
    transition: all .25s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
    border-color: #2563EB;
    box-shadow: 0 14px 32px rgba(37,99,235,.14);
}

.kpi-val {
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1;
}

.kpi-val.red {
    color: #E63946;
}

.kpi-val.amber {
    color: #2563EB;
}

.kpi-val.teal {
    color: #1D4ED8;
}

.kpi-val.blue {
    color: #E63946;
}

.kpi-lbl {
    font-size: .78rem;
    color: #163B6D;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-top: 12px;
    font-weight: 600;
}

.kpi-delta {
    font-size: .88rem;
    margin-top: 14px;
    font-weight: 700;
}

.kpi-delta.pos {
    color: #00A86B;
}

.kpi-delta.neg {
    color: #E63946;
}

.kpi-delta.neu {
    color: #163B6D;
}

.kpi-delta.warn {
    color: #F59E0B;
}

.callout {
    background: linear-gradient(90deg, rgba(230,57,70,.08), rgba(37,99,235,.03));
    border-left: 5px solid #E63946;
    border-radius: 0 14px 14px 0;
    padding: 18px 24px;
    margin: 0 0 18px;
    font-size: .96rem;
    line-height: 1.75;
    box-shadow: 0 8px 22px rgba(15,67,130,.06);
}

.callout,
.callout * {
    color: #000000 !important;
}

.callout b {
    color: #000000 !important;
}

.story-card {
    background: #F8FBFF;
    border: 1px solid #D7E6FA;
    border-left: 5px solid #2563EB;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 18px;
    color: #0B2A5B;
    line-height: 1.7;
    box-shadow: 0 8px 22px rgba(15,67,130,.05);
}

.act-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 38px 0 18px;
}

.act-num {
    background: #2563EB;
    color: #FFFFFF;
    font-size: .78rem;
    font-weight: 800;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.act-title {
    font-size: 1.55rem;
    font-weight: 800;
    color: #1F2937;
    margin: 0;
}

.stMultiSelect span[data-baseweb="tag"] {
    background-color: #2563EB !important;
    color: white !important;
}

label {
    color: #163B6D !important;
    font-weight: 600 !important;
}

#MainMenu, footer, header {
    visibility: hidden;
}

/* ── Metric component overrides ── */
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #0B2A5B !important;
}
[data-testid="stMetricLabel"] {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: #163B6D !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
[data-testid="stMetricDelta"] {
    font-size: 0.85rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] svg {
    display: none;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── DATA PATHS ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(BASE_DIR, "final_csvs")

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading NSW crime data…")
def load_all():
    crime_df = pd.read_csv(
        os.path.join(CSV_DIR, "nsw_lga_crime_tableau_clean.csv"),
        parse_dates=["Month"],
    )

    daily_df = pd.read_csv(
        os.path.join(CSV_DIR, "nsw_daily_crime_grouped_clean.csv"),
        parse_dates=["Date"],
    )

    pop_df = pd.read_csv(
        os.path.join(CSV_DIR, "nsw_lga_avg_population_2021_2025_clean.csv")
    ).dropna(subset=["LGA"])

    police_cnt_df = pd.read_csv(
        os.path.join(CSV_DIR, "nsw_police_station_count_by_lga_clean.csv")
    ).dropna(subset=["LGA"])

    police_geo_df = pd.read_csv(
        os.path.join(CSV_DIR, "nsw_police_stations_with_lga_clean.csv")
    )

    lga_centroids = (
        police_geo_df.dropna(subset=["LGA"])
        .groupby("LGA")[["Latitude", "Longitude"]]
        .mean()
        .reset_index()
    )

    return crime_df, daily_df, pop_df, police_cnt_df, police_geo_df, lga_centroids


crime_df, daily_df, pop_df, police_cnt_df, police_geo_df, lga_centroids = load_all()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def compute_lga_summary(df: pd.DataFrame) -> pd.DataFrame:
    agg = (
        df.groupby("LGA")["Incident_Count"]
        .sum()
        .reset_index()
        .rename(columns={"Incident_Count": "Total_Crime"})
    )

    out = (
        agg.merge(
            pop_df[["LGA", "Avg_Population_2021_2025", "Population_2025"]],
            on="LGA",
            how="left",
        )
        .merge(police_cnt_df, on="LGA", how="left")
        .merge(lga_centroids, on="LGA", how="left")
    )

    out["Crime_Rate_Per_1000"] = (
        out["Total_Crime"] / out["Avg_Population_2021_2025"]
    ) * 1000

    out["Crimes_Per_Station"] = (
        out["Total_Crime"] / out["Police_Station_Count"].replace(0, np.nan)
    )

    out = out.dropna(subset=["Avg_Population_2021_2025"])

    return out


PLOTLY_BASE = dict(
    paper_bgcolor="white",
    plot_bgcolor="white",
    font=dict(color="#111827", family="Inter, sans-serif", size=12),
    title_font=dict(size=15, color="#111827"),
    margin=dict(l=8, r=8, t=42, b=8),
    xaxis=dict(
        gridcolor="rgba(0,0,0,0.08)",
        linecolor="rgba(0,0,0,0.15)",
        tickfont=dict(color="#374151"),
    ),
    yaxis=dict(
        gridcolor="rgba(0,0,0,0.08)",
        linecolor="rgba(0,0,0,0.15)",
        tickfont=dict(color="#374151"),
    ),
    legend=dict(
        bgcolor="rgba(255,255,255,0.95)",
        bordercolor="rgba(0,0,0,0.08)",
        borderwidth=1,
        font=dict(color="#111827"),
    ),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#93C5FD",
        font_color="#111827",
    ),
)


def themed(fig, h: int = None):
    fig.update_layout(**PLOTLY_BASE)
    if h:
        fig.update_layout(height=h)
    return fig


# ── WHAT-IF THRESHOLDS ───────────────────────────────────────────────────────
st.markdown("---")
st.markdown("**⚙️ What-If Thresholds** — adjust to model different policy scenarios", unsafe_allow_html=False)
wi1, wi2 = st.columns(2)
with wi1:
    cr_thresh = st.slider("🚨 Flag LGAs above crime rate (per 1,000 residents)", 20, 600, 150, 10)
with wi2:
    cps_thresh = st.slider("🚔 Under-policed flag (crimes per police station)", 500, 15000, 3000, 250)
st.markdown("---")

# ── FILTER TITLE ──────────────────────────────────────────────────────────────
st.markdown(
    """
<div class="filter-title">
🔎 Dashboard Filters
</div>
""",
    unsafe_allow_html=True,
)

# ── FILTERS ───────────────────────────────────────────────────────────────────
f1, f2, f3 = st.columns([1, 1.4, 1.6])

with f1:
    year_range = st.slider(
        "Time Period",
        min_value=2021,
        max_value=2025,
        value=(2021, 2025),
        step=1,
    )

with f2:
    all_lgas = sorted(crime_df["LGA"].dropna().unique().tolist())

    lga_pick = st.multiselect(
        "LGA",
        options=["All LGAs"] + all_lgas,
        default=["All LGAs"],
    )

with f3:
    all_offences = sorted(crime_df["Offence category"].dropna().unique().tolist())

    offence_pick = st.multiselect(
        "Offence Category",
        options=["All Offences"] + all_offences,
        default=["All Offences"],
    )

# ── APPLY FILTERS ─────────────────────────────────────────────────────────────
fc = crime_df.copy()

fc = fc[
    fc["Year"].between(
        year_range[0],
        year_range[1],
    )
]

if "All LGAs" not in lga_pick and len(lga_pick) > 0:
    fc = fc[fc["LGA"].isin(lga_pick)]

if "All Offences" not in offence_pick and len(offence_pick) > 0:
    fc = fc[fc["Offence category"].isin(offence_pick)]

# ── RECALCULATE SUMMARY ───────────────────────────────────────────────────────
if not fc.empty:
    lga_sum = compute_lga_summary(fc)
else:
    lga_sum = pd.DataFrame()

# ── KPI VALUES ────────────────────────────────────────────────────────────────
total_inc = int(fc["Incident_Count"].sum()) if not fc.empty else 0

n_lgas = fc["LGA"].nunique() if not fc.empty else 0

med_rate = (
    lga_sum["Crime_Rate_Per_1000"].median()
    if not lga_sum.empty and "Crime_Rate_Per_1000" in lga_sum.columns
    else 0
)

high_risk = (
    int((lga_sum["Crime_Rate_Per_1000"] > cr_thresh).sum())
    if not lga_sum.empty and "Crime_Rate_Per_1000" in lga_sum.columns
    else 0
)

under_policed = (
    int((lga_sum["Crimes_Per_Station"] > cps_thresh).sum())
    if not lga_sum.empty and "Crimes_Per_Station" in lga_sum.columns
    else 0
)

top_lga = (
    fc.groupby("LGA")["Incident_Count"].sum().idxmax()
    if not fc.empty
    else "N/A"
)

top_off = (
    fc.groupby("Offence category")["Incident_Count"].sum().idxmax()
    if not fc.empty
    else "N/A"
)

# ── YEAR-OVER-YEAR CHANGE ─────────────────────────────────────────────────────
if not fc.empty and year_range[1] > year_range[0]:
    prev_y = fc[fc["Year"] == year_range[1] - 1]["Incident_Count"].sum()
    curr_y = fc[fc["Year"] == year_range[1]]["Incident_Count"].sum()

    yoy = ((curr_y - prev_y) / prev_y) * 100 if prev_y else 0
else:
    yoy = 0

yoy_cls = "neg" if yoy > 0 else "pos"
yoy_sym = "▲" if yoy > 0 else "▼"

# ── DYNAMIC RISK STATUS ───────────────────────────────────────────────────────
if high_risk > cr_thresh:
    risk_cls = "neg"
    risk_icon = "⚠"
    risk_text = "Above threshold"
elif high_risk == cr_thresh:
    risk_cls = "warn"
    risk_icon = "●"
    risk_text = "At threshold"
else:
    risk_cls = "pos"
    risk_icon = "✓"
    risk_text = "Under threshold"

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
<div class="hero-banner">
    <h1 class="hero-title">
        NSW <span>Crime Intelligence</span>
    </h1>

<p class='hero-sub'>
    A data narrative exploring where crime concentrates,
    how policing resources are distributed,
    and what the numbers mean for community safety —
    {year_range[0]} to {year_range[1]}.
</p>
</div>
""",
    unsafe_allow_html=True,
)

# ── STORY SNAPSHOT ────────────────────────────────────────────────────────────
st.markdown(
    f"""
<div class="callout">
    <b>Story snapshot ({year_range[0]}–{year_range[1]}):</b>
    Across <b>{n_lgas} NSW LGAs</b>,
    <b>{total_inc:,} incidents</b> were recorded —
    with <b>{top_lga}</b> leading in volume and
    <b>{top_off}</b> the most prevalent offence type.
    The median LGA crime rate sits at
    <b>{med_rate:.0f} per 1,000 residents</b>.
    Under the current threshold settings,
    <b>{high_risk} LGAs</b> exceed the crime-rate alert
    and <b>{under_policed} LGAs</b>
    are flagged as under-policed.
</div>
""",
    unsafe_allow_html=True,
)

# ── KPI CARDS ─────────────────────────────────────────────────────────────────
k1, k2, k3 = st.columns(3)

with k1:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-val red">{total_inc:,}</div>
    <div class="kpi-lbl">Total Incidents ({year_range[0]}–{year_range[1]})</div>
    <div class="kpi-delta {yoy_cls}">{yoy_sym} {abs(yoy):.1f}% vs prior year</div>
</div>
""",
        unsafe_allow_html=True,
    )

with k2:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-val amber">{n_lgas}</div>
    <div class="kpi-lbl">LGAs with Crime Records</div>
    <div class="kpi-delta neu">Across New South Wales</div>
</div>
""",
        unsafe_allow_html=True,
    )

with k3:
    st.markdown(
        f"""
<div class="kpi-card">
    <div class="kpi-val teal">{med_rate:.0f}</div>
    <div class="kpi-lbl">Median Crime Rate / 1,000</div>
    <div class="kpi-delta neu">Across all selected LGAs</div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ACT 1 — THE SCALE
# ══════════════════════════════════════════════════════════════════════════════
BLUE_SCALE = [
    [0.0, "#DBEAFE"],
    [0.2, "#BFDBFE"],
    [0.4, "#93C5FD"],
    [0.6, "#60A5FA"],
    [0.8, "#2563EB"],
    [1.0, "#1E3A8A"],
]

st.markdown(
    """<div class="act-header">
      <div class="act-num">1</div>
      <h2 class="act-title">The Scale — Statewide Crime Trends</h2>
    </div>""",
    unsafe_allow_html=True,
)

col_trend, col_offbar = st.columns([2, 1])

with col_trend:
    yearly_tot = fc.groupby("Year")["Incident_Count"].sum().reset_index()
    yearly_tot.columns = ["Year", "Incidents"]

    fig_trend = go.Figure()
    fig_trend.add_trace(
        go.Scatter(
            x=yearly_tot["Year"],
            y=yearly_tot["Incidents"],
            mode="lines+markers",
            line=dict(color="#2563EB", width=3),
            marker=dict(size=9, color="#1E3A8A", line=dict(color="#DBEAFE", width=2)),
            hovertemplate="<b>%{x}</b><br>Incidents: <b>%{y:,}</b><extra></extra>",
        )
    )

    themed(fig_trend, 300)

    fig_trend.update_layout(
        title="NSW Annual Crime Incidents",
        hovermode="x unified",
        showlegend=False,
        xaxis=dict(tickmode="linear", dtick=1),
    )

    st.plotly_chart(fig_trend, use_container_width=True)

with col_offbar:
    top_off_df = (
        fc.groupby("Offence category")["Incident_Count"]
        .sum()
        .sort_values()
        .tail(10)
        .reset_index()
    )

    fig_offbar = go.Figure(
        go.Bar(
            x=top_off_df["Incident_Count"],
            y=top_off_df["Offence category"],
            orientation="h",
            marker=dict(
                color=top_off_df["Incident_Count"],
                colorscale=BLUE_SCALE,
                showscale=False,
                line=dict(color="white", width=0.8),
            ),
            hovertemplate="<b>%{y}</b><br>Incidents: <b>%{x:,}</b><extra></extra>",
        )
    )

    themed(fig_offbar, 300)
    fig_offbar.update_layout(title="Top 10 Offence Categories")
    st.plotly_chart(fig_offbar, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ACT 2 — WHERE
# ══════════════════════════════════════════════════════════════════════════════
import geopandas as gpd

st.markdown(
    """<div class="act-header">
      <div class="act-num">2</div>
      <h2 class="act-title">Where — Crime Across NSW Geography</h2>
    </div>""",
    unsafe_allow_html=True,
)

# ── MAP + BAR LAYOUT ──────────────────────────────────────────────────────────
map_col, geo_bar_col = st.columns([1.45, 1])

# ── LOAD GEO DATA ─────────────────────────────────────────────────────────────
geo_df = gpd.read_file(os.path.join(BASE_DIR, "nsw_lga.geojson"))

# Clean LGA names for matching
geo_df["LGA"] = geo_df["LGA"].astype(str).str.strip()
geo_json = geo_df.__geo_interface__

map_data = lga_sum.dropna(subset=["LGA"]).copy()
map_data["LGA"] = map_data["LGA"].astype(str).str.strip()

# ── MAP COLUMN ────────────────────────────────────────────────────────────────
with map_col:
    metric_choice = st.radio(
        "Map colour:",
        ["Total Crime", "Crime Rate / 1k"],
        horizontal=True,
        key="map_metric_local",
    )

    metric = (
        "Total_Crime"
        if metric_choice == "Total Crime"
        else "Crime_Rate_Per_1000"
    )

    colorbar_title = (
        "Total Crime"
        if metric_choice == "Total Crime"
        else "Crime Rate / 1k"
    )

    fig = px.choropleth(
        map_data,
        geojson=geo_json,
        locations="LGA",
        featureidkey="properties.LGA",
        color=metric,
        hover_name="LGA",
        hover_data={
            "Total_Crime": ":,",
            "Crime_Rate_Per_1000": ":.1f",
            "Police_Station_Count": True,
        },
        color_continuous_scale="Blues",
    )

    police_df = police_geo_df.dropna(subset=["Latitude", "Longitude"]).copy()

    fig.add_trace(
        go.Scattergeo(
            lat=police_df["Latitude"],
            lon=police_df["Longitude"],
            mode="markers",
            marker=dict(
                size=6,
                color="#E63946",
                opacity=0.85,
                line=dict(width=0.6, color="white"),
            ),
            name="Police Stations",
            text=police_df["Station_Name"],
            hovertemplate="<b>%{text}</b><extra></extra>",
        )
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False,
    )

    fig.update_layout(
        title="NSW Crime Heat Map with Police Station Overlay",
        height=490,
        margin=dict(l=0, r=0, t=45, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#111827"),
        title_font=dict(color="#111827"),
        coloraxis_colorbar=dict(
            title=colorbar_title,
            tickfont=dict(color="#111827"),
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#D7E6FA",
            borderwidth=1,
            font=dict(color="#111827"),
        ),
    )

    st.plotly_chart(fig, use_container_width=True)

# ── BAR CHART COLUMN ──────────────────────────────────────────────────────────
with geo_bar_col:
    n_show = st.selectbox(
        "Show top:",
        [10, 15, 20],
        key="geo_n",
    )

    rank_by = st.radio(
        "Rank by:",
        ["Total Crime", "Crime Rate / 1k"],
        horizontal=True,
        key="geo_rank",
    )

    met_c = (
        "Total_Crime"
        if rank_by == "Total Crime"
        else "Crime_Rate_Per_1000"
    )

    top_lgas_df = (
        lga_sum.nlargest(n_show, met_c)[
            ["LGA", "Total_Crime", "Crime_Rate_Per_1000", "Police_Station_Count"]
        ]
        .sort_values(met_c, ascending=True)
    )

    fig_geobar = go.Figure(
        go.Bar(
            x=top_lgas_df[met_c],
            y=top_lgas_df["LGA"],
            orientation="h",
            marker=dict(
                color=top_lgas_df[met_c],
                colorscale=BLUE_SCALE,
                showscale=False,
                line=dict(color="white", width=0.8),
            ),
            customdata=top_lgas_df[
                ["Total_Crime", "Crime_Rate_Per_1000", "Police_Station_Count"]
            ].values,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Total: <b>%{customdata[0]:,}</b><br>"
                "Rate: <b>%{customdata[1]:.1f}/1k</b><br>"
                "Stations: <b>%{customdata[2]:.0f}</b><extra></extra>"
            ),
        )
    )

    themed(fig_geobar, 490)

    fig_geobar.update_layout(
        title=f"Top {n_show} LGAs — {rank_by}",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#111827"),
        title_font=dict(color="#111827"),
        xaxis=dict(
            gridcolor="rgba(0,0,0,0.08)",
            linecolor="rgba(0,0,0,0.15)",
            tickfont=dict(color="#374151"),
        ),
        yaxis=dict(
            tickfont=dict(size=9.5, color="#374151"),
            gridcolor="rgba(0,0,0,0.08)",
            linecolor="rgba(0,0,0,0.15)",
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_color="#111827",
            bordercolor="#93C5FD",
        ),
    )

    st.plotly_chart(fig_geobar, use_container_width=True)
# ══════════════════════════════════════════════════════════════════════════════
# ACT 3 — WHEN
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """<div class="act-header">
      <div class="act-num">3</div>
      <h2 class="act-title">When — Seasonal & Annual Patterns</h2>
    </div>""",
    unsafe_allow_html=True,
)

heat_col, yoy_col = st.columns(2)

with heat_col:
    heat_raw = fc.groupby(["Year", "Month_Num"])["Incident_Count"].sum().reset_index()

    heat_piv = (
        heat_raw
        .pivot(index="Year", columns="Month_Num", values="Incident_Count")
        .fillna(0)
    )

    MN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    heat_piv.columns = [MN[c - 1] for c in heat_piv.columns]

    fig_heat = go.Figure(
        go.Heatmap(
            z=heat_piv.values,
            x=heat_piv.columns.tolist(),
            y=[str(y) for y in heat_piv.index],
            colorscale=BLUE_SCALE,
            hovertemplate="<b>%{y} — %{x}</b><br>Incidents: <b>%{z:,}</b><extra></extra>",
            colorbar=dict(
                title="Incidents",
                tickfont=dict(color="#374151"),
                title_font=dict(color="#111827"),
                bgcolor="white",
                len=0.8,
                thickness=14,
            ),
        )
    )

    themed(fig_heat, 280)
    fig_heat.update_layout(title="Crime Heatmap: Month × Year")
    st.plotly_chart(fig_heat, use_container_width=True)

with yoy_col:
    top5 = (
        fc.groupby("Offence category")["Incident_Count"]
        .sum()
        .nlargest(5)
        .index
        .tolist()
    )

    off_yr = (
        fc[fc["Offence category"].isin(top5)]
        .groupby(["Year", "Offence category"])["Incident_Count"]
        .sum()
        .reset_index()
    )

    COLS = ["#E63946", "#2563EB", "#F59E0B", "#10B981", "#8B5CF6"]

    fig_yoy = go.Figure()

    for i, o in enumerate(top5):
        d = off_yr[off_yr["Offence category"] == o]

        fig_yoy.add_trace(
            go.Scatter(
                x=d["Year"],
                y=d["Incident_Count"],
                mode="lines+markers",
                name=o[:28] + ("…" if len(o) > 28 else ""),
                line=dict(color=COLS[i], width=3),
                marker=dict(size=7, color=COLS[i], line=dict(color="white", width=1)),
                hovertemplate=f"<b>{o}</b><br>%{{x}}: <b>%{{y:,}}</b><extra></extra>",
            )
        )

    themed(fig_yoy, 280)
    fig_yoy.update_layout(title="Top 5 Offences: Year-over-Year")
    st.plotly_chart(fig_yoy, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ACT 4 — CONTEXT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """<div class="act-header">
      <div class="act-num">4</div>
      <h2 class="act-title">Context — Crime Rate vs Police Station Coverage</h2>
    </div>""",
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="story-card">
      This visual explores the relationship between 
      <b>crime rate per 1,000 residents</b> and the 
      <b>number of police stations</b> across NSW LGAs.
      Areas positioned in the high-crime and low-police-coverage
      region may require greater attention.
    </div>
    """,
    unsafe_allow_html=True,
)

scatter_df = lga_sum.dropna(
    subset=[
        "Crime_Rate_Per_1000",
        "Police_Station_Count",
        "Total_Crime",
        "Avg_Population_2021_2025",
        "LGA",
    ]
).copy()

scatter_df["Bubble_Size"] = np.sqrt(scatter_df["Avg_Population_2021_2025"]) / 12

avg_crime_rate = scatter_df["Crime_Rate_Per_1000"].mean()
avg_police = scatter_df["Police_Station_Count"].mean()

fig_bub = go.Figure()

fig_bub.add_trace(
    go.Scatter(
        x=scatter_df["Crime_Rate_Per_1000"],
        y=scatter_df["Police_Station_Count"],
        mode="markers",
        marker=dict(
            size=scatter_df["Bubble_Size"],
            sizemode="area",
            sizeref=2.0 * max(scatter_df["Bubble_Size"]) / (55**2),
            sizemin=6,
            color=scatter_df["Crime_Rate_Per_1000"],
            colorscale=BLUE_SCALE,
            opacity=0.88,
            line=dict(width=1.4, color="rgba(255,255,255,0.95)"),
            colorbar=dict(title="Crime Rate<br>per 1,000", thickness=15),
        ),
        customdata=scatter_df[
            [
                "LGA",
                "Total_Crime",
                "Avg_Population_2021_2025",
                "Crime_Rate_Per_1000",
                "Police_Station_Count",
            ]
        ].values,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br><br>"
            "Crime Rate: <b>%{customdata[3]:.1f} per 1,000</b><br>"
            "Police Stations: <b>%{customdata[4]:.0f}</b><br>"
            "Total Incidents: <b>%{customdata[1]:,}</b><br>"
            "Population: <b>%{customdata[2]:,.0f}</b>"
            "<extra></extra>"
        ),
    )
)

fig_bub.add_vline(
    x=avg_crime_rate,
    line_dash="dash",
    line_color="#3B82F6",
    line_width=2,
    annotation_text="Average crime rate",
    annotation_position="top right",
    annotation_font=dict(size=11, color="#2563EB"),
)

fig_bub.add_hline(
    y=avg_police,
    line_dash="dash",
    line_color="#14B8A6",
    line_width=2,
    annotation_text="Average police stations",
    annotation_position="top right",
    annotation_font=dict(size=11, color="#0F766E"),
)

fig_bub.add_annotation(
    x=scatter_df["Crime_Rate_Per_1000"].max() * 0.88,
    y=scatter_df["Police_Station_Count"].min() + 0.6,
    text="Higher crime rate<br>Lower police coverage",
    showarrow=False,
    font=dict(size=12, color="#1E3A8A"),
    bgcolor="rgba(219,234,254,0.75)",
    bordercolor="#93C5FD",
    borderwidth=1,
    borderpad=6,
)

fig_bub.update_layout(
    title=dict(text="Crime Rate vs Police Station Coverage by LGA", font=dict(size=26, color="#111827")),
    xaxis=dict(
        title="Crime Rate per 1,000 Residents",
        title_font=dict(size=15, color="#374151"),
        tickfont=dict(size=12, color="#4B5563"),
        gridcolor="rgba(0,0,0,0.08)",
        zeroline=False,
    ),
    yaxis=dict(
        title="Number of Police Stations",
        title_font=dict(size=15, color="#374151"),
        tickfont=dict(size=12, color="#4B5563"),
        gridcolor="rgba(0,0,0,0.08)",
        zeroline=False,
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=560,
    margin=dict(l=40, r=40, t=80, b=50),
    hoverlabel=dict(bgcolor="white", font_size=13, font_family="Arial"),
)

st.plotly_chart(fig_bub, use_container_width=True)

st.caption(
    "Each bubble represents an NSW LGA. Bubble size reflects population size, "
    "while colour intensity represents crime rate per 1,000 residents."
)

# ── Crime Rate Heatmap Map ────────────────────────────────────────────────────
import geopandas as gpd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

# ── LOAD GEO DATA ─────────────────────────────────────
geo_df = gpd.read_file(os.path.join(BASE_DIR, "nsw_lga.geojson"))
geo_json = geo_df.__geo_interface__

map_data = lga_sum.dropna(subset=["LGA"]).copy()

metric = "Total_Crime"   # or Crime_Rate_Per_1000

# ── BASE MAP FIGURE ───────────────────────────────────
fig = go.Figure()

# ═══════════════════════════════════════════════════════
# 1. LGA BOUNDARIES (OUTLINE ONLY - NO FILL)
# ═══════════════════════════════════════════════════════
fig.add_trace(
    go.Choroplethmapbox(
        geojson=geo_json,
        locations=map_data["LGA"],
        featureidkey="properties.LGA",
        z=map_data[metric],
        colorscale="Blues",
        showscale=True,
        marker_opacity=0.75,
        marker_line_width=1.2,
        marker_line_color="#1e3a8a",
        hoverinfo="location+z",
        colorbar=dict(title="Total Crime"),
    )
)

# ═══════════════════════════════════════════════════════
# 2. LGA CENTROID BUBBLES (CRIME INTENSITY)
# ═══════════════════════════════════════════════════════
fig.add_trace(
    go.Scattermapbox(
        lat=lga_sum["Latitude"],
        lon=lga_sum["Longitude"],
        mode="markers",

        marker=dict(
            size=lga_sum["Crime_Rate_Per_1000"],  
            sizemode="area",

            # scaling control (VERY important)
            sizeref=2.0 * max(lga_sum["Crime_Rate_Per_1000"]) / (45**2),
            sizemin=5,

            color=lga_sum["Crime_Rate_Per_1000"],
            colorscale="Blues",
            opacity=0.85,
            showscale=True,
            colorbar=dict(title="Crime Rate / 1k"),
        ),

        text=lga_sum["LGA"],
        hovertemplate="<b>%{text}</b><br>Rate: %{marker.color:.1f}/1k<extra></extra>",
        name="LGA Crime Intensity",
    )
)

# ═══════════════════════════════════════════════════════
# 3. POLICE STATIONS (RED DOTS)
# ═══════════════════════════════════════════════════════
police_df = police_geo_df.dropna(subset=["Latitude", "Longitude"])

fig.add_trace(
    go.Scattermapbox(
        lat=police_df["Latitude"],
        lon=police_df["Longitude"],
        mode="markers",
        marker=dict(
            size=6,
            color="red",
            opacity=0.9,
        ),
        text=police_df["Station_Name"],
        name="Police Stations",
        hovertemplate="<b>%{text}</b><extra></extra>",
    )
)

# ═══════════════════════════════════════════════════════
# 4. MAP SETTINGS (LIGHT BLUE THEME)
# ═══════════════════════════════════════════════════════
fig.update_layout(
    mapbox=dict(
        style="carto-positron",   # LIGHT BASE MAP
        zoom=5.6,
        center={"lat": -32.8, "lon": 147.5},
    ),
    height=550,
    margin=dict(l=0, r=0, t=0, b=0),

    paper_bgcolor="white",
    plot_bgcolor="white",

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
    ),
)

# ── RENDER ─────────────────────────────────────────────
st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ACT 5 — THE GAP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    """<div class="act-header">
      <div class="act-num">5</div>
      <h2 class="act-title">The Gap — Are Police Resources Matching Crime Demand?</h2>
    </div>""",
    unsafe_allow_html=True,
)

gap_df = (
    lga_sum.dropna(subset=["Crimes_Per_Station"])
    .nlargest(20, "Crimes_Per_Station")
    .sort_values("Crimes_Per_Station", ascending=True)
)

gap_df["Colour"] = np.linspace(0, 1, len(gap_df))

fig_gap = go.Figure(
    go.Bar(
        x=gap_df["Crimes_Per_Station"],
        y=gap_df["LGA"],
        orientation="h",
        marker=dict(
            color=gap_df["Colour"],
            colorscale=BLUE_SCALE,
            showscale=False,
            line=dict(color="white", width=0.8),
        ),
        customdata=gap_df[
            [
                "Total_Crime",
                "Police_Station_Count",
                "Crime_Rate_Per_1000",
                "Avg_Population_2021_2025",
            ]
        ].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Crimes per Station: <b>%{x:,.0f}</b><br>"
            "Total Incidents: <b>%{customdata[0]:,}</b><br>"
            "Police Stations: <b>%{customdata[1]:.0f}</b><br>"
            "Crime Rate: <b>%{customdata[2]:.1f}/1k</b><br>"
            "Population: <b>%{customdata[3]:,.0f}</b>"
            "<extra></extra>"
        ),
    )
)

fig_gap.add_vline(
    x=cps_thresh,
    line_dash="dash",
    line_color="#1E3A8A",
    line_width=2,
    annotation_text=f"Threshold: {cps_thresh:,}",
    annotation_font=dict(color="#1E3A8A", size=11),
)

themed(fig_gap, 460)

fig_gap.update_layout(
    title="Top 20 LGAs: Crimes per Police Station — Under-policed Risk",
    xaxis=dict(title="Crimes per Police Station"),
)

st.plotly_chart(fig_gap, use_container_width=True)

under_policed_df = (
    lga_sum[lga_sum["Crimes_Per_Station"] > cps_thresh]
    .copy()
    .sort_values("Crimes_Per_Station", ascending=False)
)

if not under_policed_df.empty:
    st.markdown(
        f"""
        <div style="
            margin-top:18px;
            margin-bottom:10px;
            padding:14px 18px;
            background:#FEF2F2;
            border-left:5px solid #DC2626;
            border-radius:10px;
            color:#991B1B;
            font-weight:700;
        ">
            ⚠ Under-policed LGAs: {len(under_policed_df)} areas exceed 
            {cps_thresh:,} incidents per police station
        </div>
        """,
        unsafe_allow_html=True,
    )

    display_df = under_policed_df[
        [
            "LGA",
            "Crimes_Per_Station",
            "Total_Crime",
            "Police_Station_Count",
            "Crime_Rate_Per_1000",
        ]
    ].rename(
        columns={
            "LGA": "LGA",
            "Crimes_Per_Station": "Crimes per Station",
            "Total_Crime": "Total Incidents",
            "Police_Station_Count": "Police Stations",
            "Crime_Rate_Per_1000": "Crime Rate / 1k",
        }
    )

    st.dataframe(
        display_df.style.format(
            {
                "Crimes per Station": "{:,.0f}",
                "Total Incidents": "{:,.0f}",
                "Police Stations": "{:,.0f}",
                "Crime Rate / 1k": "{:,.1f}",
            }
        ).background_gradient(
            subset=["Crimes per Station"],
            cmap="Reds"
        ),
        use_container_width=True,
        hide_index=True,
    )

else:
    st.success(
        f"No LGAs exceed the current threshold of {cps_thresh:,} incidents per police station."
    )

# ══════════════════════════════════════════════════════════════════════════════
# ACT 6 — DEEP DIVE
# ══════════════════════════════════════════════════════════════════════════════
RED_ALERT = "#DC2626"

st.markdown(
    """<div class="act-header">
      <div class="act-num">6</div>
      <h2 class="act-title">Deep Dive — Explore Any LGA in Detail</h2>
    </div>""",
    unsafe_allow_html=True,
)

explore_lga = st.selectbox(
    "Select an LGA to explore:",
    sorted(crime_df["LGA"].dropna().unique()),
    key="explorer",
)

ex_crime = crime_df[
    (crime_df["LGA"] == explore_lga)
    & (crime_df["Year"].between(*year_range))
].copy()

ex_stats = lga_sum[lga_sum["LGA"] == explore_lga]

if not ex_stats.empty:
    ex_total = int(ex_stats["Total_Crime"].iloc[0])
    ex_rate = ex_stats["Crime_Rate_Per_1000"].iloc[0]
    ex_pop = ex_stats["Avg_Population_2021_2025"].iloc[0]
    ex_stations = ex_stats["Police_Station_Count"].iloc[0]
    ex_cps = ex_stats["Crimes_Per_Station"].iloc[0]

    em1, em2, em3, em4 = st.columns(4)

    with em1:
        st.metric("Total Incidents", f"{ex_total:,}")

    with em2:
        delta_rate = ex_rate - med_rate
        st.metric(
            "Crime Rate / 1k",
            f"{ex_rate:.1f}",
            delta=f"{delta_rate:+.1f} vs NSW median",
            delta_color="inverse",
        )

    with em3:
        st.metric("Avg Population", f"{ex_pop:,.0f}")

    with em4:
        risk_text = (
            "⚠ Under-policed"
            if not np.isnan(ex_cps) and ex_cps > cps_thresh
            else "Within threshold"
        )

        st.metric(
            "Crimes per Station",
            f"{ex_cps:,.0f}" if not np.isnan(ex_cps) else "N/A",
            delta=risk_text,
            delta_color="inverse",
        )

    ec1, ec2 = st.columns([1.5, 1])

    with ec1:
        ex_monthly = (
            ex_crime.groupby("Month")["Incident_Count"]
            .sum()
            .reset_index()
        )

        fig_ex_trend = go.Figure()

        fig_ex_trend.add_trace(
            go.Scatter(
                x=ex_monthly["Month"],
                y=ex_monthly["Incident_Count"],
                mode="lines+markers",
                name=explore_lga,
                fill="tozeroy",
                fillcolor="rgba(96,165,250,0.15)",
                line=dict(color="#2563EB", width=3),
                marker=dict(size=7, color="#1E3A8A", line=dict(color="white", width=1.2)),
                hovertemplate="<b>%{x|%b %Y}</b><br>Incidents: <b>%{y:,}</b><extra></extra>",
            )
        )

        themed(fig_ex_trend, 320)
        fig_ex_trend.update_layout(title=f"{explore_lga}: Monthly Crime Trend")
        st.plotly_chart(fig_ex_trend, use_container_width=True)

    with ec2:
        ex_off = (
            ex_crime.groupby("Offence category")["Incident_Count"]
            .sum()
            .sort_values(ascending=False)
            .head(8)
            .reset_index()
        )

        PIE_COLORS = [
            "#DC2626",
            "#2563EB",
            "#3B82F6",
            "#60A5FA",
            "#93C5FD",
            "#BFDBFE",
            "#DBEAFE",
            "#EFF6FF",
        ]

        fig_ex_pie = px.pie(
            ex_off,
            values="Incident_Count",
            names="Offence category",
            color_discrete_sequence=PIE_COLORS,
            hole=0.45,
        )

        fig_ex_pie.update_traces(
            hovertemplate="<b>%{label}</b><br>%{value:,} incidents<br>(%{percent})<extra></extra>",
            textfont_size=10,
            marker=dict(line=dict(color="white", width=2)),
        )

        themed(fig_ex_pie, 320)
        fig_ex_pie.update_layout(title=f"{explore_lga}: Offence Mix")
        st.plotly_chart(fig_ex_pie, use_container_width=True)

    ex_yr = (
        ex_crime.groupby(["Year", "Offence category"])["Incident_Count"]
        .sum()
        .reset_index()
    )

    top3_sorted = (
        ex_crime.groupby("Offence category")["Incident_Count"]
        .sum()
        .nlargest(3)
        .index
        .tolist()
    )

    ex_yr_top = ex_yr[ex_yr["Offence category"].isin(top3_sorted)].copy()

    if len(top3_sorted) >= 3:
        color_map = {
            top3_sorted[0]: "#DC2626",
            top3_sorted[1]: "#2563EB",
            top3_sorted[2]: "#60A5FA",
        }
    else:
        color_map = {}

    fig_ex_yr = px.bar(
        ex_yr_top,
        x="Year",
        y="Incident_Count",
        color="Offence category",
        barmode="group",
        color_discrete_map=color_map,
        labels={
            "Incident_Count": "Incidents",
            "Offence category": "Offence",
        },
    )

    themed(fig_ex_yr, 280)

    fig_ex_yr.update_layout(
        title=f"{explore_lga}: Annual Breakdown — Top 3 Offences",
        xaxis=dict(tickmode="linear"),
    )

    fig_ex_yr.update_traces(
        marker_line_color="white",
        marker_line_width=1,
    )

    st.plotly_chart(fig_ex_yr, use_container_width=True)

else:
    st.info(f"No data available for {explore_lga} in the selected filters.")

# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    """
<div style="display:flex;justify-content:space-between;align-items:flex-start;
     color:#6e7681;font-size:.75rem;padding:6px 0 20px;line-height:1.7;">
  <div>
    <b style="color:#8b949e;">NSW Crime Intelligence Dashboard</b> · Data Narrative · 2021–2025<br>
    <b>Crime data:</b> NSW Bureau of Crime Statistics &amp; Research (BOCSAR)<br>
    <b>Population:</b> ABS Estimated Resident Population (ERP)<br>
    <b>Policing:</b> NSW Police Force GIS station records
  </div>
  <div style="text-align:right;">
    <b style="color:#8b949e;">Narrative Arc:</b> Martini Glass<br>
    Acts 1–5: author-driven story → Act 6: user-driven sandbox<br>
    Built with Streamlit · Plotly · Python
  </div>
</div>
""",
    unsafe_allow_html=True,
)