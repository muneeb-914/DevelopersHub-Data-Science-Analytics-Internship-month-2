"""
Task 5: Interactive Business Dashboard — Global Superstore
Author: Muneeb Ur Rehman
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0d1117; color: #e6edf3; }
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border-right: 1px solid #30363d;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1c2128 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-2px); }
    .kpi-title { color: #8b949e; font-size: 0.82rem; font-weight: 600;
                 text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
    .kpi-value { color: #e6edf3; font-size: 2rem; font-weight: 700; line-height: 1.1; }
    .kpi-delta { font-size: 0.78rem; margin-top: 4px; }
    .kpi-positive { color: #3fb950; }
    .kpi-negative { color: #f85149; }
    .kpi-neutral  { color: #8b949e; }

    /* Section headers */
    .section-header {
        color: #e6edf3; font-size: 1.1rem; font-weight: 600;
        border-left: 3px solid #58a6ff;
        padding-left: 10px; margin: 1.5rem 0 0.8rem 0;
    }

    /* Plotly chart backgrounds */
    .js-plotly-plot { border-radius: 10px; }

    /* Streamlit selectbox, multiselect */
    .stSelectbox > div, .stMultiSelect > div { background: #161b22 !important; }

    /* Metric delta */
    [data-testid="metric-container"] { background: #161b22; border-radius: 8px; padding: 8px; }
</style>
""", unsafe_allow_html=True)

# ── Color Palette ────────────────────────────────────────────────────────────
COLORS = {
    "bg":       "#0d1117",
    "card":     "#161b22",
    "border":   "#30363d",
    "blue":     "#58a6ff",
    "green":    "#3fb950",
    "red":      "#f85149",
    "orange":   "#d29922",
    "purple":   "#bc8cff",
    "teal":     "#39d353",
    "text":     "#e6edf3",
    "muted":    "#8b949e",
}

PALETTE = [
    "#58a6ff", "#3fb950", "#f85149", "#d29922", "#bc8cff", "#39d353",
    "#ff7b72", "#ffa657", "#79c0ff", "#a5d6ff", "#f2cc60", "#7ee787",
    "#ffab70", "#d2a8ff",
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="#0d1117",
    plot_bgcolor="#161b22",
    font=dict(color="#e6edf3", family="Inter, sans-serif"),
    margin=dict(l=30, r=20, t=40, b=30),
    xaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d"),
    yaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d"),
)

# ── Data Loading ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_file = Path(__file__).parent / "data" / "Global_Superstore2.csv"
    if not data_file.exists():
        raise FileNotFoundError(f"Dataset not found: {data_file}")

    last_error = None
    for encoding in ("utf-8", "utf-8-sig", "cp1252", "latin1"):
        try:
            df = pd.read_csv(data_file, encoding=encoding)
            break
        except UnicodeDecodeError as exc:
            last_error = exc
    else:
        raise last_error
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True, errors="coerce")
    if df["Order Date"].isna().any():
        bad_dates = df["Order Date"].isna().sum()
        raise ValueError(f"{bad_dates} rows have invalid Order Date values.")

    df["Year"]    = df["Order Date"].dt.year
    df["Month"]   = df["Order Date"].dt.month
    df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)
    df["Profit Margin %"] = np.where(
        df["Sales"].ne(0),
        df["Profit"] / df["Sales"] * 100,
        0,
    ).round(2)
    return df

