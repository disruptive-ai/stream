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

# Create the text input box
user_input = st.text_input("Prompt", placeholder="Ask anything and press Enter", key=input_key, on_change=on_enter_pressed)

# Store the current value of the text input in session state
if input_key not in st.session_state:
    st.session_state[input_key] = input_value
else:
    input_value = st.session_state[input_key]

res_box = st.empty()
combined = []
for resp in openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                    messages=[{"role": "user", "content": user_input}],
                                    max_tokens=120,
                                    stream = True):

    deltas = resp.choices[0].delta

    for obj in [deltas]:
        combined.append(obj)

    combined_string = ""
    for obj in combined:
        content = obj.get("content")
        if content is not None:
            combined_string += content

    # remove newline characters from the combined_string
    combined_string = combined_string.replace('\n', "")
    # print(combined_string) # use for troubleshooting

    # show in the text box
    res_box.markdown(f'*{combined_string.strip()}*')



### WORKING with no stream, dont change
# def stream_chat(prompt):
#     # create a new ChatCompletion object and set the "stream" parameter to True
#     completion = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}],
#         stream=False
#     )

#     print(completion)
#     st.text_area("Messages", value=completion.choices[0].message.content.strip())

# if __name__ == '__main__':
#     st.header("OpenAI Chat API")
#     user_input = st.text_input("Prompt", placeholder="Ask me anything...")
#     stream_chat(user_input)
