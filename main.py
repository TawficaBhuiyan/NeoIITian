import streamlit as st
import json
import os
from datetime import date
from neo_iitian.chatbot import get_response
from neo_iitian.utils import show_message

# ==== 🧠 Persistent chat history ====
CHAT_HISTORY_FILE = f"chat_history_{date.today()}.json"

def load_history():
    """Load chat history from a local JSON file."""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_history(history):
    """Save current chat history to a JSON file."""
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
# ====================================

# Streamlit setup
st.set_page_config(page_title="NeoIITian | CS Chatbot", page_icon="🤖", layout="centered")

st.markdown(
    """
    <h1 style='text-align:center; color:#0e76a8;'>🤖 NeoIITian</h1>
    <h4 style='text-align:center; color:gray;'>Your Personal Software Engineer Assistant</h4>
    <hr>
    """,
    unsafe_allow_html=True,
)

# Load session
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# ===== 📜 Sidebar: Saved chat & options =====
with st.sidebar:
    st.subheader("💾 Chat History")

    # Show last 15 messages
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            if len(data) == 0:
                st.info("No messages yet.")
            else:
                for i, msg in enumerate(data[-15:]):
                    role = "🧑‍💻 You" if msg["role"] == "user" else "🤖 Bot"
                    st.markdown(f"**{i}. {role}:** {msg['content'][:100]}{'...' if len(msg['content'])>100 else ''}")

                # Delete one chat
                st.markdown("---")
                st.write("**Delete a specific message:**")
                delete_index = st.number_input("Enter message index:", min_value=0, max_value=len(data)-1, step=1)
                if st.button("❌ Delete Selected Message"):
                    del data[delete_index]
                    save_history(data)
                    st.session_state.messages = data
                    st.success("Message deleted successfully!")
                    st.experimental_rerun()

        except Exception as e:
            st.warning(f"⚠️ Could not load history: {e}")
    else:
        st.info("No saved chat yet! Start chatting 👇")

    # Delete all chats
    st.markdown("---")
    if st.button("🗑️ Delete All History"):
        st.session_state.messages = []
        save_history([])
        st.success("All chat history deleted!")
        st.experimental_rerun()
# ============================================

# Chat input
user_input = st.chat_input("Ask me anything about Computer Science...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = get_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": response})
    save_history(st.session_state.messages)  # 💾 Save after each message

# Display chat history in main area
for msg in st.session_state.messages:
    show_message(msg["role"], msg["content"])

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Built with ❤️ by Tawfica Bhuiyan | Powered by LangChain + Gemini")
