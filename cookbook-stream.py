import streamlit as st
import openai

# Set up OpenAI API credentials
openai.api_key = st.secrets['OPENAI_KEY']

st.header("Streamed Chat API")

# Create the text input box
user_input = st.text_input("Prompt", placeholder="Ask anything and press Enter", key="", on_change="")
res_box = st.empty()

# a ChatCompletion request
response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {'role': 'user', 'content': "List 5 reasons to be happy"}
    ],
    stream=True  # streamed
)

# create variables to collect the stream of chunks
collected_chunks = []
collected_messages = []
for chunk in response:
    collected_chunks.append(chunk)  # save the event response
    chunk_message = chunk['choices'][0]['delta']  # extract the message
    if chunk_message:  # check if message is not empty
        collected_messages.append(chunk_message)  # save the message
    stream_content = ''.join([s.get('content', '') for s in collected_messages])
    print(stream_content)

# show in the text box
res_box.markdown(f'*{stream_content}*')

# print the text received
# full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
# print(f"Full conversation received: {full_reply_content}")

