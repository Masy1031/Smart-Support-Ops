import streamlit as st
import os
import logging
from src.rag_engine import initialize_rag_engine, query_rag_engine
from src.utils import save_query_log, get_openai_api_key, setup_logging
from src.analytics import display_analytics_dashboard

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(layout="wide", page_title="Smart Support Ops")

# --- Sidebar --- #
st.sidebar.title("設定")

# OpenAI API Key Input
openai_api_key = get_openai_api_key()
if not openai_api_key:
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password", help=".envファイルにOPENAI_API_KEYが設定されていない場合")
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
        logger.info("OpenAI API Key set from sidebar.")
    else:
        st.sidebar.warning("OpenAI API Keyを設定してください。")
        logger.warning("OpenAI API Key is not set.")
        st.stop()

# Page Navigation
page = st.sidebar.radio("ページ切り替え", ["問い合わせ対応(Resolver)", "分析ダッシュボード(Analytics)"])

# Knowledge Base Update Button
if st.sidebar.button("知識ベースの更新"):
    with st.spinner("知識ベースを更新中..."):
        try:
            st.session_state['query_engine'] = initialize_rag_engine()
            st.sidebar.success("知識ベースが更新されました！")
            logger.info("Knowledge base updated.")
        except Exception as e:
            st.sidebar.error(f"知識ベースの更新中にエラーが発生しました: {e}")
            logger.error(f"Error updating knowledge base: {e}")

# Initialize RAG engine if not already in session state
if 'query_engine' not in st.session_state:
    with st.spinner("RAGエンジンを初期化中..."):
        try:
            st.session_state['query_engine'] = initialize_rag_engine()
            logger.info("RAG engine initialized.")
        except Exception as e:
            st.error(f"RAGエンジンの初期化中にエラーが発生しました: {e}")
            logger.error(f"Error initializing RAG engine: {e}")
            st.stop()

# --- Main Content --- #
if page == "問い合わせ対応(Resolver)":
    st.title("🚀 問い合わせ対応 (Intelligent Resolver)")

    # Text Input Area
    user_query = st.text_area("問い合わせ内容またはエラーログを入力してください", height=150)

    # Execute Button
    if st.button("AIに回答を依頼する"):
        if user_query:
            logger.info(f"User query received: {user_query[:100]}...")
            with st.spinner("AIが回答を生成中..."):
                try:
                    answer, source_nodes, confidence, confidence_percentage = query_rag_engine(st.session_state['query_engine'], user_query)
                    st.session_state['last_response'] = {
                        "query": user_query,
                        "answer": answer,
                        "confidence": confidence,
                        "confidence_percentage": confidence_percentage,
                        "source_nodes": source_nodes,
                    }
                    logger.info("AI response generated successfully.")

                    st.subheader("AI回答")
                    st.write(answer)

                    st.subheader("確信度スコア")
                    st.write(f"{confidence} ({confidence_percentage})")

                    st.subheader("参照ソース")
                    for i, node in enumerate(source_nodes):
                        st.write(f"**ドキュメント: {node.metadata.get('file_name', 'Unknown')}**")
                        st.write(node.text)
                        st.markdown("---")
                except Exception as e:
                    logger.error(f"Error generating AI response: {e}")
                    st.error(f"回答生成中にエラーが発生しました: {e}")
        else:
            st.warning("問い合わせ内容を入力してください。")
            logger.warning("User tried to submit an empty query.")

    # Action Area
    if 'last_response' in st.session_state:
        st.markdown("### 回答へのフィードバック")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("解決（Good）", use_container_width=True):
                save_query_log(
                    st.session_state['last_response']['query'],
                    st.session_state['last_response']['answer'],
                    st.session_state['last_response']['confidence'],
                    "解決済み"
                )
                st.success("フィードバックを保存しました: 解決済み")
                logger.info(f"Query marked as resolved: {st.session_state['last_response']['query'][:50]}...")
                del st.session_state['last_response'] # Clear for next query
        with col2:
            if st.button("未解決（Bad）", use_container_width=True):
                save_query_log(
                    st.session_state['last_response']['query'],
                    st.session_state['last_response']['answer'],
                    st.session_state['last_response']['confidence'],
                    "要改善"
                )
                st.error("フィードバックを保存しました: 要改善")
                logger.info(f"Query marked as needs improvement: {st.session_state['last_response']['query'][:50]}...")
                st.subheader("開発へのエスカレーション用テキスト")
                st.code(f"""【Issueタイトル】未解決の問い合わせ: {st.session_state['last_response']['query'][:50]}...

【事象】
ユーザーからの問い合わせに対してAIの回答では解決できませんでした。

【問い合わせ内容】
{st.session_state['last_response']['query']}

【AI回答】
{st.session_state['last_response']['answer']}

【確信度】
{st.session_state['last_response']['confidence_percentage']}

【対応】
関連ドキュメントの拡充、またはAI回答ロジックの改善が必要です。
""")
                del st.session_state['last_response'] # Clear for next query

elif page == "分析ダッシュボード(Analytics)":
    display_analytics_dashboard()
