import streamlit as st
import google.generativeai as genai
import os

# --- الإعدادات السحرية ---
MY_API_KEY = "AIzaSyCOdFVcx0W2pdlfh5uDTq-v5DN2zD2ZfWU" # حط مفتاحك هنا

# السطر ده بيجبر البرنامج يكلم النسخة المستقرة ويهرب من الـ 404
os.environ["GOOGLE_GENERATIVE_AI_NETWORK_ENDPOINT"] = "generativelanguage.googleapis.com"
genai.configure(api_key=MY_API_KEY)

# واجهة شيك وبسيطة
st.set_page_config(page_title="X ASSISTANT v2", page_icon="⚡")
st.markdown("<h1 style='text-align: center; color: #00f2fe;'>🤖 X ASSISTANT v2</h1>", unsafe_allow_html=True)

# الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إدخال المستخدم
if prompt := st.chat_input("تؤمرني بإيه يا حريف؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("بيفكر..."):
            try:
                # محاولة تشغيل أحدث موديل مستقر
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                res_text = response.text
                
                st.markdown(res_text)
                st.session_state.messages.append({"role": "assistant", "content": res_text})
            except Exception as e:
                st.error(f"السيرفر لسه معلق. جرب تعمل Reboot App")
                st.info(f"الخطأ: {e}")

# زرار مسح الشات في الجنب
if st.sidebar.button("🗑️ مسح المحادثة"):
    st.session_state.messages = []
    st.rerun()
  