df_raw = load_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔎 Filters")
    st.markdown("---")

    # Region
    regions_avail = ["All"] + sorted(df_raw["Region"].unique().tolist())
    selected_region = st.selectbox("🌍 Region", regions_avail)

    # Category
    cats_avail = ["All"] + sorted(df_raw["Category"].unique().tolist())
    selected_cat = st.selectbox("📦 Category", cats_avail)

    # Sub-Category (dynamic)
    if selected_cat != "All":
        subcats_avail = ["All"] + sorted(df_raw[df_raw["Category"] == selected_cat]["Sub-Category"].unique().tolist())
    else:
        subcats_avail = ["All"] + sorted(df_raw["Sub-Category"].unique().tolist())
    selected_subcat = st.selectbox("🏷️ Sub-Category", subcats_avail)

    # Segment
    segs_avail = ["All"] + sorted(df_raw["Segment"].unique().tolist())
    selected_seg = st.selectbox("👥 Segment", segs_avail)

    # Year range
    years = sorted(df_raw["Year"].unique().tolist())
    year_range = st.select_slider(
        "📅 Year Range",
        options=years,
        value=(min(years), max(years))
    )

    st.markdown("---")
    st.markdown(
        "<div style='color:#8b949e; font-size:0.75rem; text-align:center;'>"
        "Global Superstore Dashboard<br>by Muneeb Ur Rehman</div>",
        unsafe_allow_html=True
    )

# ── Apply Filters ─────────────────────────────────────────────────────────────
df = df_raw.copy()
if selected_region != "All":
    df = df[df["Region"] == selected_region]
if selected_cat != "All":
    df = df[df["Category"] == selected_cat]
if selected_subcat != "All":
    df = df[df["Sub-Category"] == selected_subcat]
if selected_seg != "All":
    df = df[df["Segment"] == selected_seg]
df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

if df.empty:
    st.warning("No records match the selected filters. Adjust the sidebar filters to continue.")
    st.stop()

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown(
    """<h1 style="color:#e6edf3; font-size:1.8rem; font-weight:700; margin-bottom:0.2rem;">
    📊 Global Superstore — Business Intelligence Dashboard</h1>
    <p style="color:#8b949e; font-size:0.9rem; margin-top:0;">
    Interactive sales, profit & segment performance analysis</p>""",
    unsafe_allow_html=True
)
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
total_sales    = df["Sales"].sum()
total_profit   = df["Profit"].sum()
total_orders   = df["Order ID"].nunique()
avg_margin     = (total_profit / total_sales * 100) if total_sales else 0
total_qty      = df["Quantity"].sum()
avg_discount   = df["Discount"].mean() * 100

# Compare to full dataset for delta
full_sales    = df_raw["Sales"].sum()

kpis = [
    ("💰 Total Sales",     f"${total_sales:,.0f}",    f"{total_sales/full_sales*100:.1f}% of total" if full_sales else "0.0% of total",  "neutral"),
    ("📈 Total Profit",    f"${total_profit:,.0f}",   f"Margin: {avg_margin:.1f}%",                   "positive" if total_profit > 0 else "negative"),
    ("🛒 Total Orders",    f"{total_orders:,}",       f"Qty sold: {total_qty:,}",                     "neutral"),
    ("🏷️ Avg Discount",    f"{avg_discount:.1f}%",    "Applied to orders",                            "neutral"),
]

cols = st.columns(4)
for col, (title, value, delta, delta_type) in zip(cols, kpis):
    with col:
        delta_class = f"kpi-{delta_type}"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-delta {delta_class}">{delta}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Row 1: Sales Trend + Region Breakdown ─────────────────────────────────────
c1, c2 = st.columns([3, 2])

with c1:
    st.markdown('<div class="section-header">📅 Monthly Sales & Profit Trend</div>', unsafe_allow_html=True)
    monthly = (
        df.groupby(df["Order Date"].dt.to_period("M").astype(str))
          .agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
          .reset_index()
          .rename(columns={"Order Date":"Period"})
    )

    fig_trend = make_subplots(specs=[[{"secondary_y": True}]])
    fig_trend.add_trace(
        go.Bar(x=monthly["Period"], y=monthly["Sales"],
               name="Sales", marker_color=COLORS["blue"], opacity=0.7),
        secondary_y=False
    )
    fig_trend.add_trace(
        go.Scatter(x=monthly["Period"], y=monthly["Profit"],
                   name="Profit", line=dict(color=COLORS["green"], width=2.5),
                   mode="lines+markers", marker=dict(size=4)),
        secondary_y=True
    )
    fig_trend.update_layout(
        **PLOTLY_LAYOUT,
        height=320,
        title=dict(text="Sales (bars) & Profit (line)", font=dict(size=13)),
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
        bargap=0.2,
    )
    fig_trend.update_yaxes(title_text="Sales ($)", secondary_y=False,
                           gridcolor="#21262d", zerolinecolor="#30363d")
    fig_trend.update_yaxes(title_text="Profit ($)", secondary_y=True,
                           gridcolor="#21262d", zerolinecolor="#30363d")
    st.plotly_chart(fig_trend, use_container_width=True)

