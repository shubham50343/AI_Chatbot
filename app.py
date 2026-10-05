import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------
# LOAD ENVIRONMENT VARIABLES
# -----------------------------
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 25px;
    }

    .stChatMessage {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown(
    '<div class="main-title">🤖 AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Powered by Groq AI + Streamlit</div>',
    unsafe_allow_html=True
)

# -----------------------------
# API CHECK
# -----------------------------
if not api_key:
    st.error(
        "GROQ_API_KEY nahi mili. Apni .env file check karo."
    )
    st.stop()

# -----------------------------
# GROQ CLIENT
# -----------------------------
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

# -----------------------------
# CHAT HISTORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful AI assistant. "
                "Answer clearly and politely. "
                "You can understand English and Hindi/Hinglish. "
                "Keep answers easy to understand."
            )
        }
    ]

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("⚙️ Settings")

    st.write("### Chatbot")
    st.write("AI Chatbot using Streamlit and Groq API.")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Answer clearly and politely. "
                    "You can understand English and Hindi/Hinglish. "
                    "Keep answers easy to understand."
                )
            }
        ]
        st.rerun()

    st.divider()

    st.write("**Model:**")
    st.code("openai/gpt-oss-20b")

# -----------------------------
# DISPLAY OLD MESSAGES
# -----------------------------
for message in st.session_state.messages:

    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input(
    "Type your message here..."
)

# -----------------------------
# PROCESS MESSAGE
# -----------------------------
if user_input:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=st.session_state.messages,
                    temperature=0.7,
                    max_tokens=2048
                )

                answer = response.choices[0].message.content

                st.markdown(answer)

                # Save response in history
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error(
                    "AI response generate nahi ho paaya."
                )

                st.code(str(e))