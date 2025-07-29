import streamlit as st
import pandas as pd
import os
st.selectbox("Filtrer etter sesong", ["Alle"] + df['session'].unique().tolist())
st.set_page_config(page_title="Crypto Signal Dashboard", layout="wide")

st.title("📊 Smart Money Signal Dashboard")
st.markdown("Live-oversikt over siste tekniske signaler fra SignalBot")

if not os.path.exists("signal_log.csv"):
    st.warning("Ingen signaler logget enda...")
else:
    df = pd.read_csv("signal_log.csv")
    df = df.sort_values("timestamp", ascending=False)

    with st.sidebar:
        st.header("🔍 Filtrering")
        min_rating = st.slider("Minimum Rating", 1, 5, 3)
        type_filter = st.selectbox("Type", ["Alle", "Scalp", "Swing"])
        session_filter = st.selectbox("Sesjon", ["Alle", "Asia", "London", "New York"])

    filtered = df[df["rating"] >= min_rating]

    if type_filter != "Alle":
        filtered = filtered[filtered["type"] == type_filter]

    if session_filter != "Alle":
        filtered = filtered[filtered["session"] == session_filter]

    st.markdown(f"### 🔎 Viser {len(filtered)} signal(er)")
    st.dataframe(filtered, use_container_width=True)

    if st.checkbox("📈 Vis siste graf med signal"):
        latest = filtered.iloc[0]
        img_path = latest["chart_path"]
        if os.path.exists(img_path):
            st.image(img_path, caption=latest["symbol"])
        else:
            st.warning("Fant ikke bilde for siste signal.")