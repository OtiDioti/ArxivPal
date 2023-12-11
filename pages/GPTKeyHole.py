import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from st_pages import hide_pages # needed to hide pages
#%% 
hide_pages(st.session_state['pages_to_hide'])
text_input_container = st.empty() # showcase bar
st.session_state['API_key'] = st.text_input('Insert OpenAi API key (this will be not registered anywhere):') # asking for key

if st.session_state['API_key']!= "": # hide bar
    switch_page('ChatGPT')