import streamlit as st
import openai

# Set up OpenAI API credentials
openai.api_key = st.secrets['OPENAI_KEY']

st.header("OpenAI Chat API")

### FOR THE ENTER BUTTON
input_key = "my_input" # Define a unique key for the text input
input_value = "" # Define a placeholder value for the input

# Define a function to execute when the button is clicked
def on_button_click():
    # Get the current value of the text input
    input_value = st.session_state[input_key]

    # a ChatCompletion request
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': input_value}
        ],
        stream=True  # streamed
    )

    # create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    for chunk in response:
        collected_chunks.append(chunk)  # save the event response
        if 'choices' in chunk and chunk['choices']:  # check if 'choices' key exists and is not empty
            chunk_message = chunk['choices'][0]['delta']  # extract the message
            if chunk_message:  # check if message is not empty
                collected_messages.append(chunk_message)  # save the message
        stream_content = ''.join([s.get('content', '') for s in collected_messages if s])  # add check for empty strings
        # print(stream_content) # use for troubleshooting
        stream_content = stream_content.strip()  # remove leading/trailing whitespace
        res_box.markdown(stream_content)

# Create the text input box
user_input = st.text_input("Prompt", placeholder="Ask anything and press Enter", key=input_key)

# Store the current value of the text input in session state
if input_key not in st.session_state:
    st.session_state[input_key] = input_value
else:
    input_value = st.session_state[input_key]

# Create a button widget and define its behavior when clicked
button = st.button("Send")
if button:
    on_button_click()

res_box = st.empty()

# show in the text box
# res_box.markdown(f'*{stream_content}*')

# print the text received
# full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
# print(f"Full conversation received: {full_reply_content}")
