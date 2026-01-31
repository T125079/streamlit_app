import streamlit as st
import pandas as pd
import plotly.express as px
st.title('１日の平均睡眠時間')
df = pd.read_csv('sleep.csv')
with st.sidebar:
    st.sidebar.header("表示グラフオプション")
    show_graph_options=st.radio(
        "表示するグラフの種類を選択してください。",
        ["性別、年代ごとの棒グラフ","性別ごとの円グラフ"]
    )
    if show_graph_options == "性別、年代ごとの棒グラフ":
        show_graph_options='bar_graph'
    elif show_graph_options == "性別ごとの円グラフ":
        show_graph_options='pie_chart'
    
    st.sidebar.header("フィルターオプション")
    st.write('フィルターするオプションを選択してください。')
    if show_graph_options == "bar_graph":
        sex_options = st.multiselect(
            "性別を選択してください。（複数選択可）",
            df['sex'].unique()
        )

        age_options = st.multiselect(
            "年代を選択してください。（複数選択可）",
            df['age'].unique()
        )
        filtered_df = df[
            df['sex'].isin(sex_options) &
            df['age'].isin(age_options)
        ]
    

if show_graph_options == "bar_graph":
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
        st.dataframe(filtered_df.rename(columns=jp_columns),use_container_width=True)
    
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
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("選択された条件に該当するデータがありません。")







