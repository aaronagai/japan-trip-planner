import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

CSV_PATH = "Japan_Trip.csv"

st.set_page_config(page_title="Japan Trip Planner", layout="wide", page_icon="🇯🇵")

import streamlit.components.v1 as components

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp { background-color: #090909; }
.block-container { padding: 2rem 2rem 4rem 2rem; max-width: 1400px; }

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

.label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 4px;
}

.big-num {
    font-size: 28px;
    font-weight: 700;
    color: #fff;
    line-height: 1.1;
}

.sub { font-size: 12px; color: #555; margin-top: 2px; }

.page-title {
    font-size: 22px;
    font-weight: 700;
    color: #fff;
    margin-bottom: 2px;
}
.page-sub { font-size: 13px; color: #555; margin-bottom: 28px; }

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

.progress-wrap { margin: 8px 0; }
.progress-label { display: flex; justify-content: space-between; font-size: 12px; color: #666; margin-bottom: 4px; }
.progress-track { background: #1a1a1a; border-radius: 3px; height: 4px; width: 100%; }
.progress-fill { height: 4px; border-radius: 3px; }

.stPlotlyChart { animation: fadeInUp 0.7s ease-out; }
.card-sm { animation: fadeInUp 0.5s ease-out; }
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

#MainMenu, footer, header { visibility: hidden; }

div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
details { border: none !important; box-shadow: none !important; }
details summary { border: none !important; }
.streamlit-expanderHeader { border: none !important; box-shadow: none !important; }
.streamlit-expanderContent { border: none !important; }
div[data-testid="stSidebar"] { background: #0d0d0d; border-right: 1px solid #1a1a1a; }

@media (max-width: 768px) {
    .block-container { padding: 1rem !important; }
    .big-num { font-size: 20px !important; }
    div[data-testid="column"] { min-width: 100% !important; flex: 1 1 100% !important; }
    .page-title { font-size: 18px !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
auto_refresh = st.sidebar.checkbox("Auto-refresh (every 3s)", value=True)
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="label">Trip</div><div style="color:#fff;font-size:14px;font-weight:600;">Japan</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="label" style="margin-top:12px">Duration</div><div style="color:#fff;font-size:14px;">TBD</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="label" style="margin-top:12px">Pax</div><div style="color:#fff;font-size:14px;">TBD & TBD</div>', unsafe_allow_html=True)

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
flight_total    = sum(filter(None, [parse_rm(get(r,7)) for r in [4,5,6,7,8]]))
accom_total     = sum(filter(None, [parse_rm(get(r,7)) for r in [13,14]]))
food_total      = sum(filter(None, [parse_rm(get(r,4)) for r in [19,20]]))
transport_total = sum(filter(None, [parse_rm(get(r,4)) for r in [25,26]]))
act_total       = sum(filter(None, [parse_rm(get(r,2)) for r in [32,33,34]]))
grand_total     = flight_total + accom_total + food_total + transport_total + act_total
t1              = parse_rm(get(39,1))
t2              = parse_rm(get(40,1))

# Page title
st.markdown('<div class="page-title">Japan Trip Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Japan · TBD · Two Pax</div>', unsafe_allow_html=True)

# KPI row
kpi_items = [
    ("Grand Total",   rm(grand_total),  "All expenses"),
    ("Flights",       rm(flight_total), "5 segments"),
    ("Accommodation", rm(accom_total),  "TBD nights"),
    ("Food",          rm(food_total),   "All cities"),
    ("Transport",     rm(transport_total), "All cities"),
]
kpi_html = '<div style="background:#111111;border:1px solid #1f1f1f;border-radius:10px;display:flex;overflow:hidden;margin-bottom:16px;">'
for i, (label, val, sub) in enumerate(kpi_items):
    border = "border-left:1px solid #1f1f1f;" if i > 0 else ""
    kpi_html += f"""
    <div style="flex:1;padding:20px 24px;{border}">
        <div class="label">{label}</div>
        <div class="big-num">{val}</div>
        <div class="sub">{sub}</div>
    </div>"""
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)

# Charts
st.markdown('<div class="section-header">Breakdown</div>', unsafe_allow_html=True)
ch1, ch2 = st.columns([1, 1])

categories = ["Flights", "Accommodation", "Food", "Transport", "Utilities"]
values = [flight_total, accom_total, food_total, transport_total, act_total]
colors = ["#ff6b6b", "#ffa94d", "#ffd43b", "#69db7c", "#74c0fc"]

with ch1:
    fig_donut = go.Figure(go.Pie(
        labels=categories,
        values=values if any(v > 0 for v in values) else [1,1,1,1,1],
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
    t1_contrib = t1 or 0
    t2_contrib = t2 or 0
    fig_contrib = go.Figure(data=[
        go.Bar(name="Traveller 1", y=["Contribution"], x=[t1_contrib], orientation="h", marker_color="#ff6b6b", width=0.3),
        go.Bar(name="Traveller 2", y=["Contribution"], x=[t2_contrib], orientation="h", marker_color="#74c0fc", width=0.3),
    ])
    fig_contrib.update_layout(
        paper_bgcolor="#111111", plot_bgcolor="#111111",
        margin=dict(t=40, b=20, l=60, r=20),
        barmode="stack",
        xaxis=dict(showgrid=True, gridcolor="#1a1a1a", tickfont=dict(color="#555", size=11), linecolor="#1a1a1a"),
        yaxis=dict(showgrid=False, tickfont=dict(color="#888", size=12), linecolor="#1a1a1a"),
        height=180,
        title=dict(text="Contribution Split", font=dict(color="#666", size=12), x=0.02),
        legend=dict(font=dict(color="#888", size=12), bgcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig_contrib, use_container_width=True, config={"displayModeBar": False})

# Progress bars
st.markdown('<div class="section-header">Budget vs Estimate</div>', unsafe_allow_html=True)
for label, val, total, color in [
    ("Flights",       flight_total,    grand_total, "#ff6b6b"),
    ("Accommodation", accom_total,     grand_total, "#ffa94d"),
    ("Food",          food_total,      grand_total, "#ffd43b"),
    ("Transport",     transport_total, grand_total, "#69db7c"),
    ("Utilities",     act_total,       grand_total, "#74c0fc"),
]:
    p = round((val / total) * 100) if total else 0
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label"><span>{label}</span><span style="color:#fff">{rm(val)} &nbsp;<span style="color:#444">({p}%)</span></span></div>
        <div class="progress-track"><div class="progress-fill" style="width:{p}%;background:{color}"></div></div>
    </div>
    """, unsafe_allow_html=True)

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
        "Date":          [get(r,0) for r in [13,14]],
        "City":          [get(r,1) for r in [13,14]],
        "Accommodation": [get(r,2) for r in [13,14]],
        "Check In":      [get(r,3) for r in [13,14]],
        "Check Out":     [get(r,4) for r in [13,14]],
        "Nights":        [get(r,5) for r in [13,14]],
        "Budget/Night":  [get(r,6) for r in [13,14]],
        "Total":         [get(r,7) for r in [13,14]],
    })

tl, tr = st.columns(2)
with tl:
    with st.expander("Food"):
        show({
            "Dates":          [get(r,0) for r in [19,20]],
            "City":           [get(r,1) for r in [19,20]],
            "Days":           [get(r,2) for r in [19,20]],
            "Daily Estimate": [get(r,3) for r in [19,20]],
            "Total":          [get(r,4) for r in [19,20]],
        })

with tr:
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
