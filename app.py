import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

CSV_PATH = "Melbourne_Sydney_Nov.csv"

st.set_page_config(page_title="AU Trip · Nov 2025", layout="wide", page_icon="✈")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background-color: #090909; }
.block-container { padding: 2rem 2rem 4rem 2rem; max-width: 1400px; }

/* Cards */
.card {
    background: #111111;
    border: 1px solid #1f1f1f;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 16px;
}
.card-sm {
    background: #111111;
    border: 1px solid #1f1f1f;
    border-radius: 8px;
    padding: 16px 20px;
}

/* Section label */
.label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 4px;
}

/* Big number */
.big-num {
    font-size: 28px;
    font-weight: 700;
    color: #fff;
    line-height: 1.1;
}
.big-num-sm {
    font-size: 18px;
    font-weight: 600;
    color: #fff;
}

/* Sub text */
.sub { font-size: 12px; color: #555; margin-top: 2px; }

/* Page title */
.page-title {
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 2px;
}
.page-sub { font-size: 13px; color: #555; margin-bottom: 28px; }

/* Section header */
.section-header {
    font-size: 13px;
    font-weight: 600;
    color: #888;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin: 28px 0 12px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #1a1a1a;
}

/* Badge */
.badge {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    color: #888;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    font-weight: 500;
}

/* Progress bar */
.progress-wrap { margin: 8px 0; }
.progress-label { display: flex; justify-content: space-between; font-size: 12px; color: #666; margin-bottom: 4px; }
.progress-track { background: #1a1a1a; border-radius: 3px; height: 4px; width: 100%; }
.progress-fill { height: 4px; border-radius: 3px; }

#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stSidebar"] { background: #0d0d0d; border-right: 1px solid #1a1a1a; }

/* Mobile responsive */
@media (max-width: 768px) {
    .block-container { padding: 1rem !important; }
    .big-num { font-size: 20px !important; }
    div[data-testid="column"] { min-width: 100% !important; flex: 1 1 100% !important; }
    .page-title { font-size: 18px !important; }
}
</style>
""", unsafe_allow_html=True)

auto_refresh = st.sidebar.checkbox("Auto-refresh (every 3s)", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="label">Trip</div><div style="color:#fff;font-size:14px;font-weight:600;">Melbourne & Sydney</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="label" style="margin-top:12px">Duration</div><div style="color:#fff;font-size:14px;">7 Nov – 20 Nov 2025</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="label" style="margin-top:12px">Pax</div><div style="color:#fff;font-size:14px;">Aaron & Andrea</div>', unsafe_allow_html=True)

def parse_rm(val):
    if pd.isna(val): return None
    val = str(val).replace("RM", "").replace(",", "").strip()
    try: return float(val)
    except: return None

def rm(val, decimals=0):
    if val is None: return "—"
    return f"RM {val:,.{decimals}f}"

def show(data):
    st.dataframe(pd.DataFrame(data), hide_index=True, use_container_width=True)

df = pd.read_csv(CSV_PATH, header=None)

def get(r, c):
    try:
        v = df.iloc[r, c]
        return "" if pd.isna(v) else str(v).strip().replace("\r\n", "\n")
    except: return ""

def lounge_url(val):
    return val if val.startswith("http") else ""

# Parse data
flight_total = sum(filter(None, [parse_rm(get(r,7)) for r in [4,5,6,7,8]]))
accom_total  = sum(filter(None, [parse_rm(get(r,7)) for r in [13,14]]))
food_total   = sum(filter(None, [parse_rm(get(r,4)) for r in [19,20]]))
transport_total = sum(filter(None, [parse_rm(get(r,4)) for r in [25,26]]))
act_total    = sum(filter(None, [parse_rm(get(r,2)) for r in [32,33,34]]))
grand_total  = flight_total + accom_total + food_total + transport_total + act_total
aaron        = parse_rm(get(37,1))
andrea       = parse_rm(get(38,1))

# Page title
st.markdown('<div class="page-title">AU Trip Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Melbourne & Sydney · November 2025 · Two Pax</div>', unsafe_allow_html=True)

# Top KPI row
kpi_items = [
    ("Grand Total",     rm(grand_total),    "All expenses"),
    ("Flights",         rm(flight_total),   "5 segments"),
    ("Accommodation",   rm(accom_total),    "9 nights"),
    ("Aaron",           rm(aaron) if aaron else "TBD", "Flights + hotel"),
    ("Andrea",          rm(andrea) if andrea else "TBD", "Food"),
]
r1, r2 = st.columns(2), st.columns(3)
for i, (label, val, sub) in enumerate(kpi_items):
    col = r1[i] if i < 2 else r2[i - 2]
    with col:
        st.markdown(f"""
        <div class="card-sm">
            <div class="label">{label}</div>
            <div class="big-num">{val}</div>
            <div class="sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

# Charts row
st.markdown('<div class="section-header">Breakdown</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns([1, 1])

categories = ["Flights", "Accommodation", "Food", "Transport", "Activities"]
values = [flight_total, accom_total, food_total, transport_total, act_total]
colors = ["#7c6aff", "#3b82f6", "#22c55e", "#f59e0b", "#ec4899"]

with ch1:
    fig_donut = go.Figure(go.Pie(
        labels=categories,
        values=values,
        hole=0.65,
        marker=dict(colors=colors, line=dict(color="#090909", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>RM %{value:,.0f}<br>%{percent}<extra></extra>"
    ))
    fig_donut.add_annotation(
        text=f"<b>{rm(grand_total)}</b>",
        x=0.5, y=0.5, font=dict(size=16, color="white"), showarrow=False
    )
    fig_donut.update_layout(
        paper_bgcolor="#111111", plot_bgcolor="#111111",
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(font=dict(color="#888", size=12), bgcolor="rgba(0,0,0,0)"),
        height=280,
        title=dict(text="Expense Distribution", font=dict(color="#666", size=12), x=0.02)
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

with ch2:
    fig_bar = go.Figure(go.Bar(
        x=categories,
        y=values,
        marker=dict(color=colors, line=dict(width=0)),
        text=[rm(v) for v in values],
        textposition="outside",
        textfont=dict(color="#666", size=11),
        hovertemplate="<b>%{x}</b><br>RM %{y:,.0f}<extra></extra>"
    ))
    fig_bar.update_layout(
        paper_bgcolor="#111111", plot_bgcolor="#111111",
        margin=dict(t=40, b=20, l=20, r=20),
        xaxis=dict(showgrid=False, tickfont=dict(color="#666", size=12), linecolor="#1a1a1a"),
        yaxis=dict(showgrid=True, gridcolor="#1a1a1a", tickfont=dict(color="#555", size=11), linecolor="#1a1a1a"),
        height=280,
        title=dict(text="Cost by Category", font=dict(color="#666", size=12), x=0.02),
        bargap=0.4
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# Budget progress bars
st.markdown('<div class="section-header">Budget vs Estimate</div>', unsafe_allow_html=True)
estimate = parse_rm(get(39,1)) or grand_total
pct = min((grand_total / estimate) * 100, 100) if estimate else 0
bar_color = "#22c55e" if pct < 85 else "#f59e0b" if pct < 100 else "#ef4444"

for label, val, total, color in [
    ("Flights",       flight_total,    grand_total, "#7c6aff"),
    ("Accommodation", accom_total,     grand_total, "#3b82f6"),
    ("Food",          food_total,      grand_total, "#22c55e"),
    ("Transport",     transport_total, grand_total, "#f59e0b"),
    ("Activities",    act_total,       grand_total, "#ec4899"),
]:
    p = round((val / total) * 100) if total else 0
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label"><span>{label}</span><span style="color:#fff">{rm(val)} &nbsp;<span style="color:#444">({p}%)</span></span></div>
        <div class="progress-track"><div class="progress-fill" style="width:{p}%;background:{color}"></div></div>
    </div>
    """, unsafe_allow_html=True)

# Tables
st.markdown('<div class="section-header">Flights</div>', unsafe_allow_html=True)
notes = [get(r,8) for r in [4,5,6,7,8]]
flights_df = pd.DataFrame({
    "Date":        [get(r,0) for r in [4,5,6,7,8]],
    "Destination": [get(r,1) for r in [4,5,6,7,8]],
    "Departure":   [get(r,2) for r in [4,5,6,7,8]],
    "Arrival":     [get(r,3) for r in [4,5,6,7,8]],
    "Airline":     [get(r,4) for r in [4,5,6,7,8]],
    "Flight No.":  [get(r,5) for r in [4,5,6,7,8]],
    "Dep / Arr":   [get(r,6) for r in [4,5,6,7,8]],
    "Cost":        [get(r,7) for r in [4,5,6,7,8]],
    "Lounge":      [lounge_url(n) for n in notes],
})
st.dataframe(flights_df, hide_index=True, use_container_width=True, column_config={
    "Lounge": st.column_config.LinkColumn("Lounge", display_text="Available")
})

st.markdown('<div class="section-header">Accommodation</div>', unsafe_allow_html=True)
show({
    "Date":         [get(r,0) for r in [13,14]],
    "City":         [get(r,1) for r in [13,14]],
    "Accommodation":[get(r,2) for r in [13,14]],
    "Check In":     [get(r,3) for r in [13,14]],
    "Check Out":    [get(r,4) for r in [13,14]],
    "Nights":       [get(r,5) for r in [13,14]],
    "Budget/Night": [get(r,6) for r in [13,14]],
    "Total":        [get(r,7) for r in [13,14]],
})

tl, tr = st.columns(2)
with tl:
    st.markdown('<div class="section-header">Food</div>', unsafe_allow_html=True)
    show({
        "Dates":          [get(r,0) for r in [19,20]],
        "City":           [get(r,1) for r in [19,20]],
        "Days":           [get(r,2) for r in [19,20]],
        "Daily Estimate": [get(r,3) for r in [19,20]],
        "Total":          [get(r,4) for r in [19,20]],
    })

with tr:
    st.markdown('<div class="section-header">Transportation</div>', unsafe_allow_html=True)
    show({
        "Dates":          [get(r,0) for r in [25,26]],
        "City":           [get(r,1) for r in [25,26]],
        "Days":           [get(r,2) for r in [25,26]],
        "Daily Estimate": [get(r,3) for r in [25,26]],
        "Total":          [get(r,4) for r in [25,26]],
        "Notes":          [get(r,5) for r in [25,26]],
    })

st.markdown('<div class="section-header">Activities & Utilities</div>', unsafe_allow_html=True)
show({
    "Item":           [get(r,1) for r in [32,33,34]],
    "Cost (Two Pax)": [get(r,2) for r in [32,33,34]],
})

if auto_refresh:
    time.sleep(3)
    st.rerun()
