import streamlit as st
import urllib.parse
import difflib

# إعدادات الصفحة
st.set_page_config(page_title="Mira AI - Web Engine", page_icon="🤖", layout="centered")

st.title("🤖 Mira AI - Autonomous Agent")
st.caption("Engineered with ♥ by Ashraf")

# قاعدة البيانات المبسطة
known_games = {
    "كول اوف ديوتي": "Call of Duty",
    "رزدنت ايفل": "Resident Evil",
    "قراند": "Grand Theft Auto V"
}

# تهيئة الذاكرة للدردشة
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "مرحباً يا ميرّا، أنا أشرف AI. ماذا سنلعب اليوم؟"}]

# عرض الدردشة السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إدخال المستخدم
if prompt := st.chat_input("اكتبي اسم اللعبة أو سؤالك هنا..."):
    # إضافة رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # معالجة الذكاء الاصطناعي
    with st.chat_message("assistant"):
        if "كيف" in prompt or "شرح" in prompt:
            response = "لتحميل اللعبة، تأكدي من إيقاف مانع الإعلانات، ثم اضغطي على روابط التحميل المباشرة (Direct Links)."
            st.markdown(response)
        else:
            # مطابقة اسم اللعبة
            matches = difflib.get_close_matches(prompt, known_games.keys(), n=1, cutoff=0.5)
            game_name = known_games[matches[0]] if matches else prompt
            
            response = f"جاري تحضير روابط البحث للعبة: **{game_name}**"
            st.markdown(response)
            
            safe_query = urllib.parse.quote(game_name)
            st.link_button("🎯 بحث في Steam", f"https://store.steampowered.com/search/?term={safe_query}")
            st.link_button("🔍 بحث في Google", f"https://www.google.com/search?q=تحميل+{safe_query}")

        st.session_state.messages.append({"role": "assistant", "content": response})