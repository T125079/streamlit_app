import streamlit as st
import pandas as pd
import plotly.express as px
st.title('１日の平均睡眠時間')
df = pd.read_csv('sleep.csv')
st.dataframe(df, width=800, height=220)