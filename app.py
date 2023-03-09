import streamlit as st
import openai

# Set up OpenAI API credentials
openai.api_key = st.secrets['OPENAI_KEY']

# Create the text output box
user_input = st.text_input("Prompt", label_visibility="hidden", placeholder="Ask anything and press Enter")

# Create the text output box
res_box = st.empty()
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

        # print the text received
        full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
        print(f"Full conversation received: {full_reply_content}")
        print(type(full_reply_content))

    numbered_list_str = full_reply_content
    # Split the string into a list of lines
    lines = numbered_list_str.splitlines()

    

    # Create a for loop to iterate through the items and create buttons for each one
    for line in lines:
        # Check if the line starts with a number
        if line.strip() and line[0].isdigit():
            parts = line.split(". ", 1)
            index = parts[0]
            text = parts[1]
            # Get the first three words of the item text and add "..." to the end
            short_text = " ".join(text.split()[:4]) + "..."
            st.button(f"{text}", key={index}, args={text}, use_container_width=True)



st.button("Send prompt", key="prompt_button", on_click=on_button_click)


# ##### TESTING WITH THINGS OUT OF ORDER #####
# st.text('This will appear first')
# # Appends some text to the app.

# my_slot1 = st.empty()
# # Appends an empty slot to the app. We'll use this later.

# my_slot2 = st.empty()
# # Appends another empty slot.

# st.text('This will appear last')
# # Appends some more text to the app.

# my_slot1.text('This will appear second')
# # Replaces the first empty slot with a text string.

# my_slot2.markdown('i am coming later')
# # Replaces the second empty slot with a chart.

### FOR THE ENTER BUTTON
# input_key = "my_input" # Define a unique key for the text input
# input_value = "" # Define a placeholder value for the input

# # Define a function to execute when the Enter key is pressed
# def on_enter_pressed():
#     # Get the current value of the text input
#     input_value = st.session_state[input_key]

#     # Do something with the input value
#     st.write("You entered:", input_value)

# Store the current value of the text input in session state
# if input_key not in st.session_state:
#     st.session_state[input_key] = input_value
# else:
#     input_value = st.session_state[input_key]

##### USE COLUMNS
# with st.container():
#    col1, col2, col3 = st.columns([1,3,1])

# with col1:
#     st.write("")  # placeholder to align columns

# with col2:
#     st.header("OpenAI Chat API")
#     # Create the text output box
#     # output_text = st.empty("Prompt Response", height=500)
#     st.empty()
#     st.write("")  # placeholder
#     st.write("")  # placeholder

# with col3:
#     st.write("")  # placeholder to align columns

# with col2:
#    user_input = st.text_input("Prompt", label_visibility="collapsed", placeholder="Ask anything and press Enter")



# show in the text box
# res_box.markdown(f'*{stream_content}*')
