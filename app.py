import streamlit as st
import openai

# Set up OpenAI API credentials
openai.api_key = st.secrets['OPENAI_KEY']

st.header("OpenAI Chat API")

### FOR THE ENTER BUTTON
input_key = "my_input" # Define a unique key for the text input
input_value = "" # Define a placeholder value for the input

# Define a function to execute when the Enter key is pressed
def on_enter_pressed():
    # Get the current value of the text input
    input_value = st.session_state[input_key]

    # Do something with the input value
    st.write("You entered:", input_value)

user_input = st.text_input("Prompt", placeholder="Ask anything and press Enter", key=input_key, on_change=on_enter_pressed)

# Create the text output box
res_box = st.empty()

# Store the current value of the text input in session state
if input_key not in st.session_state:
    st.session_state[input_key] = input_value
else:
    input_value = st.session_state[input_key]

def on_button_click():
    # a ChatCompletion request
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {'role': 'user', 'content': user_input}
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
        
# Create a button widget and define its behavior when clicked
button = st.button("Send prompt")
if button:
    on_button_click()


# show in the text box
# res_box.markdown(f'*{stream_content}*')

# print the text received
# full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
# print(f"Full conversation received: {full_reply_content}")
