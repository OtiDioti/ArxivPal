import io
import requests
from pypdf import PdfReader
# import base64
#%%

def KnowledgeExtracter(URL): # URL must take you to open a pdf file
    '''This function takes in the url to some pdf file and spits out the text
    contained within it together with the list of images in the pdf (the images 
    are returned in base64 format. This function returns only the content of 
    the PDF, thus it removes title, authors, abstract and references (possibly 
    also appendix if this is located after the refereces).
    Note that equations will unfortunately not be accurately depicted.'''
    r = requests.get(URL) # obtaining url info
    f = io.BytesIO(r.content) # extracting information
    # Extract pdf
    reader = PdfReader(f) 
    n_pages = len(reader.pages)
    paper_text = ''
    
    # img_nr = 1 # setting counter for images
    # img_list = [] # creating empty list to be used to include images in base64 
    for i in range(n_pages): #iterating over all pages to extract text and images
        page = reader.pages[i] # current page
        paper_text += page.extract_text() # adding all pages together 
        
        
        # for image_file_object in page.images: # for all images in current page
        #     with open('Figure_' + str(img_nr) + image_file_object.name, "wb") as fp: # using this method
        #         fp.write(image_file_object.data) 
        #         img_nr += 1 
        #         img_list.append(base64.b64encode(image_file_object.data).decode('utf-8')) # converting image to baase64 and appending (conversion needed for chatgpt)
            
    
    # lowered_txt = paper_text.lower() # will be needed for finding words
    # introduction_idx = lowered_txt.find('introduction') # finds the point in the paper at which the word "introduction" appears for the first time (.lower() is needed to find references instead of Abstract or ABSTRACT)
    references_idx = paper_text.rfind('[1]') # finds the point in the paper at which "[1]" appears for the last time (this should in theory help finding the references section)
    paper_text = paper_text[:references_idx].replace('\n',' ') # removes all text before abstract (i.e. title and authors) and after references start, and removes all newline commands
    
    return paper_text#, img_list

