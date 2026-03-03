import streamlit as st
import os
from dotenv import load_dotenv
from compare import get_cloudflare_response, get_groq_response

# 1. 必须是整个脚本的第一个 Streamlit 命令
st.set_page_config(page_title="AI Auditor V2", layout="wide")

# 2. 加载环境变量
load_dotenv()

# 3. 自定义 CSS
st.markdown(
    """
    <style>
    .stButton > button {
        background-color: #0d6efd !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #0b5ed7 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔍 AI Auditor 智能审计 (V2.0)")
st.markdown("---")

prompt_input = st.text_area(
    "请输入需要审计的提示词 (Prompt):",
    placeholder="在此输入文本...",
    height=150,
)

if st.button("开始审计对比"):
    if not prompt_input:
        st.warning("请先输入内容！")
    else:
        col1, col2 = st.columns(2)

        with st.spinner('正在调用 AI 模型，请稍候...'):
            cf_result = get_cloudflare_response(prompt_input)
            gr_result = get_groq_response(prompt_input)

            with col1:
                st.subheader("Cloudflare (DeepSeek-R1)")
                st.text_area("结果 1:", value=cf_result, height=400, key="out1")

            with col2:
                st.subheader("Groq (Llama)")
                st.text_area("结果 2:", value=gr_result, height=400, key="out2")

            full_report = f"--- AI AUDIT REPORT ---\n\nPROMPT:\n{prompt_input}\n\n"
            full_report += f"[CLOUDFLARE OUTPUT]:\n{cf_result}\n\n"
            full_report += f"[GROQ OUTPUT]:\n{gr_result}\n"

            st.markdown("---")
            st.download_button(
                label="📥 点击下载审计报告 (TXT)",
                data=full_report,
                file_name="audit_report_v2.txt",
                mime="text/plain"
            )