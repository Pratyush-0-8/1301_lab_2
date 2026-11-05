# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import plotly.express as px
import json

with open("data.json", "r") as file:
    data = json.load(file)

artists = data["artists"]
years = data["years"]

st.title("Spotify Artist Streaming Statistics")


st.header("Total Streams by Artist")

names = []
streams = []

for artist in artists:
    names.append(artist["name"])
    streams.append(artist["total_streams"])

df = pd.DataFrame({
    "Artist": names,
    "Streams (Billions)": streams
})

st.bar_chart(df, x="Artist", y="Streams (Billions)")



st.header("Yearly Streams by Artist")

if "selected_artist" not in st.session_state:
    st.session_state.selected_artist = "Drake"

selected_artist = st.selectbox(
    "Select an Artist",
    names,
    key="selected_artist"
)

for artist in artists:
    if artist["name"] == selected_artist:
        yearly_streams = artist["yearly_streams"]

yearly_df = pd.DataFrame({
    "Year": years,
    "Streams (Billions)": yearly_streams
})

fig = px.line(
    yearly_df,
    x="Year",
    y="Streams (Billions)",
    title="Yearly Streams for " + selected_artist,
    markers=True
)

st.plotly_chart(fig)

st.divider()
st.title("Spotify Listening Habits")

csv_data = pd.read_csv("data.csv")
csv_data["Value"] = pd.to_numeric(csv_data["Value"], errors="coerce")
csv_data = csv_data.dropna(subset=["Value"])

if not csv_data.empty:

    totals = csv_data.groupby("Category")["Value"].sum().reset_index()

    # STATIC BAR CHART
    st.header("Total Listening Hours by Genre")

    st.bar_chart(totals, x="Category", y="Value")

    # DYNAMIC PIE CHART
    st.header("Listening Hours Distribution")

    if "min_hours" not in st.session_state:
        st.session_state.min_hours = 0

    max_hours = int(totals["Value"].max())

    min_hours = st.slider(
        "Minimum total listening hours",
        min_value=0,
        max_value=max_hours,
        key="min_hours"
    )

    filtered_totals = totals[totals["Value"] >= min_hours]

    fig2 = px.pie(
        filtered_totals,
        names="Category",
        values="Value",
        title="Listening Hours by Genre"
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("No survey data available.")