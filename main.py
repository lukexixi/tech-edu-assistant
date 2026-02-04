import streamlit as st
import requests

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

.header{
    font-size:28px;
    font-weight:800;
    color:#1E3A8A;
    text-align:center;
}

.brand{
    text-align:center;
    color:#475569;
    margin-bottom:18px;
    font-weight:500;
}

.pain{
    background:#F1F5F9;
    padding:18px;
    border-radius:14px;
    border-left:6px solid #3B82F6;
    line-height:1.7;
    font-size:15px;
}
</style>
""", unsafe_allow_html=True)


# ========== 3. 品牌头部 ==========
st.markdown('<div class="header">🧪 青少年科技素养长期发展评估</div>', unsafe_allow_html=True)
st.markdown('<div class="brand">洛克实验室 · 家庭科技成长研究中心</div>', unsafe_allow_html=True)


# ========== 4. 痛点升级 ==========
st.markdown("""
<div class="pain">
<b>很多理性家长都会困惑：</b><br><br>

✔ 小学学编程，初中还能不能接得上？<br>
✔ 现在不打基础，将来会不会被淘汰？<br>
✔ 冲竞赛到底是机会，还是弯路？<br><br>

洛克实验室基于多年家庭跟踪研究，
通过「4A科技素养模型」，
帮助家长看清长期方向，而不是短期焦虑。
</div>
""", unsafe_allow_html=True)


# ========== 5. 侧边栏 ==========
with st.sidebar:

    st.markdown("### 🧪 洛克实验室")
    st.caption("青少年科技成长研究机构")

    st.divider()

    st.markdown("📘 家庭支持工具包")
    st.write("• 4A成长观察表")
    st.write("• 竞赛路径风险说明")
    st.write("• 家庭陪伴指南")

    st.caption("完成测评后可申请获取参考资料")

    st.divider()

    st.caption("⚠️ 本系统不提供升学或获奖承诺，仅作长期参考")


# ========== 6. 聊天初始化 ==========
if "messages" not in st.session_state:
    st.session_state.messages = []


# ========== 7. 功能入口升级 ==========
st.markdown("### 🔍 开始专业评估")

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("🌱 兴趣发展评估"):
        st.session_state.messages.append({
            "role":"user",
            "content":"请基于4A模型评估孩子当前兴趣发展状态"
        })

with c2:
    if st.button("🛠 实践能力分析"):
        st.session_state.messages.append({
            "role":"user",
            "content":"请分析孩子动手实践与工程能力水平"
        })

with c3:
    if st.button("🧠 思维结构测评"):
        st.session_state.messages.append({
            "role":"user",
            "content":"请评估孩子的计算思维发展阶段"
        })


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

                answer = (
                    data.get("text") or
                    data.get("response") or
                    "系统繁忙，请稍后再试。"
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role":"assistant",
                    "content":answer
                })

        except:
            st.error("⚠️ 当前服务繁忙，请稍后重试。")
