import streamlit as st
import requests

st.title("ChatGPT-like clone")

# Set a default model
if "huggingface_model" not in st.session_state:
    st.session_state["huggingface_model"] = "microsoft/DialoGPT-large"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hugging Face API URL
API_URL = f"https://api-inference.huggingface.co/models/{st.session_state['huggingface_model']}"

# Hugging Face API headers
headers = {"Authorization": f"Bearer {st.secrets['hf_key']}"}

# Function to query the model
def query(payload):
    payload["parameters"] = {"max_length": 400}
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Generate assistant response
    response = query({"inputs": st.session_state.messages})
    # st.write(response)
    # Extract the assistant's message from the response
    assistant_message = response[-1]["generated_text"][-1]["content"]
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_message)
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})