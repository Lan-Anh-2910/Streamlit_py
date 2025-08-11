import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- Load token ---
mapbox_token = st.secrets["MAPBOX_TOKEN"]

# --- Load site data ---
sites_df = pd.read_csv("Overall.csv")
sites_df.columns = sites_df.columns.str.strip()
sites_df["Latitude"] = pd.to_numeric(sites_df["Latitude"], errors="coerce")
sites_df["Longitude"] = pd.to_numeric(sites_df["Longitude"], errors="coerce")

# --- Load route data ---
routes_df = pd.read_csv("Route.csv")
routes_df.columns = routes_df.columns.str.strip()

st.set_page_config(layout="wide")
st.title("🗺️ Bản đồ Site & Route tại Việt Nam (Mapbox Streets)")

# --- Sidebar filters ---
region_filter = st.sidebar.multiselect("Chọn Region", sites_df["Region"].dropna().unique())
province_filter = st.sidebar.multiselect("Chọn Tỉnh/Thành", sites_df["Province"].dropna().unique())
status_filter = st.sidebar.multiselect("Chọn Site Status", sites_df["Site Status"].dropna().unique())
show_route = st.sidebar.checkbox("Hiển thị Route", value=False)

# --- Apply site filters ---
filtered_sites = sites_df.copy()
if region_filter:
    filtered_sites = filtered_sites[filtered_sites["Region"].isin(region_filter)]
if province_filter:
    filtered_sites = filtered_sites[filtered_sites["Province"].isin(province_filter)]
if status_filter:
    filtered_sites = filtered_sites[filtered_sites["Site Status"].isin(status_filter)]

filtered_sites = filtered_sites.dropna(subset=["Latitude", "Longitude"])

# --- Debug ---
st.write("📊 Dữ liệu Site sau lọc:")
st.dataframe(filtered_sites)

# --- Vẽ bản đồ ---
try:
    if not filtered_sites.empty:
        fig = go.Figure()

        # 1. Thêm điểm Site
        fig.add_trace(go.Scattermapbox(
            lat=filtered_sites["Latitude"],
            lon=filtered_sites["Longitude"],
            mode="markers",
            marker=dict(size=8, color="red"),
            text=filtered_sites["Name"],
            hoverinfo="text"
        ))

        # 2. Nếu bật Route -> vẽ đường nối
        if show_route:
            for _, route in routes_df.iterrows():
                site_ids = [route["Site1"], route["Site2"], route.get("Site3")]
                site_ids = [sid for sid in site_ids if pd.notna(sid)]  # bỏ ô trống

                # Lấy tọa độ từng site trong tuyến
                coords = filtered_sites[filtered_sites["ID"].isin(site_ids)][["Latitude", "Longitude"]]
                if len(coords) >= 2:  # cần ít nhất 2 điểm để vẽ đường
                    fig.add_trace(go.Scattermapbox(
                        lat=coords["Latitude"],
                        lon=coords["Longitude"],
                        mode="lines",
                        line=dict(width=2, color="blue"),
                        hoverinfo="none"
                    ))

        fig.update_layout(
            mapbox=dict(
                accesstoken=mapbox_token,
                style="mapbox://styles/mapbox/streets-v12",
                zoom=5,
                center=dict(lat=16, lon=107)
            ),
            margin=dict(l=0, r=0, t=0, b=0),
            height=700
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("⚠️ Không có dữ liệu phù hợp để hiển thị trên bản đồ.")

except Exception as e:
    st.error("❌ Đã xảy ra lỗi khi hiển thị bản đồ.")
    st.exception(e)
