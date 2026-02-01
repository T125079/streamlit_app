import streamlit as st
import pandas as pd
import plotly.express as px

st.title('１日の平均睡眠時間')

df = pd.read_csv('sleep.csv')

with st.sidebar:
    st.header("表示グラフオプション")
    graph_selection = st.radio(
        "表示するグラフの種類を選択してください。",
        ["性別、年代ごとの棒グラフ", "性別、年代ごとの円グラフ","睡眠時間別年代および性別の棒グラフ"]
    )
    
    if graph_selection == "性別、年代ごとの棒グラフ":
        graph_mode = 'bar'
    elif graph_selection == "性別、年代ごとの円グラフ":
        graph_mode = 'pie'
    else:
        graph_mode = 'bar2'


    st.header("フィルターオプション")
    table = st.toggle("表を表示する",value=True)
    if graph_mode in ['bar', 'pie']:
        with st.expander("表示項目オプション"):
            sex_options = st.multiselect(
                "性別を選択してください。",
                df['sex'].unique()
            )

            age_options = st.multiselect(
                "年代を選択してください。",
                df['age'].unique()
            )
        filtered_df = df[
            df['sex'].isin(sex_options) & 
            df['age'].isin(age_options)
        ]
    else:
        sleep_show_options = st.selectbox(
            "表示する設定を選択してください",
            ["性別", "年代"]
        )
        sleep_map = {
            "性別": "sex",
            "年代": "age"
        }
        color_col = sleep_map[sleep_show_options]
        filtered_df = df[["sleep", "percentage", color_col]]

if not filtered_df.empty:
    jp_columns = {
        "sex": "性別",
        "age": "年代",
        "sleep": "睡眠時間",
        "percentage": "割合（％）",
        "display_label": "性別・年代"
    }

    if graph_mode in ["bar", "pie"]:
        filtered_df["display_label"] = filtered_df["sex"] + " " + filtered_df["age"]

    if table:
        st.subheader("絞り込みデータ一覧")
        st.dataframe(
            filtered_df.rename(columns=jp_columns),
            use_container_width=True
        )

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
        st.subheader("睡眠時間の構成比（性別・年代）円グラフ（全体）")
        fig = px.pie(
            filtered_df,
            names="sleep",
            values="percentage",
            color="sleep",
            title="睡眠時間の割合"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("睡眠時間の構成比（性別・年代）個別表示")
        for sex in sex_options:
            for age in age_options:
                individual_df = filtered_df[
                    (filtered_df["sex"] == sex) &
                    (filtered_df["age"] == age)
                ]

                if not individual_df.empty:
                    fig = px.pie(
                        individual_df,
                        values="percentage",
                        names="sleep",
                        hole=0.5,
                        title="睡眠時間割合"
                    )
                    fig.update_layout(
                        annotations=[{
                            "text": f"{sex}<br>{age}",
                            "x": 0.5,
                            "y": 0.5,
                            "font_size": 18,
                            "showarrow": False
                        }]
                    )
                    fig.update_traces(textinfo="percent+label")
                    st.plotly_chart(fig, use_container_width=True)
    elif graph_mode == "bar2":
        st.subheader("睡眠時間ごとの割合（性別・年代）棒グラフ")
        
        fig = px.bar(
            filtered_df,
            x="sleep",
            y="percentage",
            color=color_col,
            labels={
                "sleep": "睡眠時間",
                "percentage": "割合（％）",
                color_col: "性別" if color_col == "sex" else "年代"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("選択された条件に該当するデータがありません。")


st.write(
    "国民健康・栄養調査 / 令和５年国民健康・栄養調査 第71表　"
    "１日の平均睡眠時間 - １日の平均睡眠時間、年齢階級別、人数、割合 - "
    "総数・男性・女性、20歳以上 を改変し作成"
)
