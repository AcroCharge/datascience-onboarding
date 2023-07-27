import pandas as pd
import streamlit as st
from prompt_func import get_response
import pandas as pd
import ast

st.image("https://media.istockphoto.com/id/1146670231/vector/rubber-duck-vector-illustration.jpg?s=612x612&w=0&k=20&c=75fuQJhx-j5Q9O1ndmeunLPBKbrQxsTcZ1I6DYbVsnY=", width=100)
st.text_input("URL", key="URL")

# access the value
url = st.session_state.URL

if st.button('GO!'):
    response = get_response(url)
    st.header(f"URL: {url}")
    merchant_name = ast.literal_eval(response[0])["company"]
    description = ast.literal_eval(response[1])["description"]
    st.subheader("Merchant name")
    st.write(merchant_name)
    st.subheader("Merchant description")
    st.write(description)
    st.write(pd.DataFrame({"question": ["merchant", "description"], "answer": [merchant_name, description]}))
    st.write('response: ', response)

