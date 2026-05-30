import streamlit as st
from src.rag import answer_question

st.set_page_config(
    page_title="Acme RAG Assistant",
    page_icon="🏢",
    layout="centered",
)

st.title("Acme Solutions RAG Assistant")
st.caption("Ask questions about Acme internal company knowledge base.")

question = st.text_input(
    "Your question",
    placeholder="Example: How do I connect to the corporate VPN?",
)

if st.button("Ask") and question:
    with st.spinner("Searching the knowledge base..."):
        result = answer_question(question)

    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Sources")
    for source in result["sources"]:
        st.markdown(f"- `{source}`")

    with st.expander("Retrieved context"):
        for item in result["contexts"]:
            st.markdown(f"**{item['source']}**")
            st.write(item["text"])
            st.divider()
