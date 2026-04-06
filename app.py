import streamlit as st
import time
import os
from chatbot import BankingChatbot


st.set_page_config(
    page_title="Banking Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: #1A1A1A; }
#MainMenu, footer, header   { visibility: hidden; }
.block-container            { padding: 2rem 2.5rem 1.5rem 2.5rem; }

/* sidebar */
section[data-testid="stSidebar"] {
    background-color: #FAFAFA;
    border-right: 1px solid #EBEBEB;
}
section[data-testid="stSidebar"] * { color: #1A1A1A !important; }

section[data-testid="stSidebar"] .stButton button {
    background: #FFFFFF;
    border: 1px solid #E4E4E4;
    color: #2D2D2D !important;
    border-radius: 6px;
    text-align: left;
    padding: 0.45rem 0.85rem;
    font-size: 0.84rem;
    width: 100%;
    font-weight: 400;
    transition: all 0.15s ease;
    margin-bottom: 2px;
    box-shadow: none;
}
section[data-testid="stSidebar"] .stButton button:hover {
    background: #F5F5F5;
    border-color: #CACACA;
}

/* page header */
.page-header {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    padding-bottom: 1.1rem;
    border-bottom: 1px solid #EBEBEB;
    margin-bottom: 1.5rem;
}
.header-title { font-size: 1.2rem; font-weight: 600; color: #FAFAFA; margin: 0; }
.header-sub   { font-size: 0.78rem; color: #9A9A9A; margin: 0.1rem 0 0 0; }
.header-tag {
    margin-left: auto;
    font-size: 0.7rem; font-weight: 500;
    color: #FAFAFA; background: #0D1B3E;
    border: 1px solid #E5E7EB; border-radius: 4px;
    padding: 0.2rem 0.6rem;
    text-transform: uppercase; letter-spacing: 0.04em;
}

/* chat bubbles */
.msg-row          { display: flex; align-items: flex-end; gap: 0.55rem; margin-bottom: 1.1rem; }
.msg-row.user     { justify-content: flex-end; }
.msg-row.bot      { justify-content: flex-start; }
.bubble           { padding: 0.7rem 1rem; border-radius: 14px; max-width: 68%; font-size: 0.93rem; line-height: 1.6; }
.msg-row.user .bubble { background: #0D1B3E; color: #FFF; border-radius: 14px 14px 3px 14px; }
.msg-row.bot  .bubble { background: #FFF !important; color: #1A1A1A !important; border: 1px solid #EBEBEB; border-radius: 14px 14px 14px 3px; }
.avatar       { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; flex-shrink: 0; }
.avatar.user  { background: #E8ECF5; color: #0D1B3E; }
.avatar.bot   { background: #F3F4F6; color: #555; border: 1px solid #E5E7EB; }

/* welcome screen */
.welcome { text-align: center; padding: 3rem 1.5rem; }
.welcome p { font-size: 0.9rem; line-height: 1.7; color: #B0B0B0; max-width: 360px; margin: 0 auto; }

/* stat pills */
.stat-row  { display: flex; gap: 0.5rem; margin-bottom: 1rem; }
.stat-pill { flex: 1; background: #F3F4F6; border: 1px solid #E5E7EB; border-radius: 8px; padding: 0.55rem 0.5rem; text-align: center; }
.stat-pill .num { font-size: 1.25rem; font-weight: 600; color: #0D1B3E !important; }
.stat-pill .lbl { font-size: 0.68rem; color: #9CA3AF !important; }

.section-label {
    font-size: 0.7rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.08em;
    color: #AAAAAA !important; margin: 1.2rem 0 0.5rem 0;
}

/* input */
.stTextInput input {
    border: 1px solid #DCDCDC !important;
    border-radius: 8px !important;
    padding: 0.6rem 0.9rem !important;
    font-size: 0.92rem !important;
    background: #FFF !important;
    color: #1A1A1A !important;
    box-shadow: none !important;
    transition: border-color 0.15s !important;
}
.stTextInput input:focus  { border-color: #0D1B3E !important; box-shadow: none !important; }
.stTextInput input::placeholder { color: #BBBBBB !important; }

/* send button */
div[data-testid="column"]:last-child .stButton button {
    background: #0D1B3E !important;
    color: #FFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    height: 2.62rem !important;
    width: 100% !important;
    font-size: 0.88rem !important;
    box-shadow: none !important;
    transition: background 0.15s !important;
}
div[data-testid="column"]:last-child .stButton button:hover { background: #162550 !important; }

/* scroll area */
.msgs-wrap { min-height: 200px; max-height: 56vh; overflow-y: auto; padding: 0.5rem 0.25rem 0.5rem 0; }
.msgs-wrap::-webkit-scrollbar { width: 3px; }
.msgs-wrap::-webkit-scrollbar-thumb { background: #E0E0E0; border-radius: 3px; }

.input-area { margin-top: 1.2rem; border-top: 1px solid #EBEBEB; padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)


# load chatbot once and cache it so it doesn't reload on every interaction
@st.cache_resource(show_spinner=False)
def load_chatbot():
    return BankingChatbot()


# session state defaults
if "messages"    not in st.session_state: st.session_state.messages    = []
if "query_count" not in st.session_state: st.session_state.query_count = 0
if "input_key"   not in st.session_state: st.session_state.input_key   = 0


# ── sidebar ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("#### Banking Assistant")
    st.markdown("<hr style='border:none;border-top:1px solid #EBEBEB;margin:0.6rem 0 0.9rem 0;'>",
                unsafe_allow_html=True)

    st.markdown(f"""
    <div class='stat-row'>
      <div class='stat-pill'><div class='num'>10</div><div class='lbl'>Q&A Entries</div></div>
      <div class='stat-pill'><div class='num'>{st.session_state.query_count}</div><div class='lbl'>Queries</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Try asking</div>", unsafe_allow_html=True)

    sample_questions = [
        "What is KYC?",
        "What is a savings account?",
        "Documents to open a bank account?",
        "How does UPI work?",
        "What is a credit score?",
        "Debit card vs credit card?",
        "What is a fixed deposit?",
        "How to avoid banking fraud?",
    ]
    for q in sample_questions:
        if st.button(q, key=f"sq_{q}"):
            st.session_state["prefill"] = q
            st.rerun()

    st.markdown("<hr style='border:none;border-top:1px solid #EBEBEB;margin:1rem 0 0.8rem 0;'>",
                unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Clear conversation", key="clear_btn"):
        st.session_state.messages    = []
        st.session_state.query_count = 0
        st.session_state.input_key  += 1
        st.rerun()


# ── main area ─────────────────────────────────────────────────────────────
st.markdown("""
<div class='page-header'>
  <div style='font-size:1.6rem;'>🏦</div>
  <div>
    <div class='header-title'>AI Banking Assistant</div>
    <div class='header-sub'>Sentence Transformers · RAG · LLM</div>
  </div>
</div>
""", unsafe_allow_html=True)

with st.spinner("Loading model..."):
    bot = load_chatbot()

# build the chat HTML
if not st.session_state.messages:
    chat_html = """
    <div class='welcome'>
      <div style='font-size:2rem; margin-bottom:0.75rem;'>💬</div>
      <p>Ask me anything about banking — accounts, KYC, loans, UPI, credit scores, and more.</p>
    </div>"""
else:
    chat_html = ""
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            chat_html += f"""
            <div class='msg-row user'>
              <div class='bubble'>{msg['content']}</div>
              <div class='avatar user'>You</div>
            </div>"""
        else:
            chat_html += f"""
            <div class='msg-row bot'>
              <div class='avatar bot'>🤖</div>
              <div class='bubble'>{msg['content']}</div>
            </div>"""

st.markdown(f"<div class='msgs-wrap'>{chat_html}</div>", unsafe_allow_html=True)

# input area
st.markdown("<div class='input-area'>", unsafe_allow_html=True)
prefill = st.session_state.pop("prefill", "")
col_in, col_btn = st.columns([6, 1])

with col_in:
    user_input = st.text_input(
        label="",
        placeholder="Type a question...",
        key=f"inp_{st.session_state.input_key}",
        value=prefill,
        label_visibility="collapsed",
    )
with col_btn:
    send = st.button("Send", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# handle user message
if (send or user_input) and user_input.strip():
    query = user_input.strip()
    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.query_count += 1

    with st.spinner(""):
        time.sleep(0.25)
        reply = bot.ask(query)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.input_key += 1
    st.rerun()
