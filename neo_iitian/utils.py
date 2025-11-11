import streamlit as st

def show_message(role, message):
    """Stylish chat message with role distinction."""
    if role == "user":
        st.markdown(
            f"<div style='background-color:#0e76a8;padding:10px;border-radius:10px;color:white;text-align:right;margin-bottom:10px;'>💬 You: {message}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background-color:#f1f1f1;padding:10px;border-radius:10px;color:#333;margin-bottom:10px;'>🤖 NeoIITian: {message}</div>",
            unsafe_allow_html=True,
        )
