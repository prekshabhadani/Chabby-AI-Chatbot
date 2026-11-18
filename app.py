
import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

# --------------------------------
# LOAD API KEY
# --------------------------------

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("OPENROUTER_API_KEY")

# --------------------------------
# MODEL DETAILS
# --------------------------------

MODEL = "inclusionai/ling-3.2-flash:free"

# --------------------------------
# PAGE SETTINGS
# --------------------------------

st.set_page_config(
    page_title="Chabby 🌸",
    page_icon="🌷",
    layout="wide"
)

# --------------------------------
# FLORAL PINK DESIGN
# --------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 10% 10%, #fce4ec 0%, transparent 35%),
        radial-gradient(ellipse at 90% 90%, #f8dce8 0%, transparent 35%),
        #fffaf7;
    color: #71465a;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #a64d72 !important;
}

h1 {
    font-size: 3.2rem !important;
    text-align: center;
}

[data-testid="stSidebar"] {
    background: #fff0f5;
    border-right: 1px solid #f3d4df;
}

[data-testid="stSidebar"] h1 {
    font-size: 2rem !important;
}

[data-testid="stSidebar"] p {
    color: #a4778b !important;
}

[data-testid="stChatMessage"] {
    background: #fff8fa;
    border: 1px solid #f4d4df;
    border-radius: 22px;
    padding: 16px;
    margin-bottom: 15px;
    box-shadow: 0 5px 18px rgba(166,77,114,0.06);
}

[data-testid="stChatMessage"] p {
    color: #6b2945 !important;
}

/* Chat input */

[data-testid="stChatInput"] {
    background: #fff8fa !important;
    border: 1px solid #edc4d4 !important;
    border-radius: 25px !important;
}

[data-testid="stChatInput"] textarea {
    color: #6b2945 !important;
    -webkit-text-fill-color: #6b2945 !important;
    caret-color: #a64d72 !important;
    background: #fff8fa !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #b58a9b !important;
    -webkit-text-fill-color: #b58a9b !important;
    opacity: 1 !important;
}

/* Buttons */

.stButton button {
    background: linear-gradient(135deg, #d98baa, #b85f86);
    color: white !important;
    border: none;
    border-radius: 30px;
    padding: 10px 20px;
    transition: all 0.3s ease;
}

.stButton button:hover {
    background: #a64d72;
    transform: translateY(-2px);
}

/* Sidebar divider */

hr {
    border-color: #f1d3df;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# HEADER
# --------------------------------

st.title("🌷 Chabby 🌷")

st.markdown(
    "<p style='text-align:center; color:#b58a9b;'>"
    "a little garden of thoughts, ideas & conversations ♡"
    "</p>",
    unsafe_allow_html=True
)

# --------------------------------
# CHECK API KEY
# --------------------------------

if not API_KEY:
    st.error(
        "API key not found! Please check that your .env file "
        "contains OPENROUTER_API_KEY."
    )
    st.stop()

# --------------------------------
# CONNECT TO OPENROUTER
# --------------------------------

llm = ChatOpenAI(
    model=MODEL,
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7
)

# --------------------------------
# CHAT HISTORY
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.title("🌸 Chabby")

    st.write("your little garden companion")

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --------------------------------
# DISPLAY OLD MESSAGES
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------
# USER INPUT
# --------------------------------

prompt = st.chat_input("Ask me anything... 🌷")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare previous conversation
    chat_history = []

    for message in st.session_state.messages[:-1]:

        if message["role"] == "user":
            chat_history.append(
                HumanMessage(content=message["content"])
            )

        else:
            chat_history.append(
                AIMessage(content=message["content"])
            )

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Chabby is thinking... 🌸"):

            try:

                response = llm.invoke(
                    chat_history + [HumanMessage(content=prompt)]
                )

                answer = str(response.content)

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:

                st.error(
                    f"Chabby couldn't respond right now: {e}"
                )
