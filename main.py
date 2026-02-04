import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ========== 1. 页面配置 ==========
st.set_page_config(
    page_title="洛克实验室｜青少年科技素养评估系统",
    page_icon="🧪",
    layout="centered"
)

# ========== 2. UI 优化 ==========
st.markdown("""
<style>
.main { background-color: #FCFCFC; }
.stButton>button {
    width:100%;
    border-radius:28px;
    border:2px solid #1E3A8A;
    color:#1E3A8A;
    font-weight:600;
    height:3.2em;
    transition:all .3s;
}
.stButton>button:hover {
    background:#1E3A8A;
    color:#fff;
    transform:scale(1.03);
}
.header{ font-size:28px; font-weight:800; color:#1E3A8A; text-align:center; }
.brand{ text-align:center; color:#475569; margin-bottom:18px; font-weight:500; }
.pain{ background:#F1F5F9; padding:18px; border-radius:14px; border-left:6px solid #3B82F6; line-height:1.7; font-size:15px; }
.contact-card { background:#FFFFFF; padding:12px; border-radius:10px; border:1px solid #E2E8F0; margin-top:10px; }
</style>
""", unsafe_allow_html=True)

# ========== 3. 品牌头部 ==========
st.markdown('<div class="header">🧪 青少年科技素养长期发展评估</div>', unsafe_allow_html=True)
st.markdown('<div class="brand">洛克实验室 · 青少年科技成长研究中心</div>', unsafe_allow_html=True)

# ========== 4. 痛点升级 ==========
st.markdown("""
<div class="pain">
<b>很多理性家长都会困惑：</b><br>
✔ 小学学编程，初中还能不能接得上？<br>
✔ 现在不打基础，将来会不会被淘汰？<br>
✔ 冲竞赛到底是机会，还是弯路？<br><br>
洛克实验室基于「4A科技素养模型」，帮助家长看清长期方向。
</div>
""", unsafe_allow_html=True)

# ========== 5. 侧边栏：品牌与联系方式 ==========
with st.sidebar:
    st.markdown("### 🧪 洛克实验室")
    st.caption("青少年科技成长研究机构")
    
    # --- 新增：联系方式矩阵 ---
    with st.expander("📞 联系洛克实验室", expanded=True):
        st.markdown(f"""
        <div class="contact-card">
        <b>👤 小洛助手</b>：18962534373<br>
        <b>💬 微信号</b>：LUKE_LABS<br>
        <b>📕 小红书</b>：187100618<br>
        <b>🎵 抖音号</b>：LUKE_LABS
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()

    # --- 新增：对话抓取导出功能 ---
    st.markdown("### 📥 咨询记录导出")
    if st.session_state.get("messages"):
        # 将聊天记录转换为表格数据以便抓取信息
        chat_data = [{"角色": m["role"], "内容": m["content"]} for m in st.session_state.messages]
        df = pd.DataFrame(chat_data)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="💾 下载本次对话清单",
            data=csv,
            file_name=f"咨询记录_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )
        st.caption("提示：顾问可下载此表留存客户咨询画像")
    else:
        st.caption("暂无咨询记录可导出")

    st.divider()
    st.caption("⚠️ 本系统不提供升学或获奖承诺，仅作长期参考")

# ========== 6. 聊天初始化 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []

# ========== 7. 功能入口 ==========
st.markdown("### 🔍 开始专业评估")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🌱 兴趣发展评估"):
        st.session_state.messages.append({"role":"user","content":"请基于4A模型评估孩子当前兴趣发展状态"})
with c2:
    if st.button("🛠 实践能力分析"):
        st.session_state.messages.append({"role":"user","content":"请分析孩子动手实践与工程能力水平"})
with c3:
    if st.button("🧠 思维结构测评"):
        st.session_state.messages.append({"role":"user","content":"请评估孩子的计算思维发展阶段"})

# ========== 8. 历史记录 ==========
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ========== 9. API ==========
API_URL = "https://cloud.flowiseai.com/api/v1/prediction/bf9603b5-6f62-4e3b-a48e-c0e52e30c963"

# ========== 10. 输入 ==========
if prompt := st.chat_input("例如：三年级，喜欢拼装和游戏，专注力一般"):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("洛克实验室研究顾问正在生成分析报告..."):
                res = requests.post(API_URL, json={"question":prompt})
                res.raise_for_status()
                data = res.json()
                answer = data.get("text") or data.get("response") or "系统繁忙。"
                st.markdown(answer)
                st.session_state.messages.append({"role":"assistant","content":answer})
        except:
            st.error("⚠️ 当前服务繁忙，请稍后重试。")
