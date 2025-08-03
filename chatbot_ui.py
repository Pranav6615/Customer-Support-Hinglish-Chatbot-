import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal::Bzmrn6Yp"

st.set_page_config(page_title="Hinglish Support Bot", layout="centered")
st.title("💬 Hinglish Support Bot Demo")
st.caption("You can ask up to 5 questions in this demo.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# Limit check
if st.session_state.query_count >= 5:
    st.warning("🛑 You’ve reached the 5-message demo limit.")
    st.stop()

# Show past messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input field
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    st.session_state.query_count += 1

    try:
        response = openai.ChatCompletion.create(
            model=FINE_TUNED_MODEL,
            messages=st.session_state.messages
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)
