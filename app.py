# app.py
import streamlit as st
import pandas as pd
from etl import fetch_objects, transform_data, insert_records
from db import get_connection
from queries import QUERIES

st.set_page_config(page_title="Harvard Artifacts Explorer", layout="wide")
st.title("🎨 Harvard Artifacts Explorer")

# ✅ Corrected classification spelling
CLASSIFICATIONS = ["Coins", "Paintings", "Sculpture", "Vessels", "Drawings"]

classification = st.selectbox("Choose Classification", CLASSIFICATIONS)

if "records" not in st.session_state:
    st.session_state.records = []

# ---------------- FETCH ---------------- #
if st.button("📥 Fetch Data from API"):
    with st.spinner("Fetching records..."):
        data = fetch_objects(classification)
        st.session_state.records = data
        st.success(f"Fetched {len(data)} records.")

# ---------------- PREVIEW ---------------- #
if st.button("🔎 Preview Data"):
    if st.session_state.records:
        df = pd.DataFrame(st.session_state.records)
        st.dataframe(df)
    else:
        st.warning("⚠ No data fetched yet!")

# ---------------- INSERT ---------------- #
if st.button("💾 Insert into TiDB"):
    if not st.session_state.records:
        st.warning("⚠ Please fetch data before inserting.")
    else:
        engine = get_connection()
        meta, media, colors = transform_data(st.session_state.records)

        insert_records(engine, "artifact_metadata", meta)

        valid_ids = set(pd.read_sql("SELECT id FROM artifact_metadata", engine)['id'])
        media = [row for row in media if row[0] in valid_ids]
        colors = [row for row in colors if row[0] in valid_ids]

        insert_records(engine, "artifact_media", media)
        insert_records(engine, "artifact_colors", colors)

        st.success("✅ Data inserted successfully without FK errors!")

# ---------------- COUNT CHECK ---------------- #
if st.button("📊 Show DB Count"):
    engine = get_connection()
    meta_count = pd.read_sql("SELECT COUNT(*) as total FROM artifact_metadata", engine)['total'][0]
    media_count = pd.read_sql("SELECT COUNT(*) as total FROM artifact_media", engine)['total'][0]
    color_count = pd.read_sql("SELECT COUNT(*) as total FROM artifact_colors", engine)['total'][0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Metadata Rows", meta_count)
    col2.metric("Media Rows", media_count)
    col3.metric("Colors Rows", color_count)

# ---------------- Queries CHECK ---------------- #
st.subheader("📊 Run Predefined Queries")
query_label = st.selectbox("Choose Query", list(QUERIES.keys()))
if st.button("🚀 Run Query"):
    engine = get_connection()
    try:
        df = pd.read_sql(QUERIES[query_label], engine)
        if df.empty:
            st.info("No results found for the selected query.")
        else:
            st.dataframe(df)
    except Exception as e:
        st.error(f"Error: {e}")
