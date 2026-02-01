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
        ]
    else:
            bar2_show_options = st.selectbox(
                "表示する設定を選択してください",
                ["性別", "年代"]
            )
            bar2_map = {
                "性別": "sex",
                "年代": "age"
            }
            bar2_color_col = bar2_map[bar2_show_options]
            if bar2_color_col == "sex":
                bar2_age = st.radio(
                    "表示する年代を選択してください。",
                    df["age"].unique(),
                    horizontal=True
                )
                filtered_df = df[df["age"] == bar2_age].copy()

            else:
                bar2_sex = st.radio(
                    "表示する性別を選択してください。",
                    df["sex"].unique(),
                    horizontal=True
                )
                filtered_df = df[df["sex"] == bar2_sex].copy()
                

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
        st.subheader("睡眠時間の構成比個別表示")
        bar2_order = sorted(filtered_df["sleep"].unique())
        colors = px.colors.qualitative.Plotly
        color_map = {
            label: colors[i % len(colors)]
            for i, label in enumerate(bar2_order)
        }
        charts_data = []
        for sex in sex_options:
            for age in age_options:
                individual_df = filtered_df[
                    (filtered_df["sex"] == sex) & (filtered_df["age"] == age)
                ]
                if not individual_df.empty:
                    charts_data.append((sex, age, individual_df))
        total_count = len(charts_data)
        if total_count > 0:
            row_cols = min(total_count, 4)
            for i in range(0, total_count, row_cols):
                cols = st.columns(row_cols, gap="small")
                for j in range(row_cols):
                    idx = i + j
                    if idx < total_count:
                        sex, age, df = charts_data[idx]
                        with cols[j]:
                            fig = px.pie(
                                df,
                                values="percentage",
                                names="sleep",
                                hole=0.5,
                                category_orders={"sleep": bar2_order},
                                color="sleep",
                                color_discrete_map=color_map
                            )
                            fig.update_layout(
                                showlegend=False,
                                margin=dict(t=25, b=0, l=0, r=0),
                                height=160,
                                annotations=[{
                                    "text": f"<b>{sex}<br>{age}</b>",
                                    "x": 0.5,
                                    "y": 0.5,
                                    "font_size": 10,
                                    "showarrow": False
                                }]
                            )
                            fig.update_traces(
                                textinfo="percent",
                                textposition="inside"
                            )
                            st.plotly_chart(fig, use_container_width=True)
            legend_html = (
                "<div style='text-align: center; "
                "margin-top: -10px; margin-bottom: 20px;'>"
            )
            for label in bar2_order:
                color = color_map[label]
                legend_html += (
                    f"<span style='color:{color}; "
                    "font-size: 14px; margin-right: 3px;'>■</span>"
                    f"<span style='font-size: 12px; margin-right: 12px;'>"
                    f"{label}</span>"
                )
            legend_html += "</div>"
            st.markdown(legend_html, unsafe_allow_html=True)

    elif graph_mode == "bar2":
        st.subheader("睡眠時間ごとの割合（性別・年代）棒グラフ")
        
        fig = px.bar(
            filtered_df,
            x="sleep",
            y="percentage",
            color=bar2_color_col,
            labels={
                "sleep": "睡眠時間",
                "percentage": "割合（％）",
                bar2_color_col: "性別" if bar2_color_col == "sex" else "年代"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("選択された条件に該当するデータがありません。")


st.write(
    "国民健康・栄養調査 / 令和５年国民健康・栄養調査 第71表"
    "１日の平均睡眠時間 - １日の平均睡眠時間、年齢階級別、人数、割合 - "
    "総数・男性・女性、20歳以上 を改変し作成"
)