with c2:
    st.markdown('<div class="section-header">🌍 Sales by Region</div>', unsafe_allow_html=True)
    region_df = df.groupby("Region").agg(Sales=("Sales","sum"), Profit=("Profit","sum")).reset_index()
    fig_region = go.Figure(go.Pie(
        labels=region_df["Region"],
        values=region_df["Sales"],
        hole=0.5,
        marker=dict(colors=PALETTE[:len(region_df)],
                    line=dict(color=COLORS["bg"], width=2)),
        textinfo="label+percent",
        textfont=dict(size=12, color="#e6edf3"),
    ))
    fig_region.update_layout(
        **PLOTLY_LAYOUT,
        height=320,
        title=dict(text="Revenue Share by Region", font=dict(size=13)),
        showlegend=False,
    )
    st.plotly_chart(fig_region, use_container_width=True)

# ── Row 2: Category Profit + Segment ──────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="section-header">📦 Profit by Category & Sub-Category</div>', unsafe_allow_html=True)
    subcat_df = (
        df.groupby(["Category","Sub-Category"])
          .agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
          .reset_index()
          .sort_values("Profit", ascending=True)
    )
    fig_cat = px.bar(
        subcat_df, x="Profit", y="Sub-Category", color="Category",
        orientation="h",
        color_discrete_map={
            "Technology": COLORS["blue"],
            "Furniture":  COLORS["orange"],
            "Office Supplies": COLORS["green"],
        },
    )
    fig_cat.update_layout(**PLOTLY_LAYOUT, height=340,
                          title=dict(text="Profit by Sub-Category", font=dict(size=13)),
                          showlegend=True, yaxis_title="", xaxis_title="Profit ($)")
    st.plotly_chart(fig_cat, use_container_width=True)

with c4:
    st.markdown('<div class="section-header">👥 Segment-wise Performance</div>', unsafe_allow_html=True)
    seg_df = (
        df.groupby("Segment")
          .agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique"))
          .reset_index()
    )
    seg_df["Margin %"] = (seg_df["Profit"] / seg_df["Sales"] * 100).round(1)

    fig_seg = go.Figure()
    fig_seg.add_trace(go.Bar(
        name="Sales",  x=seg_df["Segment"], y=seg_df["Sales"],
        marker_color=COLORS["blue"], opacity=0.85,
    ))
    fig_seg.add_trace(go.Bar(
        name="Profit", x=seg_df["Segment"], y=seg_df["Profit"],
        marker_color=COLORS["green"], opacity=0.85,
    ))
    fig_seg.update_layout(
        **PLOTLY_LAYOUT, barmode="group", height=340,
        title=dict(text="Sales & Profit by Segment", font=dict(size=13)),
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
    )
    st.plotly_chart(fig_seg, use_container_width=True)

# ── Row 3: Top 5 Customers + Discount Analysis ────────────────────────────────
c5, c6 = st.columns(2)

