import streamlit as st
import requests

# 1. 页面基本配置：设定研究顾问的专业视觉风格
st.set_page_config(
    page_title="青少年科技素养 4A 规划助手", 
    page_icon="🧪",
    layout="centered"
)

# 2. 自定义 CSS：营造“研究型智库”的氛围
st.markdown("""
    <style>
    .main { background-color: #FDFDFD; }
    .stButton>button { width: 100%; border-radius: 20px; border: 1px solid #1E3A8A; color: #1E3A8A; }
    .stButton>button:hover { background-color: #1E3A8A; color: white; }
    .report-header { font-size: 24px; font-weight: 700; color: #1E3A8A; margin-bottom: 10px; }
    .guide-text { font-size: 14px; color: #666; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 顶部标题与认知声明
st.markdown('<p class="report-header">⚖️ 青少年科技素养 4A 发展规划自测</p>', unsafe_allow_html=True)
st.markdown('<p class="guide-text">本工具旨在基于教育学逻辑，帮助家庭建立理性、科学的科技学习认知体系。我们坚决反对功利化误导，所有建议仅供成长参考。</p>', unsafe_allow_html=True)
st.info("💡 提示：本系统采用“4A 发展模型”，从兴趣、能力、思维、自主性四个维度进行深度分析。")

# 4. 侧边栏：品牌人设与合规资源入口
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3429/3429433.png", width=80) # 模拟专家头像
    st.title("家庭科技成长顾问")
    st.markdown("---")
    st.markdown("**📖 深度研究支持**")
    st.write("获取《青少年科技素养 4A 实践观察手册》或申请加入【理性教育交流圈】。")
    st.caption("请在社交平台私信回复暗号：")
    st.code("4A手册", language=None)
    st.markdown("---")
    st.caption("⚠️ 安全提示：本平台不提供任何升学、保过或竞赛获奖承诺，请理性规划。")

# 5. 聊天记录初始化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. 核心功能引导：基于 4A 模型的交互
st.markdown("### 🔍 快速启动专业分析")
col1, col2 = st.columns(2)
with col1:
    if st.button("🧩 兴趣与认知评估"):
        st.session_state.messages.append({"role": "user", "content": "我想基于 Awareness 维度，评估孩子目前对科技学习的真实兴趣点。"})
with col2:
    if st.button("🧠 计算思维自测"):
        st.session_state.messages.append({"role": "user", "content": "请从 Algorithmic Thinking 维度，帮我拆解孩子在编程学习中应具备的底层逻辑。"})

# 7. 渲染聊天对话
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Flowise 后端 API 调用
# 对应您的“AI博主大脑”或“研究顾问”的 API ID
API_URL = "https://cloud.flowiseai.com/api/v1/prediction/bf9603b5-6f62-4e3b-a48e-c0e52e30c963"

if prompt := st.chat_input("输入孩子目前的学习情况，例如：五年级，自学过一年乐高..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner('研究顾问正在查阅 4A 评价模型...'):
                response = requests.post(API_URL, json={"question": prompt})
                response.raise_for_status()
                res_json = response.json()
                # 兼容 Flowise 不同输出格式
                answer = res_json.get("text") or res_json.get("response") or "系统忙，请稍后再试。"
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("⚠️ 顾问服务暂时无法连接。请检查 Flowise 后端设置。")
