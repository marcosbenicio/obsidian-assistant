import streamlit as st

from search import hybrid_search
from metrics import RAGWithMetrics
from db import save_conversation, save_feedback


@st.cache_resource
def get_assistant():
    # llm client comes from the env-driven factory in rag.py: OpenAI by
    # default, any OpenAI-compatible server (Ollama) via LLM_BASE_URL
    return RAGWithMetrics(search_fn=hybrid_search)


assistant = get_assistant()

st.title("Obsidian Assistant")

user_input = st.text_input("Ask your vault:")

if st.button("Ask"):
    with st.spinner("Searching your notes..."):
        answer = assistant.rag(user_input)
        st.write(answer)

        record = assistant.last_call
        st.caption(
            f"{record.response_time:.2f}s | "
            f"{record.prompt_tokens} in / {record.completion_tokens} out | "
            f"${record.cost:.4f}"
        )

        conversation_id = save_conversation(record, user_input)
        st.session_state.conversation_id = conversation_id

col1, col2 = st.columns(2)

with col1:
    if st.button("+1") and "conversation_id" in st.session_state:
        save_feedback(st.session_state.conversation_id, "user", score=1)
        st.toast("Thanks!")

with col2:
    if st.button("-1") and "conversation_id" in st.session_state:
        save_feedback(st.session_state.conversation_id, "user", score=-1)
        st.toast("Noted.")
