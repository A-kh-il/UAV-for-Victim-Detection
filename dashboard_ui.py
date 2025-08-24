# dashboard_ui.py

import streamlit as st
import pandas as pd
import os
from PIL import Image
import folium
from streamlit_folium import st_folium

# --- Config ---
st.set_page_config(page_title="Victim Detection Dashboard", layout="wide")

# --- Load Data ---
CSV_FILE = "detections.csv"
IMAGE_FOLDER = "snapshots"

st.title("🚁 Victim Detection Dashboard")

if not os.path.exists(CSV_FILE):
    st.warning("CSV file not found. Run the detection script first.")
    st.stop()

# Read CSV data
df = pd.read_csv(CSV_FILE)
if df.empty:
    st.info("No detections yet.")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter")
min_conf = st.sidebar.slider("Minimum Confidence", 0.0, 1.0, 0.9)

filtered = df[df["Confidence"] >= min_conf]

# --- Table Display ---
st.subheader("📋 Detection Records")
st.dataframe(filtered.sort_values("Timestamp", ascending=False), use_container_width=True)

# --- Image + Map Display ---
st.subheader("🧍 Detection Snapshot & Location")
for i, row in filtered.iterrows():
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"**Time:** {row['Timestamp']}")
        st.markdown(f"**Confidence:** {row['Confidence']}")
        image_path = row['Image']
        if os.path.exists(image_path):
            st.image(Image.open(image_path), caption="Detected Person", width=250)
        else:
            st.warning("Image not found")

    with col2:
        try:
            lat, lon = float(row['Latitude']), float(row['Longitude'])
            m = folium.Map(location=[lat, lon], zoom_start=18)
            folium.Marker([lat, lon], tooltip="Detected Location").add_to(m)
            st_folium(m, width=600, height=300)
        except:
            st.error("Invalid GPS data")

    st.markdown("---")
