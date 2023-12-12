import requests
from bs4 import BeautifulSoup
#%% 
def ArticlesExtracter(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser") # Beautiful soup reorganizes the content contained in "page"
    
    ##### From here we search thorugh the html page #####
    dlpage = soup.find(id="dlpage") # obtaining the dlpage
    section_names = dlpage.findAll('h3') # finding the names of all sections contained in the URL (i.e. new_submissions, cross_list, replacements)
    n_sections = len(section_names) # new_submissions, cross_list, replacements (sometimes one or two of these are missing)
    title = dlpage.findAll("h1")[0] # find page title
    submissions = dlpage.findAll("dl") # find all submissions within dlpage (note: each <dl> correspond to either New Submissions, Cross list or Replacement)
    ##### Here we separate the submissions #####
    tmp_list = [0, 0, 0] # we need a list since we do not know how many sections will be presented in the current URL
    
    for i in range(n_sections):
        section_name = section_names[i].get_text() # the current section name
        if section_name.count('New submissions') == 1:
            tmp_list[0] = submissions[i]
            
        elif section_name.count('Cross-lists') == 1:
            tmp_list[1] = submissions[i]
            
        elif  section_name.count('Replacements') == 1:
            tmp_list[2] = submissions[i]
            
    return tmp_list, title