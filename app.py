import streamlit as st
import pandas as pd
import plotly.express as px
st.title('１日の平均睡眠時間')
df = pd.read_csv('sleep.csv')
with st.sidebar:
    st.sidebar.header("フィルターオプション")
    st.write('フィルターするオプションを選択してください。')
    sex_options = st.multiselect(
        "性別を選択してください。（複数選択可）",
        ["男性", "女性", "すべて"]
    )
    sex_mapping = {
        "男性": "male",
        "女性": "female",
        "すべて": "all"
    }
    selected_sex = [sex_mapping[item] for item in sex_options]

    age_options = st.multiselect(
        "年代を選択してください。（複数選択可）",
        ["20代","30代","40代","50代","60代","70代以上",]
    )
    age_mapping = {
        "20代": "20-29",
        "30代": "30-39",
        "40代": "40-49",
        "50代": "50-59",
        "60代": "60-69",
        "70代以上": "70-",
    }
    selected_age = [age_mapping[item] for item in age_options]
    st.write(f"選択された英語ラベル: {selected_sex}{selected_age}")

