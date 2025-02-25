import streamlit as st
import requests

FASTAPI_URL= "http://localhost:8000/"

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Document Chatbot with FastAPI & Streamlit")
st.write("Upload a document and chat with it using Deepseek-RAG.")

st.subheader("Upload a Document")
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with st.spinner("Uploading and processing..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(f"{FASTAPI_URL}/add_document/", files=files)
        
        if response.status_code == 200:
            st.success("Document uploaded successfully!")
        else:
            st.error("Upload failed. Please try again.")


st.subheader("💬 Chat with the Document")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask something about the document...")

if user_input and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        # response = requests.post(f"{FASTAPI_URL}/chat/", json={"query": user_input})
        response = requests.post(f"{FASTAPI_URL}/chat/", params={"chat": user_input})

        if response.status_code == 200:
            result = response.json().get("answer", "No response received.")
        else:
            result = "Error: Could not retrieve response."

    st.session_state.messages.append({"role": "deepseek", "content": result})

    with st.chat_message("deepseek"):
        st.markdown(result)
