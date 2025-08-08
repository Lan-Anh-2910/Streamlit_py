import streamlit as st
import pandas as pd
import plotly.express as px

# --- Load data ---
df = pd.read_csv("Overall.csv")

# --- Clean column names ---
df.columns = df.columns.str.strip()  # ✅ Xử lý lỗi tên cột thừa dấu cách

st.set_page_config(layout="wide")
st.title("🗺️ Bản đồ Site tại Việt Nam")

# --- Sidebar filters ---
region_filter = st.sidebar.multiselect("Chọn Region", df["Region"].dropna().unique())
province_filter = st.sidebar.multiselect("Chọn Tỉnh/Thành", df["Province"].dropna().unique())
status_filter = st.sidebar.multiselect("Chọn Site Status", df["Site Status"].dropna().unique())

# --- Filter data ---
filtered_df = df.copy()
if region_filter:
    filtered_df = filtered_df[filtered_df["Region"].isin(region_filter)]
if province_filter:
    filtered_df = filtered_df[filtered_df["Province"].isin(province_filter)]
if status_filter:
    filtered_df = filtered_df[filtered_df["Site Status"].isin(status_filter)]

# --- Ensure valid Latitude/Longitude ---
filtered_df = filtered_df.dropna(subset=["Latitude", "Longitude"])
filtered_df = filtered_df[filtered_df["Latitude"] != ""]
filtered_df = filtered_df[filtered_df["Longitude"] != ""]

try:
    # --- Plot map ---
    if not filtered_df.empty:
        fig = px.scatter_mapbox(
            filtered_df,
            lat="Latitude",
            lon="Longitude",
            color="Site Status",
            hover_name="Name",  # ✅ Đảm bảo đúng tên cột sau khi strip
            zoom=5,
            mapbox_style="open-street-map",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Không có dữ liệu phù hợp để hiển thị trên bản đồ.")
except Exception as e:
    st.error(f"Đã xảy ra lỗi khi hiển thị bản đồ: {e}")
