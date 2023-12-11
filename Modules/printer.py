import streamlit as st
from streamlit_extras.switch_page_button import switch_page # needed to switch page upon button click
#%%

bad_chars = [';', ':', '!', "*", "\"","\'","$","{","}","/","\\"] # there could be more characters which make the strings not searchable

def PrintArticles(A, keywords):
    ''' 
    This function cleans up <dl><dl> objects and extracts
    titles, abstracts, authors and link of articles concerning 
    subjects indicated by the the keyword list (and prints them too).
    '''
    articles = A.findAll("dd") # Contains "natural language" information such as titles and abstracts
    dts = A.findAll("dt") # Contains hyperlinks for downloads and other info
    n = len(articles) # Number of articles 
    for i in range(n): # Looping over all extracted articles
        article = articles[i] # extracting article number "i"	
        dt = dts[i] # exctracting hyperlink pertaining current article
        title = article.findAll("div", {"class": "list-title mathjax"}) # Obtaining the the title of the current article
        authors = article.findAll("div", {"class": "list-authors"}) # Obtaining the authors 
        abstract = article.findAll("p", {"class": "mathjax"}) # Obtaining the article's abstract
        link = dt.findAll("a", {"title": "Abstract"})[0].get("href") # Obtaining the link with corresponding "title" Abstract
        pdf_link = dt.findAll("a", {"title": "Download PDF"})[0].get("href") # Obtaining the link with corresponding "title" Download PDF
		
        title_str = title[0].get_text().strip().replace("Title: ","") # Cleaning up title info
        author_str = authors[0].get_text().strip().replace("Authors:","").strip() # Cleaning up authors info
        abstract_str = abstract[0].get_text().strip() # Cleaning up abstract info
		
        for char in bad_chars: # looping over problematic character list
            abstract_str_tmp = abstract_str.replace(char,"") # replacing problematic characters in abstract with emptiness
            title_str_tmp = title_str.replace(char,"") # replacing problematic characters in title with emptiness
        abstract_lst = abstract_str_tmp.lower().split() # makes all string elements of abstract lower case and splits them into a list of "words"
        title_lst = title_str_tmp.lower().split() # makes all string elements of title lower case and splits them into a list of "words"

        found = False # initializing as if we did not find anything
        for x in keywords: # looping over the keywords we are looking for
            if (x in abstract_lst or x in title_lst): # if current keyword is found in either title list or abstract list
                key = x # save which element was found
                found = True # update found to True
                break # break for loop if an element was found
        if found: # if a keyword was found
            st.write('# '+title_str)
            st.write(abstract_str)
            st.write(author_str)
            st.write('keyword: '+key)
            st.write("https://arxiv.org/"+link)
            if st.button('Ask GPT', key = i): # if the button correpsponding to this paper is clicked
                st.session_state['current_title'] = title_str # saving the title of the interesting paper into session state
                st.session_state['current_abstract'] = abstract_str # saving the abstract of the interesting paper into session state
                st.session_state['current_link'] = "https://arxiv.org/" + pdf_link # saving the link of the interesting paper into session state
                switch_page("ChatGPT") # switching to GPT chat









