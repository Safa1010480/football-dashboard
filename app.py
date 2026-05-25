import streamlit as st
import pandas as pd
from filters import load_data, apply_filters
import charts

st.set_page_config(page_title="International Football Dashboard", page_icon="⚽", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0a0e1a !important; color: white !important; } header[data-testid="stHeader"] { background-color: #0a0e1a !important; } .stDeployButton { display: none; } #MainMenu { visibility: hidden; } footer { visibility: hidden; }
    .stSidebar, [data-testid="stSidebar"] { background-color: #0d1117 !important; }
    h1, h2, h3, h4, h5, h6 { color: #00d4ff !important; }
    p, span, div, label { color: #ffffff !important; }
    .stMetric label { color: #aaaaaa !important; }
    .stMetric [data-testid="metric-value"] { color: #00d4ff !important; }
    div[data-testid="metric-container"] { background: #1a1f2e !important; border: 1px solid #00d4ff !important; border-radius: 10px; padding: 12px; }
    .stSelectbox label, .stMultiSelect label, .stSlider label, .stTextInput label { color: #00d4ff !important; font-weight: bold; }
    .stSlider [data-baseweb="slider"] { color: white !important; }
    [data-testid="stSidebar"] * { color: #ffffff !important; }
    .stButton button { background-color: #00d4ff !important; color: #0a0e1a !important; font-weight: bold; border: none; border-radius: 8px; }
    .stDataFrame { background-color: #0d1117 !important; color: white !important; }
    .stCaption { color: #aaaaaa !important; }
    .stWarning { color: white !important; }
    .stTextInput input { background-color: #1a1f2e !important; color: #ffffff !important; border: 1px solid #00d4ff !important; border-radius: 6px; }
    .stMultiSelect [data-baseweb="select"] { background-color: #1a1f2e !important; border: 1px solid #00d4ff !important; border-radius: 6px; }
    .stMultiSelect [data-baseweb="select"] * { background-color: #1a1f2e !important; color: #ffffff !important; }
    .stMultiSelect [data-baseweb="tag"] { background-color: #00d4ff !important; color: #0a0e1a !important; }
    div[data-baseweb="popover"] { background-color: #1a1f2e !important; border: 1px solid #00d4ff !important; }
    div[data-baseweb="popover"] * { background-color: #1a1f2e !important; color: #ffffff !important; }
    div[data-baseweb="menu"] { background-color: #1a1f2e !important; }
    div[data-baseweb="menu"] * { color: #ffffff !important; }
    div[data-baseweb="menu"] li:hover { background-color: #00d4ff22 !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data("data/results.csv")

df = get_data()
charts.set_style()

st.title("⚽ International Men's Football Dashboard")
st.markdown("Exploring every international match from **1872 to present**")
st.markdown("---")

st.sidebar.title("🔍 Dashboard Filters")

year_min = int(df["year"].min())
year_max = int(df["year"].max())
year_range = st.sidebar.slider("📅 Year Range", year_min, year_max, (1950, year_max))

all_tournaments = sorted(df["tournament"].dropna().unique())
tournaments = st.sidebar.multiselect("🏆 Tournament(s)", all_tournaments)

all_teams = sorted(set(df["home_team"].unique()) | set(df["away_team"].unique()))
teams = st.sidebar.multiselect("🌍 Team(s)", all_teams)

max_goals = int(df["total_goals"].max())
score_range = st.sidebar.slider("⚽ Total Goals in Match", 0, max_goals, (0, max_goals))

search_text = st.sidebar.text_input("🔎 Search (team / city / country)", "")

if st.sidebar.button("🔄 Reset All Filters"):
    st.rerun()

filtered = apply_filters(df, year_range, tournaments, teams, score_range, search_text)

if len(filtered) == 0:
    st.warning("No matches found. Try resetting filters.")
    st.stop()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📋 Total Matches",   f"{len(filtered):,}")
k2.metric("⚽ Avg Goals/Match", f"{filtered['total_goals'].mean():.2f}")
k3.metric("🔥 Highest Scoring", f"{int(filtered['total_goals'].max())} goals")
k4.metric("🏆 Tournaments",     filtered["tournament"].nunique())
k5.metric("🌍 Countries",       filtered["country"].nunique())

st.markdown("---")

st.subheader("📈 Trends Over Time")
col1, col2 = st.columns(2)
with col1:
    st.pyplot(charts.line_chart(filtered))
with col2:
    st.pyplot(charts.area_chart(filtered))

st.subheader("🏆 Team & Tournament Performance")
col3, col4 = st.columns(2)
with col3:
    st.pyplot(charts.bar_chart(filtered))
with col4:
    st.pyplot(charts.count_plot(filtered))

st.subheader("⚽ Goals Analysis")
col5, col6, col7 = st.columns(3)
with col5:
    st.pyplot(charts.histogram(filtered))
with col6:
    st.pyplot(charts.scatter_plot(filtered))
with col7:
    st.pyplot(charts.pie_chart(filtered))

st.subheader("📊 Distributions & Correlations")
col8, col9, col10 = st.columns(3)
with col8:
    st.pyplot(charts.box_plot(filtered))
with col9:
    st.pyplot(charts.violin_plot(filtered))
with col10:
    st.pyplot(charts.heatmap(filtered))

st.subheader("📄 Filtered Data Preview")
st.dataframe(
    filtered[["date","home_team","away_team","home_score","away_score","total_goals","tournament","city","country","outcome"]]
    .sort_values("date", ascending=False),
    use_container_width=True,
    height=300
)
st.caption(f"Showing {len(filtered):,} matches after applying filters.")
