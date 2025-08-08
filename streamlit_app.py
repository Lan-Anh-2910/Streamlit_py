# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load data ---
df = pd.read_csv("Overall.csv")

st.set_page_config(layout="wide")
st.title("Bản đồ Site tại Việt Nam")

# --- Sidebar filters ---
region_filter = st.sidebar.multiselect("Chọn Region", df["Region"].unique())
province_filter = st.sidebar.multiselect("Chọn Tỉnh/Thành", df["Province"].unique())
status_filter = st.sidebar.multiselect("Chọn Site Status", df["Site Status"].unique())

# --- Filter data ---
filtered_df = df.copy()
if region_filter:
    filtered_df = filtered_df[filtered_df["Region"].isin(region_filter)]
if province_filter:
    filtered_df = filtered_df[filtered_df["Province"].isin(province_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df["Site Status"].isin(status_filter)]

# --- Plot map ---
st.write("Filtered DataFrame:")
st.dataframe(filtered_df)
fig = px.scatter_mapbox(
    filtered_df,
    lat="Latitude",
    lon="Longitude",
    color="Site Status",
    hover_name="Site Name",
    zoom=5,
    mapbox_style="open-street-map",
    height=600
)
st.plotly_chart(fig, use_container_width=True)

# --- Show table ---
st.dataframe(filtered_df)

