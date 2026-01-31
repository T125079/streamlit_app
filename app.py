import streamlit as st
import pandas as pd
import plotly.express as px

st.title('１日の平均睡眠時間')

df = pd.read_csv('sleep.csv')

with st.sidebar:
    st.header("表示グラフオプション")
    graph_selection = st.radio(
        "表示するグラフの種類を選択してください。",
        ["性別、年代ごとの棒グラフ", "性別、年代ごとの棒グラフ"]
    )
    
    if graph_selection == "性別、年代ごとの棒グラフ":
        graph_mode = 'bar'
    else:
        graph_mode = 'pie'

    st.header("フィルターオプション")
    sex_options = st.multiselect(
        "性別を選択してください。",
        df['sex'].unique(),
        default=df['sex'].unique()
    )

    age_options = st.multiselect(
        "年代を選択してください。",
        df['age'].unique(),
        default=df['age'].unique()
    )

filtered_df = df[
    df['sex'].isin(sex_options) & 
    df['age'].isin(age_options)
].copy()

if not filtered_df.empty:
    filtered_df['display_label'] = filtered_df['sex'] + " " + filtered_df['age']

    jp_columns = {
        "sex": "性別",
        "age": "年代",
        "sleep": "睡眠時間",
        "percentage": "割合（％）",
        "display_label": "性別・年代"
    }

    st.subheader("絞り込みデータ一覧")
    st.dataframe(filtered_df.rename(columns=jp_columns), use_container_width=True)

    if graph_mode == "bar":
        st.subheader("睡眠時間の構成比（性別・年代）棒グラフ")
        fig = px.bar(
            filtered_df,
            x="display_label",
            y="percentage",
            color="sleep",
            labels={
                "display_label": "性別・年代",
                "percentage": "割合（％）",
                "sleep": "睡眠時間"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    elif graph_mode == "pie":
        st.subheader("睡眠時間の構成比（性別・年代）円グラフ")
        for sex in sex_options:
            for age in age_options:
                individual_df = filtered_df[(filtered_df['sex'] == sex) & (filtered_df['age'] == age)]
                if not individual_df.empty:
                    fig = px.pie(
                        individual_df,
                        values="percentage",
                        names="sleep",
                        hole=0.5,
                        title=f"{sex} {age} の睡眠時間割合"
                    )
                    fig.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("選択された条件に該当するデータがありません。")