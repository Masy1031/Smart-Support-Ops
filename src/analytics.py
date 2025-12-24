import pandas as pd
import streamlit as st
import plotly.express as px
import os

LOG_FILE = "data/logs/history.csv"

def load_logs():
    """Loads the query log from history.csv into a Pandas DataFrame."""
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE, encoding='utf-8-sig')
        return df
    return pd.DataFrame(columns=["timestamp", "query", "answer", "confidence", "status"])

def display_analytics_dashboard():
    """Displays the analytics dashboard with KPIs and improvement suggestions."""
    st.title("📈 分析ダッシュボード (Insight Dashboard)")

    df_logs = load_logs()

    if df_logs.empty:
        st.info("まだ問い合わせログがありません。Resolverで問い合わせを処理してください。")
        return

    # --- KPI 表示 ---
    st.header("主要KPI")
    total_queries = len(df_logs)
    resolved_queries = df_logs[df_logs["status"] == "解決済み"]
    auto_resolution_rate = (len(resolved_queries) / total_queries * 100) if total_queries > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("累計問い合わせ数", total_queries)
    with col2:
        st.metric("自動解決率", f"{auto_resolution_rate:.1f}%")
    with col3:
        # Simple topic ranking (e.g., by confidence distribution)
        st.subheader("確信度別問い合わせ数")
        confidence_counts = df_logs["confidence"].value_counts().reset_index()
        confidence_counts.columns = ["Confidence", "Count"]
        fig_confidence = px.bar(confidence_counts, x="Confidence", y="Count",
                                title="問い合わせの確信度分布", color="Confidence",
                                color_discrete_map={'高': 'green', '中': 'orange', '低': 'red'})
        st.plotly_chart(fig_confidence, use_container_width=True)

    # --- 改善提案リスト ---
    st.header("改善提案リスト (Killer Feature)")

    # Filter for low confidence or 'Bad' evaluations
    needs_improvement_df = df_logs[(df_logs["confidence"] == "低") | (df_logs["status"] == "要改善")]

    if not needs_improvement_df.empty:
        st.write("**回答スコアが低かった、またはBad評価の質問:**")
        for index, row in needs_improvement_df.iterrows():
            with st.expander(f"問い合わせID: {index + 1} - 確信度: {row['confidence']} - ステータス: {row['status']}"):
                st.write(f"**質問:** {row['query']}")
                st.write(f"**AI回答:** {row['answer']}")
                st.warning("💡 このトピックに関するFAQドキュメントが不足している可能性があります。")
    else:
        st.info("現在、改善が必要な問い合わせはありません。素晴らしい！")


