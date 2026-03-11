import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

CSV_PATH = "Melbourne_Sydney_Nov.csv"

st.set_page_config(page_title="AU Trip · Nov 2026", layout="wide", page_icon="✈")

import streamlit.components.v1 as components


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

/* Chart entrance animation */
.stPlotlyChart {
    animation: fadeInUp 0.7s ease-out;
}
.card-sm {
    animation: fadeInUp 0.5s ease-out;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

#MainMenu, footer, header { visibility: hidden; }

/* Remove expander border */
div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
details { border: none !important; box-shadow: none !important; }
details summary { border: none !important; }
.streamlit-expanderHeader { border: none !important; box-shadow: none !important; }
.streamlit-expanderContent { border: none !important; }
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

# ── Dashboard ──────────────────────────────────────────────────
auto_refresh = st.sidebar.checkbox("Auto-refresh (every 3s)", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="label">Trip</div><div style="color:#fff;font-size:14px;font-weight:600;">Sydney & Melbourne</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="label" style="margin-top:12px">Duration</div><div style="color:#fff;font-size:14px;">6 Nov – 15 Nov 2026</div>', unsafe_allow_html=True)
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
aaron        = parse_rm(get(39,1))
andrea       = parse_rm(get(40,1))

# Page title
st.markdown('<div class="page-title">Australia Trip Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Sydney & Melbourne · 6 – 15 Nov 2026 · Two Pax</div>', unsafe_allow_html=True)

# Top KPI row
kpi_items = [
    ("Grand Total",    rm(grand_total),  "All expenses"),
    ("Flights",        rm(flight_total), "5 segments"),
    ("Accommodation",  rm(accom_total),  "8 nights"),
    ("Food",           rm(food_total),   "Both cities"),
    ("Transport",      rm(transport_total), "Both cities"),
    ("Utilities",      rm(act_total),    "Visa, roaming, insurance"),
]
kpi_html = '<div style="background:#111111;border:1px solid #1f1f1f;border-radius:10px;overflow:hidden;margin-bottom:16px;">'
for i, (label, val, sub) in enumerate(kpi_items):
    border = "border-top:1px solid #1f1f1f;" if i > 0 else ""
    kpi_html += f"""
    <div style="padding:16px 24px;{border}">
        <div class="label">{label}</div>
        <div style="font-size:18px;font-weight:700;color:#fff;margin:2px 0;">{val}</div>
        <div class="sub">{sub}</div>
    </div>"""
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)

# Charts row
st.markdown('<div class="section-header">Breakdown</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns([1, 1])

categories = ["Flights", "Accommodation", "Food", "Transport", "Utilities"]
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
    aaron_contrib = aaron or 0
    andrea_contrib = andrea or 0
    total_contrib = aaron_contrib + andrea_contrib
    aaron_pct = round((aaron_contrib / total_contrib) * 100) if total_contrib else 0
    andrea_pct = 100 - aaron_pct
    fig_contrib = go.Figure(data=[
        go.Bar(name="Aaron",  y=["Contribution"], x=[aaron_contrib],  orientation="h", marker_color="#7c6aff", width=0.3),
        go.Bar(name="Andrea", y=["Contribution"], x=[andrea_contrib], orientation="h", marker_color="#ec4899", width=0.3),
    ])
    fig_contrib.update_layout(
        paper_bgcolor="#111111", plot_bgcolor="#111111",
        margin=dict(t=40, b=20, l=60, r=20),
        barmode="stack",
        xaxis=dict(showgrid=True, gridcolor="#1a1a1a", tickfont=dict(color="#555", size=11), linecolor="#1a1a1a"),
        yaxis=dict(showgrid=False, tickfont=dict(color="#888", size=12), linecolor="#1a1a1a"),
        height=180,
        title=dict(text="Aaron <> Andrea Contribution", font=dict(color="#666", size=12), x=0.02),
        legend=dict(font=dict(color="#888", size=12), bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_contrib, use_container_width=True, config={"displayModeBar": False})
    components.html("""
    <script>
    setTimeout(() => {
        const plots = window.parent.document.querySelectorAll('.js-plotly-plot');
        plots.forEach(p => { try { Plotly.animate(p, null); } catch(e) {} });
    }, 500);
    </script>
    """, height=0)

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
    ("Utilities",     act_total,       grand_total, "#ec4899"),
]:
    p = round((val / total) * 100) if total else 0
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label"><span>{label}</span><span style="color:#fff">{rm(val)} &nbsp;<span style="color:#444">({p}%)</span></span></div>
        <div class="progress-track"><div class="progress-fill" style="width:{p}%;background:{color}"></div></div>
    </div>
    """, unsafe_allow_html=True)

# Calendar View
st.markdown('<div class="section-header">Calendar View</div>', unsafe_allow_html=True)

cal_mode = st.radio("", ["Travel", "Office Leave"], horizontal=True, label_visibility="collapsed")

from datetime import datetime

def parse_day(s):
    try: return int(str(s).strip().split()[0])
    except: return None

stay_map = {}
for r, color in [(13, "#3b82f6"), (14, "#22c55e")]:
    city = get(r, 1)
    cin  = parse_day(get(r, 3))
    cout = parse_day(get(r, 4))
    if city and cin and cout:
        for d in range(cin, cout):
            stay_map[d] = (city, color)

flight_map = {}
for r in [5, 6, 7]:  # Australia flights only (KUL-SYD, SYD-MEL, MEL-KUL)
    d     = parse_day(get(r, 0))
    route = get(r, 1).replace("\n", " ")
    fno   = get(r, 5)
    if d and 6 <= d <= 22:
        flight_map[d] = (route, fno)

base_dow = datetime(2026, 11, 6).weekday()
cells_html = ""
for _ in range(base_dow):
    cells_html += '<div></div>'

if cal_mode == "Travel":
    for day in range(6, 23):
        if day in flight_map:
            bg, border = "#2a1f4a", "#7c6aff"
        elif day in stay_map:
            city, color = stay_map[day]
            bg     = "#0d1a2e" if "Sydney" in city else "#0d2010"
            border = color
        else:
            bg, border = "#111111", "#1f1f1f"
        cells_html += (
            "<div style='background:" + bg + ";border:1px solid " + border + ";border-radius:6px;"
            "padding:8px 6px;min-height:48px;display:flex;align-items:flex-end;'>"
            "<div style='font-size:10px;color:#555;'>" + str(day) + "</div>"
            "</div>"
        )
    legend_html = """
<div style="display:flex;gap:16px;margin-top:8px;flex-wrap:wrap;">
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#2a1f4a;border:1px solid #7c6aff;"></div>
        <span style="font-size:13px;color:#888;">Flight day</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#0d1a2e;border:1px solid #3b82f6;"></div>
        <span style="font-size:13px;color:#888;">Sydney</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#0d2010;border:1px solid #22c55e;"></div>
        <span style="font-size:13px;color:#888;">Melbourne</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#111111;border:1px solid #1f1f1f;"></div>
        <span style="font-size:13px;color:#888;">No event</span>
    </div>
</div>"""
else:
    leave_map = {
        7:  ("#0d2010", "#22c55e"),
        8:  ("#0d2010", "#22c55e"),
        9:  ("#2a0000", "#ef4444"),
        10: ("#2a1500", "#f59e0b"),
        11: ("#2a1500", "#f59e0b"),
        12: ("#2a1500", "#f59e0b"),
        13: ("#2a1500", "#f59e0b"),
        14: ("#0d2010", "#22c55e"),
        15: ("#0d2010", "#22c55e"),
        16: ("#2a1500", "#f59e0b"),
    }
    for day in range(6, 23):
        if day in leave_map:
            bg, border = leave_map[day]
        else:
            bg, border = "#111111", "#1f1f1f"
        cells_html += (
            "<div style='background:" + bg + ";border:1px solid " + border + ";border-radius:6px;"
            "padding:8px 6px;min-height:48px;display:flex;align-items:flex-end;'>"
            "<div style='font-size:10px;color:#555;'>" + str(day) + "</div>"
            "</div>"
        )
    legend_html = """
<div style="display:flex;gap:16px;margin-top:8px;flex-wrap:wrap;">
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#0d2010;border:1px solid #22c55e;"></div>
        <span style="font-size:13px;color:#888;">Public Holiday</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#2a0000;border:1px solid #ef4444;"></div>
        <span style="font-size:13px;color:#888;">Public Holiday (Special)</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#2a1500;border:1px solid #f59e0b;"></div>
        <span style="font-size:13px;color:#888;">Office Leave</span>
    </div>
    <div style="display:flex;align-items:center;gap:6px;">
        <div style="width:12px;height:12px;border-radius:3px;background:#111111;border:1px solid #1f1f1f;"></div>
        <span style="font-size:13px;color:#888;">No event</span>
    </div>
</div>"""

headers_html = "".join(
    "<div style='text-align:center;font-size:10px;color:#444;padding:3px 0;'>" + h + "</div>"
    for h in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
)

cal_full = (
    "<link href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500&display=swap' rel='stylesheet'>"
    "<div style='font-family:Inter,sans-serif;background:#111111;border:1px solid #1f1f1f;border-radius:8px;padding:16px;'>"
    "<div style='display:grid;grid-template-columns:repeat(7,1fr);gap:5px;'>"
    + headers_html + cells_html +
    "</div></div>"
)
components.html(cal_full, height=420)

st.markdown(legend_html, unsafe_allow_html=True)

# Tables
st.markdown("---")
with st.expander("Flights"):
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
        "Lounge": st.column_config.LinkColumn("Lounge", display_text="Available", width="small")
    })

with st.expander("Accommodation"):
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

with st.expander("Food"):
    show({
        "Dates":          [get(r,0) for r in [19,20]],
        "City":           [get(r,1) for r in [19,20]],
        "Days":           [get(r,2) for r in [19,20]],
        "Daily Estimate": [get(r,3) for r in [19,20]],
        "Total":          [get(r,4) for r in [19,20]],
    })

with st.expander("Transportation"):
    show({
        "Dates":          [get(r,0) for r in [25,26]],
        "City":           [get(r,1) for r in [25,26]],
        "Days":           [get(r,2) for r in [25,26]],
        "Daily Estimate": [get(r,3) for r in [25,26]],
        "Total":          [get(r,4) for r in [25,26]],
        "Notes":          [get(r,5) for r in [25,26]],
    })

with st.expander("Utilities & Others"):
    show({
        "Item":           [get(r,1) for r in [32,33,34]],
        "Cost (Two Pax)": [get(r,2) for r in [32,33,34]],
    })

if auto_refresh:
    time.sleep(3)
    st.rerun()

