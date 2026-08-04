import streamlit as st
import pandas as pd

st.title("AI Wood Storage Site Dashboard")

sites = pd.read_csv("data/sites.csv")

st.subheader("Wood Storage Sites")
st.dataframe(sites)

st.map(
    sites.rename(columns={
        "latitude": "lat",
        "longitude": "lon"
    })[["lat", "lon"]]
)