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
        ["20代","30代","40代","50代","60代","70代以上","すべて"]
    )
    age_mapping = {
        "20代": "20-29",
        "30代": "30-39",
        "40代": "40-49",
        "50代": "50-59",
        "60代": "60-69",
        "70代以上": "70-",
        "すべて": "all"
    }
    selected_age = [age_mapping[item] for item in age_options]

filtered_df = df[
    (df['sex'].isin(selected_sex)) & 
    (df['age'].isin(selected_age))
]

if not filtered_df.empty:
    inv_sex_map = {v: k for k, v in sex_mapping.items()}
    inv_age_map = {v: k for k, v in age_mapping.items()}
    sleep_mapping = {
    "-5": "5時間未満",
    "5-6": "5時間以上6時間未満",
    "6-7": "6時間以上7時間未満",
    "7-8": "7時間以上8時間未満",
    "8-9": "8時間以上9時間未満",
    "9-": "9時間以上"
    }
    filtered_df['sex'] = filtered_df['sex'].map(inv_sex_map)
    filtered_df['age'] = filtered_df['age'].map(inv_age_map)
    filtered_df['sleep'] = filtered_df['sleep'].map(sleep_mapping)
    filtered_df['display_label'] = filtered_df['sex'] + " " + filtered_df['age']

    st.subheader("絞り込みデータ一覧")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.subheader("睡眠時間の構成比")

    fig = px.bar(
        filtered_df,
        x="display_label",
        y="percentage",
        color="sleep",
        labels={
            "display_label": "性別・年代",
            "percentage": "割合 (%)",
            "sleep": "睡眠時間"
        },

        category_orders={
            "display_label": sorted(filtered_df['display_label'].unique())
        }
    )
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("選択された条件に該当するデータがありません。")