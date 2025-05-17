import streamlit as st
import requests

st.set_page_config(page_title="PDF ChatBot", layout="centered")
st.title("📄🧠 Ask Questions from your PDF")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []  # {"role": "user"/"assistant", "content": "..."}

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file and "pdf_uploaded" not in st.session_state:
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    with st.spinner("Uploading..."):
        response = requests.post("http://localhost:8000/UploadingPDF/", files=files)

    if response.status_code == 200:
        st.success("PDF uploaded and processed successfully.")
        st.session_state["pdf_uploaded"] = True
    else:
        st.error(f"Upload failed. Status code: {response.status_code}")

# Only show chat if PDF is uploaded
if st.session_state.get("pdf_uploaded"):

    # Input box and submit button
    with st.form("chat_form"):
        query = st.text_input("Ask a question based on the PDF:")
        submitted = st.form_submit_button("Send")

    # Handle new user query
    if submitted and query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.spinner("Thinking..."):
            try:
                res = requests.post("http://localhost:8000/ChatBot/", data={"query": query})
                if res.status_code == 200:
                    reply = res.json()
                    reply_text = reply if isinstance(reply, str) else str(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply_text})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": f"[Error {res.status_code}]"})
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"[Exception: {e}]"})

    # Show chat history (after submitting)
    st.subheader("Chat History")
    for i, msg in enumerate(st.session_state.messages):
        label = "You" if msg["role"] == "user" else "Bot"
        st.text_area(label=label, value=msg["content"], height=100, key=f"msg_{i}")
