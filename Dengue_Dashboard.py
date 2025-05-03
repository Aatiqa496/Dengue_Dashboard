import streamlit as st
import pandas as pd
import plotly.express as px

# Load your dataset
@st.cache_data
def load_data():
    df = pd.read_csv("dengue_data.csv")  # Replace with your dataset
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
year = st.sidebar.multiselect("Select Year", df["year"].unique(), default=df["year"].unique())
region = st.sidebar.multiselect("Select Region", df["region"].unique(), default=df["region"].unique())

# Filter data based on selection
filtered_df = df[(df["year"].isin(year)) & (df["region"].isin(region))]

# Title
st.title("🦟 Dengue Surveillance Dashboard")

# Summary Metrics
st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Cases", int(filtered_df["cases"].sum()))
col2.metric("Total Deaths", int(filtered_df["deaths"].sum()))
col3.metric("Recovery Rate (%)", round(100 * (filtered_df["recoveries"].sum() / filtered_df["cases"].sum()), 2))

# Time series plot
st.subheader("📈 Cases Over Time")
cases_over_time = filtered_df.groupby("year")["cases"].sum().reset_index()
fig = px.line(cases_over_time, x="year", y="cases", title="Yearly Dengue Cases")
st.plotly_chart(fig)

# Map plot (assuming you have lat/lon columns)
if "latitude" in df.columns and "longitude" in df.columns:
    st.subheader("🗺️ Geographic Spread")
    fig_map = px.scatter_mapbox(
        filtered_df,
        lat="latitude",
        lon="longitude",
        size="cases",
        color="region",
        hover_name="region",
        mapbox_style="open-street-map",
        title="Dengue Hotspots"
    )
    st.plotly_chart(fig_map)

# Raw data
st.subheader("🧾 Raw Data")
st.dataframe(filtered_df)

