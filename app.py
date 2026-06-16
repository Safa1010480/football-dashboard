import streamlit as st
import pandas as pd
from filters import load_data, apply_filters
import charts

st.set_page_config(page_title="International Football Dashboard", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; color: #111827 !important; }
    header[data-testid="stHeader"] { background-color: #ffffff !important; }
    .stDeployButton { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stSidebar, [data-testid="stSidebar"] { background-color: #f8fafc !important; border-right: 1px solid #d1d5db; }
    h1, h2, h3, h4, h5, h6 { color: #2563eb !important; }
    p, span, div, label { color: #111827 !important; }
    .stMetric label { color: #3b82f6 !important; }
    .stMetric [data-testid="metric-value"] { color: #2563eb !important; }
    div[data-testid="metric-container"] { background: #ffffff !important; border: 1px solid #2563eb !important; border-radius: 10px; padding: 12px; }
    .stSelectbox label, .stMultiSelect label, .stSlider label, .stTextInput label { color: #2563eb !important; font-weight: bold; }
    [data-testid="stSidebar"] * { color: #111827 !important; }
    .stButton button { background-color: #2563eb !important; color: #ffffff !important; font-weight: bold; border: none; border-radius: 8px; }
    .stDownloadButton button { background-color: #ffffff !important; color: #2563eb !important; border: 1px solid #2563eb !important; border-radius: 6px; font-size: 12px; }
    .stDataFrame { background-color: #ffffff !important; color: #111827 !important; }
    .stCaption { color: #4b5563 !important; }
    .stTextInput input { background-color: #ffffff !important; color: #111827 !important; border: 1px solid #2563eb !important; border-radius: 6px; }
    .stMultiSelect [data-baseweb="select"] { background-color: #ffffff !important; border: 1px solid #2563eb !important; border-radius: 6px; }
    .stMultiSelect [data-baseweb="select"] * { background-color: #ffffff !important; color: #111827 !important; }
    .stMultiSelect [data-baseweb="tag"] { background-color: #2563eb !important; color: #ffffff !important; }
    div[data-baseweb="popover"] { background-color: #ffffff !important; border: 1px solid #2563eb !important; }
    div[data-baseweb="popover"] * { background-color: #ffffff !important; color: #111827 !important; }
    div[data-baseweb="menu"] { background-color: #ffffff !important; }
    div[data-baseweb="menu"] * { color: #111827 !important; }
    div[data-baseweb="menu"] li:hover { background-color: #2563eb22 !important; }
    .chart-desc { color: #4b5563 !important; font-size: 0.85rem; margin-bottom: 8px; font-style: italic; }
    .section-header { font-size: 1.1rem; font-weight: 700; color: #2563eb !important; border-left: 4px solid #2563eb; padding-left: 10px; margin: 1.5rem 0 0.8rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data("data/results.csv")

df = get_data()
charts.set_style()

st.title("International Men's Football Dashboard")
st.markdown("<p style='color:#4b5563'>Exploring every international match from 1872 to present — 49,000+ matches, 300+ teams, across all continents.</p>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.title("Dashboard Filters")
st.sidebar.markdown("Adjust filters — all charts update instantly.")

year_min = int(df["year"].min())
year_max = int(df["year"].max())
year_range = st.sidebar.slider("Year Range", year_min, year_max, (1950, year_max))

all_tournaments = sorted(df["tournament"].dropna().unique())
tournaments = st.sidebar.multiselect("Tournament(s)", all_tournaments)

all_teams = sorted(set(df["home_team"].unique()) | set(df["away_team"].unique()))
teams = st.sidebar.multiselect("Team(s)", all_teams)

max_goals = int(df["total_goals"].max())
score_range = st.sidebar.slider("Total Goals in Match", 0, max_goals, (0, max_goals))

search_text = st.sidebar.text_input("Search (team / city / country)", "")

if st.sidebar.button("Reset All Filters", use_container_width=True):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption("EDA Course Project")

filtered = apply_filters(df, year_range, tournaments, teams, score_range, search_text)

if len(filtered) == 0:
    st.warning("No matches found with the selected filters. Try resetting.")
    st.stop()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Matches",   f"{len(filtered):,}")
k2.metric("Avg Goals/Match", f"{filtered['total_goals'].mean():.2f}")
k3.metric("Highest Scoring", f"{int(filtered['total_goals'].max())} goals")
k4.metric("Tournaments",     filtered["tournament"].nunique())
k5.metric("Countries",       filtered["country"].nunique())

st.markdown("---")

st.markdown("<div class='section-header'>Trends Over Time</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.markdown("<p class='chart-desc'>Shows the growth of international football over time. Notice the sharp rise after the 1950s as more nations joined FIFA.</p>", unsafe_allow_html=True)
    fig = charts.line_chart(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "matches_per_year.png")
with col2:
    st.markdown("<p class='chart-desc'>Tracks average goals per match across decades. Early football was high-scoring; modern teams are more defensively organized.</p>", unsafe_allow_html=True)
    fig = charts.area_chart(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "goals_per_decade.png")

st.markdown("<div class='section-header'>Team and Tournament Performance</div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    st.markdown("<p class='chart-desc'>Ranks the top 10 nations by total match wins throughout history. Brazil leads, followed by Germany and Argentina.</p>", unsafe_allow_html=True)
    fig = charts.bar_chart(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "top_teams_wins.png")
with col4:
    st.markdown("<p class='chart-desc'>Compares how many matches each tournament has produced. Friendly matches dominate due to their frequency throughout the year.</p>", unsafe_allow_html=True)
    fig = charts.count_plot(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "matches_by_tournament.png")

st.markdown("<div class='section-header'>Goals Analysis</div>", unsafe_allow_html=True)
col5, col6, col7 = st.columns(3)
with col5:
    st.markdown("<p class='chart-desc'>Most matches end with 2 to 3 total goals. High-scoring matches above 7 goals are extremely rare.</p>", unsafe_allow_html=True)
    fig = charts.histogram(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "goals_distribution.png")
with col6:
    st.markdown("<p class='chart-desc'>Each dot is one match. Points below the diagonal line indicate a home win; points above indicate an away win.</p>", unsafe_allow_html=True)
    fig = charts.scatter_plot(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "home_vs_away_goals.png")
with col7:
    st.markdown("<p class='chart-desc'>Home teams win nearly 45% of all matches, proving that playing at home provides a significant competitive advantage.</p>", unsafe_allow_html=True)
    fig = charts.pie_chart(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "match_outcomes.png")

st.markdown("<div class='section-header'>Distributions and Correlations</div>", unsafe_allow_html=True)
col8, col9, col10 = st.columns(3)
with col8:
    st.markdown("<p class='chart-desc'>Compares goal spread across top tournaments. The dots outside the boxes represent unusually high-scoring matches.</p>", unsafe_allow_html=True)
    fig = charts.box_plot(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "goals_by_tournament.png")
with col9:
    st.markdown("<p class='chart-desc'>The wider the shape, the more common that score. Home teams consistently score slightly more goals than away teams.</p>", unsafe_allow_html=True)
    fig = charts.violin_plot(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "home_away_violin.png")
with col10:
    st.markdown("<p class='chart-desc'>Darker blue means stronger relationship. Total goals is strongly linked to both scores, but home and away scores have little correlation.</p>", unsafe_allow_html=True)
    fig = charts.heatmap(filtered)
    st.pyplot(fig)
    charts.download_button(fig, "correlation_heatmap.png")

st.markdown("<div class='section-header'>Filtered Data Preview</div>", unsafe_allow_html=True)
st.dataframe(
    filtered[["date","home_team","away_team","home_score","away_score","total_goals","tournament","city","country","outcome"]]
    .sort_values("date", ascending=False),
    use_container_width=True,
    height=300
)
st.caption(f"Showing {len(filtered):,} matches after applying filters.")
