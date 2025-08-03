import streamlit as st
from openai import OpenAI

# Setup OpenAI client with secret key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Your fine-tuned model name
FINE_TUNED_MODEL = "ft:gpt-3.5-turbo-0125:personal::Bzmrn6Yp"

# Streamlit UI setup
st.set_page_config(page_title="Hinglish Support Bot", layout="centered")
st.title("💬 Hinglish Support Bot Demo")
st.caption(
    "🧠 This Hinglish Support Bot is a ready-to-integrate customer support assistant, "
    "fine-tuned for formal Hinglish conversations. It can be customized for any company’s FAQs, "
    "policies, and support tone.\n\n"
    "🌐 Why Hinglish? A large segment of Indian users prefer a mix of Hindi and English — "
    "making support more relatable, accessible, and human.\n\n"
    "✅ Try asking about orders, payments, returns, or delivery in Hinglish. "
    "You’ll see how smoothly it handles real-world support scenarios."
    "You can ask upto 5 queries in this demo"
    "Example query to start => "Kya mera order dispatch ho gaya hai?" or "Kya aap EMI options provide karte hain?" "
)


# Initialize session state for chat history and query count
if "messages" not in st.session_state:
    st.session_state.messages = []

if "query_count" not in st.session_state:
    st.session_state.query_count = 0

# Enforce query limit
if st.session_state.query_count >= 5:
    st.warning("🛑 You’ve reached the 5-message demo limit.")
    st.stop()

# Show chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Input field
if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    st.session_state.query_count += 1

    try:
        # Make API call to fine-tuned model
        response = client.chat.completions.create(
            model=FINE_TUNED_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful customer support agent."},
                *st.session_state.messages
            ]
        )
        reply = response.choices[0].message.content

    except Exception as e:
        reply = f"❌ Error: {str(e)}"

    # Display and store assistant response
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").markdown(reply)

