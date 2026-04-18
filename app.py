import streamlit as st
import sqlite3
import re
import json
import streamlit.components.v1 as components

# --- 听力引擎 ---
def play_audio_button(text):
    clean_text = text.replace('\n', ' ').replace("'", "\\'")
    html_code = f"""
    <button onclick="
        var msg = new SpeechSynthesisUtterance('{clean_text}');
        msg.lang = 'en-US';
        msg.rate = 0.9;
        window.speechSynthesis.speak(msg);
    " style="background-color:#4CAF50; color:white; border:none; padding:8px 16px; border-radius:5px; cursor:pointer; font-weight:bold; margin-bottom:10px;">
    🔊 播放英文情景对话
    </button>
    """
    components.html(html_code, height=50)

# --- 网页基础设置 ---
st.set_page_config(page_title="科研&创投 3.0 (云端版)", layout="centered", page_icon="☁️")

# --- 云端专属改造：侧边栏进度控制器 ---
st.sidebar.title("🧭 导航台")
st.sidebar.markdown("---")
# 你可以根据数据库里实际的数据量（目前是14天），调整 max_value
day = st.sidebar.number_input("👉 请选择当前进度 (Day):", min_value=1, max_value=14, value=1, step=1)
st.sidebar.markdown("*(注：云端服务器为无状态模式，进度由你全权手动掌控)*")

st.title(f"🚀 深度学习台 - Day {day}")
is_exam_day = (day > 0 and day % 7 == 0)

conn = sqlite3.connect('learning.db')
cursor = conn.cursor()

if is_exam_day:
    # 考试模块
    st.header("📝 阶段实战测验")
    if 'exam_questions' not in st.session_state or st.session_state.get('exam_day') != day:
        cursor.execute("SELECT vocab, material FROM ai_english WHERE id < ? ORDER BY RANDOM() LIMIT 3", (day,))
        st.session_state.exam_questions = cursor.fetchall()
        st.session_state.exam_day = day
        st.session_state.submitted = False
    
    questions = st.session_state.exam_questions
    if questions:
        user_inputs = []
        for i, q in enumerate(questions):
            eng_word = q[0].split('(')[0].strip()
            pattern = re.compile(re.escape(eng_word), re.IGNORECASE)
            blanked = pattern.sub("【 _________ 】", q[1])
            st.markdown(f"**Q{i+1}**: *{blanked}*")
            ans = st.text_input("填入英文：", key=f"ans_{i}")
            user_inputs.append((ans, eng_word))
            st.markdown("---")
        
        if st.button("✅ 提交试卷"):
            st.session_state.submitted = True
            st.rerun()
            
        if st.session_state.submitted:
            for i, (ans, correct) in enumerate(user_inputs):
                if ans.strip().lower() == correct.lower():
                    st.success(f"Q{i+1}: 正确 ({correct})")
                else:
                    st.error(f"Q{i+1}: 错误。正解: {correct}")
            st.info("🎯 考试结束！请在左侧边栏增加天数，进入下一阶段。")

else:
    # 正常学习模式
    cursor.execute("SELECT vocab, definition, material, dialogue FROM ai_english WHERE id = ?", (day,))
    eng = cursor.fetchone()
    cursor.execute("SELECT concept, explanation, case_study, sandbox FROM vc_finance WHERE id = ?", (day,))
    vc = cursor.fetchone()

    if eng and vc:
        t1, t2, t3 = st.tabs(["🔬 医疗AI商务英语", "💼 VC创投实战", "🕹️ 动态决策沙盘"])
        
        with t1:
            st.header(f"🎯 {eng[0]}")
            st.caption("概念释义：" + (eng[1] if eng[1] else "暂无"))
            st.info(f"**核心句型：**\n{eng[2]}")
            if eng[3]:
                st.markdown("### 🎙️ 实战情景对话")
                play_audio_button(eng[3])
                st.code(eng[3], language="text")

        with t2:
            st.header(f"💡 {vc[0]}")
            st.success(f"**投资逻辑：**\n{vc[1]}")
            if vc[2]:
                st.markdown("### 🏢 真实/推演案例")
                st.warning(vc[2])
        
        with t3:
            st.header("🧠 VC Deal 模拟推演室")
            st.markdown("---")
            sandbox_raw = vc[3]
            if not sandbox_raw:
                st.write("📭 今天的知识点没有配置沙盘实战。")
            else:
                sb_data = json.loads(sandbox_raw) 
                state_key = f"sb_step_{day}"
                if state_key not in st.session_state:
                    st.session_state[state_key] = 1

                current_step = st.session_state[state_key]

                if current_step == 1:
                    st.markdown(f"#### 📁 {sb_data.get('project_name')}")
                    st.info(f"**项目背景**：{sb_data.get('background')}")
                    
                    st.markdown("👇 **请做出你的投资或管理决策：**")
                    options = sb_data.get('options', {})
                    for opt_key, opt_text in options.items():
                        if st.button(f"选项 {opt_key}：{opt_text}"):
                            st.session_state[state_key] = opt_key
                            st.rerun()

                elif current_step in ['A', 'B', 'C']:
                    outcomes = sb_data.get('outcomes', {})
                    result = outcomes.get(current_step, {})
                    msg_type = result.get('type', 'info')
                    title = result.get('title', '复盘')
                    text = result.get('text', '')
                    
                    if msg_type == 'error':
                        st.error(f"💥 {title}")
                    elif msg_type == 'success':
                        st.success(f"✅ {title}")
                    else:
                        st.warning(f"⚠️ {title}")
                        
                    st.write(f"**复盘解析：** {text}")
                    
                    if st.button("🔄 重新推演本次沙盘"):
                        st.session_state[state_key] = 1
                        st.rerun()

        st.markdown("---")
        st.info("✅ 今日学习完毕？请在左侧导航栏调整天数 (Day) 进入下一章节！")
    else:
        st.warning("📚 当前天数暂无内容。")

conn.close()