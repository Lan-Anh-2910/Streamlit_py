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

# --- Debug info ---
st.write("🧪 Các cột hiện tại:")
st.write(filtered_df.columns.tolist())

st.write("🧪 Dữ liệu Latitude/Longitude (5 dòng đầu):")
if "Latitude" in filtered_df.columns and "Longitude" in filtered_df.columns:
    st.write(filtered_df[["Latitude", "Longitude"]].head())

# --- Plot map (với kiểm tra an toàn) ---
if (
    not filtered_df.empty
    and "Latitude" in filtered_df.columns
    and "Longitude" in filtered_df.columns
    and filtered_df["Latitude"].notnull().any()
    and filtered_df["Longitude"].notnull().any()
):
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
else:
    st.warning("⚠️ Không có dữ liệu phù hợp hoặc thiếu cột tọa độ hợp lệ!")

# --- Show table ---
st.dataframe(filtered_df)
