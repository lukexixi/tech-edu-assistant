import streamlit as st
import requests

# 页面配置
st.set_page_config(page_title="AI科技教培助手", layout="centered")
st.title("🤖 科技素质教育智能顾问")
st.caption("提供乐高、Python、C++编程及白名单竞赛规划")

# 这里的 URL 填你 Flowise 云端的 API Endpoint
# 格式通常是 https://cloud.flowiseai.com/api/v1/prediction/你的ID
API_URL = "https://cloud.flowiseai.com/api/v1/prediction/bf9603b5-6f62-4e3b-a48e-c0e52e30c963"

def query_flowise(message):
    payload = {"question": message}
    response = requests.post(API_URL, json=payload)
    return response.json()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("询问竞赛报名或课程规划..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        res = query_flowise(prompt)
        # 兼容 Flowise 不同版本的返回格式
        answer = res.get("text") or res.get("response") or "系统忙，请稍后再试"
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})