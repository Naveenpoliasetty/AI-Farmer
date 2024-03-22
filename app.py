#from chatbot import llm
import textwrap
import streamlit as st
import google.generativeai as genai
from IPython.display import Markdown

from streamlit_chat import message
from streamlit.components.v1 import html

genai.configure(api_key='AIzaSyBh1c2YuWKm5il20oDPWezy3hly_cHYdn0')
model = genai.GenerativeModel('gemini-pro')

def to_markdown(text):
  text = text.replace('.', '*')
  return Markdown(textwrap.indent(text,'>',predicate= lambda _:True))

with st.sidebar:
    st.title('🌾Agriculture Expert')

def llm(text):
    text = 'Behave as an expert in agriculture.\n' + text
    response = model.generate_content(text)
    return response.text

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{'role':'assistant','content':'Hey what is up!'}]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hey What is up!"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


def llm_response(prompt_input):
    for dict_message in st.session_state.messages:
        string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond  as an 'Assistant'.\n "
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = llm(prompt_input)
    return output


# User-provided prompt
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