with c5:
    st.markdown('<div class="section-header">🏆 Top 5 Customers by Sales</div>', unsafe_allow_html=True)
    top5 = (
        df.groupby("Customer Name")
          .agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique"))
          .reset_index()
          .sort_values("Sales", ascending=False)
          .head(5)
          .sort_values("Sales", ascending=True)
    )

    fig_top5 = go.Figure()
    fig_top5.add_trace(go.Bar(
        y=top5["Customer Name"], x=top5["Sales"],
        orientation="h",
        marker=dict(
            color=top5["Profit"],
            colorscale=[[0,"#f85149"],[0.5,"#d29922"],[1,"#3fb950"]],
            showscale=True,
            colorbar=dict(title="Profit", thickness=12, len=0.8),
        ),
        text=[f"${v:,.0f}" for v in top5["Sales"]],
        textposition="outside",
        textfont=dict(color="#e6edf3", size=11),
    ))
    fig_top5.update_layout(
        **PLOTLY_LAYOUT, height=320,
        title=dict(text="Top 5 Customers (color = profit)", font=dict(size=13)),
        xaxis_title="Total Sales ($)", yaxis_title="",
    )
    st.plotly_chart(fig_top5, use_container_width=True)

with c6:
    st.markdown('<div class="section-header">🏷️ Discount Impact on Profit Margin</div>', unsafe_allow_html=True)
    disc_df = df.copy()
    disc_df["Discount Band"] = pd.cut(
        disc_df["Discount"],
        bins=[-0.01, 0.0, 0.1, 0.2, 0.3, np.inf],
        labels=["0%","1-10%","11-20%","21-30%","31%+"]
    )
    disc_agg = (
        disc_df.groupby("Discount Band", observed=True)
               .agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Rows=("Order ID","count"))
               .reset_index()
    )
    disc_agg["Margin %"] = np.where(
        disc_agg["Sales"].ne(0),
        disc_agg["Profit"] / disc_agg["Sales"] * 100,
        0,
    )

    bar_colors = [COLORS["green"] if m > 0 else COLORS["red"] for m in disc_agg["Margin %"]]
    fig_disc = go.Figure(go.Bar(
        x=disc_agg["Discount Band"].astype(str),
        y=disc_agg["Margin %"],
        marker_color=bar_colors,
        text=[f"{v:.1f}%" for v in disc_agg["Margin %"]],
        textposition="auto",
    ))
    fig_disc.add_hline(y=0, line_color="#8b949e", line_dash="dot", line_width=1.5)
    fig_disc.update_layout(
        **PLOTLY_LAYOUT, height=320,
        title=dict(text="Weighted Profit Margin by Discount Level", font=dict(size=13)),
        xaxis_title="Discount Band", yaxis_title="Profit Margin (%)",
    )
    st.plotly_chart(fig_disc, use_container_width=True)

# ── Row 4: YoY Sales + Raw Data ───────────────────────────────────────────────
st.markdown('<div class="section-header">📆 Year-over-Year Sales by Category</div>', unsafe_allow_html=True)

yoy = df.groupby(["Year","Category"]).agg(Sales=("Sales","sum")).reset_index()
fig_yoy = px.line(
    yoy, x="Year", y="Sales", color="Category",
    markers=True,
    color_discrete_map={
        "Technology": COLORS["blue"],
        "Furniture":  COLORS["orange"],
        "Office Supplies": COLORS["green"],
    },
)
fig_yoy.update_traces(line=dict(width=2.5), marker=dict(size=8))
fig_yoy.update_layout(
    **PLOTLY_LAYOUT, height=300,
    title=dict(text="Annual Sales Trend by Category", font=dict(size=13)),
    legend=dict(orientation="h", y=1.12, x=0.5, xanchor="center"),
)
st.plotly_chart(fig_yoy, use_container_width=True)

# ── Raw Data Expander ─────────────────────────────────────────────────────────
with st.expander("🗃️ View Filtered Data Table"):
    st.markdown(f"**{len(df):,} records** after applying filters")
    show_cols = ["Order Date","Customer Name","Segment","Region",
                 "Category","Sub-Category","Sales","Quantity","Discount","Profit"]
    st.dataframe(
        df[show_cols].sort_values("Sales", ascending=False).head(200),
        use_container_width=True, height=300
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#8b949e; font-size:0.8rem;'>"
    "Task 5 — Interactive Business Dashboard | "
    "Muneeb Ur Rehman | BS IT, University of Sargodha | mu181842@gmail.com"
    "</div>",
    unsafe_allow_html=True
)
