import streamlit as st
from config import supabase
import pandas as pd
from datetime import datetime

# === Helper to convert timestamp ===
def parse_timestamp(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%d %I:%M:%S %p")
    except:
        return pd.NaT

# === Query Supabase ===
def fetch_grouped_data():
    response = supabase.table("tv.garden").select("*").execute()
    data = response.data
    df = pd.DataFrame(data)

    if df.empty or "url" not in df.columns:
        return {}

    df["parsed_time"] = df["timestamp"].apply(parse_timestamp)
    df = df.sort_values(by="parsed_time", ascending=True)  # Earliest to latest

    grouped = {}
    for url, group_df in df.groupby("url"):
        name = group_df["name"].iloc[0] if "name" in group_df.columns else "Unknown"
        grouped[url] = {
            "name": name,
            "table": group_df[["timestamp", "status"]].reset_index(drop=True)
        }

    return grouped

# === UI ===
st.header("TV Garden Monitoring Report")

grouped_data = fetch_grouped_data()

if not grouped_data:
    st.warning("No data found in 'tv.garden' table.")
else:
    for url, data in grouped_data.items():
        name = data["name"]
        table = data["table"]
        st.caption(url)

        table.index += 1
        st.dataframe(table, use_container_width=True)

        st.markdown("---")
