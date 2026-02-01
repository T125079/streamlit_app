import streamlit as st
import pandas as pd
import plotly.express as px

st.title('年代・性別別 睡眠時間の分布')
df = pd.read_csv('sleep.csv')

if "show_app" not in st.session_state:
    st.session_state.show_app = False
if not st.session_state.show_app:
        st.header("アプリの概要")
        st.subheader("目的")
        st.write("このアプリは、厚生労働省の統計データを基に、日本人の睡眠時間の傾向を可視化することを目的としています。")
        st.subheader("使い方")
        st.write("""
        1. 左側のサイドバーから表示するグラフの種類を選択します。
        2. サイドバーから「性別」や「年代」の適用するフィルターを選択します。
        3. グラフが更新され、睡眠時間の分布が表示されます。
        """)
        st.subheader("表示できるグラフ")
        st.markdown("""
        本アプリでは、以下の3つのグラフから傾向を確認できます。
        * **性別 × 年代（組み合わせ別）棒グラフ**: 性別と年代の組み合わせごとに、睡眠時間の割合を比較できます。
        * **性別 × 年代（組み合わせ別）円グラフ**: 各性別・年代における睡眠時間の構成比を、円グラフで視覚的に確認できます。
        * **睡眠時間別（性別または年代）棒グラフ**: 各睡眠時間ごとの性別または年代ごとの割合を特定の性別、年代で比較できます。
        """)

        st.divider()
        st.header("使用データ")
        st.write("厚生労働省が公開している「令和5年 国民健康・栄養調査」のデータを加工して使用しています。")
        st.page_link("https://www.e-stat.go.jp/stat-search/files?stat_infid=000040276088",
            label="e-Stat(政府統計の総合窓口)",
        )

        st.subheader("基本情報")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("調査年", "2023年 (令和5年)")
            st.metric("有効回答数", "5,437人")
        with col2:
            st.metric("対象", "20歳以上")
            st.write("**調査方法:** 生活習慣調査票への回答")

        with st.expander("調査内容の詳細を表示"):
            st.write("""
            **設問:** 「ここ１ヶ月間、あなたの１日の平均睡眠時間はどのくらいでしたか。あてはまる番号を１つ選んで○印をつけて下さい。」
            この回答を集計対象としています。
            """)

        st.divider()

        if st.button("データを見てみる", use_container_width=True):
            st.session_state.show_app = True
            st.rerun()

        st.stop()
with st.sidebar:
    if st.session_state.show_app:
        if st.button("ホームに戻る",use_container_width=True):
            st.session_state.show_app = False
            st.rerun()

    st.header("表示グラフオプション")
    graph_selection = st.radio(
        "表示するグラフの種類を選択してください。",
        ["性別 × 年代（組み合わせ別）棒グラフ", "性別 × 年代（組み合わせ別）円グラフ","睡眠時間別（性別または年代）棒グラフ"]
    )
    if graph_selection == "性別 × 年代（組み合わせ別）棒グラフ":
        graph_mode = 'bar'
    elif graph_selection == "性別 × 年代（組み合わせ別）円グラフ":
        graph_mode = 'pie'
    else:
        graph_mode = 'bar2'

    st.header("フィルターオプション")
    table = st.toggle("表を表示する",value=True)
    if graph_mode in ['bar', 'pie']:
        with st.expander("表示項目オプション", expanded=True):
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
            with st.expander("表示項目オプション"):
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
        st.subheader("絞り込みデータ")
        st.dataframe(
            filtered_df.rename(columns=jp_columns),
            use_container_width=True
        )

    if graph_mode == "bar":
        st.subheader("性別 × 年代（組み合わせ別）棒グラフ")
        fig = px.bar(
            filtered_df,
            x="display_label",
            y="percentage",
            color="sleep",
            barmode="group", 
            labels={
                "display_label": "性別・年代",
                "percentage": "割合（％）",
                "sleep": "睡眠時間"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("""
        **【データの読み取り】**
        * すべての組み合わせで「5時間以上6時間未満」「6時間以上7時間未満」の合計の「5時間以上7時間未満」で50%を超えている。
        """)
    
    elif graph_mode == "pie":
        st.subheader("性別 × 年代（組み合わせ別）円グラフ")
        pie_order = [
            "5時間未満", 
            "5時間以上6時間未満", 
            "6時間以上7時間未満", 
            "7時間以上8時間未満", 
            "8時間以上9時間未満",
            "9時間以上"
        ]
        existing_labels = filtered_df["sleep"].unique()
        pie_order = [label for label in pie_order if label in existing_labels]
        remaining = [l for l in existing_labels if l not in pie_order]
        pie_order.extend(remaining)
        colors = px.colors.qualitative.Plotly
        color_map = {
            label: colors[i % len(colors)]
            for i, label in enumerate(pie_order)
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
                                category_orders={"sleep": pie_order},
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
            for label in pie_order:
                color = color_map[label]
                legend_html += (
                    f"<span style='color:{color}; "
                    "font-size: 14px; margin-right: 3px;'>■</span>"
                    f"<span style='font-size: 12px; margin-right: 12px;'>"
                    f"{label}</span>"
                )
            legend_html += "</div>"
            st.markdown(legend_html, unsafe_allow_html=True)
        st.info("""
        **【データの読み取り】**
        * すべての組み合わせを見ると「6時間以上7時間未満」の階級が最も高い割合を占めている。
        """)

    elif graph_mode == "bar2":
        st.subheader("睡眠時間別（性別または年代）棒グラフ")
        
        fig = px.bar(
            filtered_df,
            x="sleep",
            y="percentage",
            color=bar2_color_col,
            barmode="group", 
            labels={
                "sleep": "睡眠時間",
                "percentage": "割合（％）",
                bar2_color_col: "性別" if bar2_color_col == "sex" else "年代"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
        st.info("""
        **【データの読み取り】**
        * 男性、女性、すべてそれぞれが、40代、50代になると睡眠時間が短くなるが、60代以降は再び睡眠時間が長くなっている。
        """)
else:
    st.warning("選択された条件に該当するデータがありません。")