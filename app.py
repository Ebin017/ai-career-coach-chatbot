import streamlit as st
from chatbot import get_response, analyze_resume
from resume_parser import extract_text_from_pdf
from rag_pipeline import create_vector_store

st.set_page_config(page_title="AI Career Coach", layout="wide")

# -------- TITLE --------
st.title("💼 AI Career Coach")

# -------- SESSION STATE --------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

# -------- TABS --------
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📄 Resume Analysis", "📌 Resume Chat"])

# ================= TAB 1: CHAT =================
with tab1:
    st.subheader("Chat with AI Career Coach")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history ONLY
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input at bottom
    prompt = st.chat_input("Ask your career question...")

    if prompt:
        

        # Generate response with spinner
        with st.spinner("Thinking... 🤔"):
            response = get_response(prompt)

        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        # Rerun to refresh UI (important)
        st.rerun()


# ================= TAB 2: RESUME ANALYSIS =================
with tab2:
    st.subheader("Resume Analyzer")

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")

    if uploaded_file is not None:
        if st.session_state.vectorstore is None:
            resume_text = extract_text_from_pdf(uploaded_file)
            st.session_state.resume_text = resume_text
            st.session_state.vectorstore = create_vector_store(resume_text)

        st.success("✅ Resume uploaded and processed")

        if st.button("🔍 Analyze Resume"):
            with st.spinner("Analyzing your resume... 📄"):
                result = analyze_resume(st.session_state.resume_text)

            st.markdown("### 📊 Analysis")
            st.write(result)

    else:
        st.info("Upload your resume to analyze")


# ================= TAB 3: RESUME CHAT =================
with tab3:
    st.subheader("Ask Questions About Your Resume")

    if st.session_state.vectorstore is not None:
        question = st.text_input("Ask something about your resume")

        if question:
            with st.spinner("Searching your resume... 🔍"):
                docs = st.session_state.vectorstore.similarity_search(question, k=2)
                context = "\n".join([doc.page_content for doc in docs])

                prompt = f"""
                You are an AI career coach.

                Use this resume context:
                {context}

                Answer clearly:
                {question}
                """

                answer = get_response(prompt)

            st.markdown("### 📌 Answer")
            st.write(answer)

    else:
        st.warning("⚠️ Please upload your resume first in the Resume Analysis tab")