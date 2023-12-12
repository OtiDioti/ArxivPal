import sys
sys.path.append('/home/francesco/Desktop/University/PyFiles/MyModules/')
sys.path.append('/home/francesco/Desktop/University/PyFiles/VariousPythonProjects/ForFun/StreamlitProjects/TestFolder/Modules')
import streamlit as st
from printer import PrintArticles
from ArticlesExtracter import ArticlesExtracter
from st_pages import hide_pages # needed to hide pages
#%% 
hide_pages(st.session_state['pages_to_hide'])
URL = st.session_state['research_field_url'] # recovering url of selected arxiv page to scrape
#%%
usr_input = st.text_input('Input keywords to scan for (separated by a space): ') # This will show up as a bar asking for an input´

txt_file = st.file_uploader(label ='or drop in a .txt file containing all keywords (separated by a space).' ,
                            type = 'txt', 
                            accept_multiple_files=False, 
                            label_visibility="visible")

if txt_file == None: # if no file was uploaded
    keywords = usr_input.lower().split()  # use only user input
else: 
    tmp = txt_file.read().lower().strip().split() # cleaning textfile
    file_words = [w.decode("utf-8") for w in tmp] # obtaining list where byte indicator is removed
    keywords = file_words + usr_input.lower().split() # use user input and file uploaded
#%%
submission_list, title = ArticlesExtracter(URL)

for i in range(2): # we do not care about Replacements, since they do not posses an abstract (thus we iterate as 0, 1 and not 0, 1, 2)
    if submission_list[i] != 0:
        PrintArticles(submission_list[i], keywords)
