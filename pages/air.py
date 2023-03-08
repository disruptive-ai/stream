from pyairtable import Table
import streamlit as st

api_key = st.secrets['AIRTABLE_TOKEN']

quizmee_base = 'appNzH6XZUdVUrao0'
table = Table(api_key, quizmee_base, 'Videos')

for records in table.iterate(page_size=10, max_records=1000):
    # Print the record fields
    for record in records:
        title = record['fields']['Title']
        fields = record['fields']
        # intro_audio = 
        # print(intro_audio)
        expander = st.expander(str(title))
        expander.write(fields)

