import requests
import streamlit as st

# Configure the page
st.set_page_config(
    page_title="What Would Hamming Do?",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    
    .stChatMessage {
        margin-bottom: 1rem;
    }
    
    .disclaimer {
        position: fixed;
        bottom: 10px;
        left: 50%;
        transform: translateX(-50%);
        background: #f0f2f6;
        padding: 5px 12px;
        border-radius: 4px;
        font-size: 11px;
        color: #666;
        border: 1px solid #e0e0e0;
        z-index: 1000;
    }
</style>
<div class="disclaimer">
    This project is for educational purposes only and has no commercial intent. Not affiliated with any organization.
</div>
""", unsafe_allow_html=True)

st.title("What Would Hamming Do?")

# Init chat and keep track of history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages from chat history on app retun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your research, don't be shy"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.text(prompt)

    response = requests.get(
            f"http://localhost:8000/chat", params={"msg": prompt}
    )
    response.raise_for_status()

    with st.chat_message("assistant"):
        st.markdown(response.text)
