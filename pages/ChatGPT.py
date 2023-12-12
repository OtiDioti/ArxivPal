from openai import OpenAI
import streamlit as st
import os 
import sys
dir_path = os.path.dirname(os.path.realpath(__file__)) # current directory
prev_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) # parent of current directory
sys.path.append(prev_dir+'/Modules')
from PDFTextExtracter import KnowledgeExtracter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.prompts import PromptTemplate
from st_pages import hide_pages # needed to hide pages
#%% 
hide_pages(st.session_state['pages_to_hide'])
_='''Here we extract the text of the selected paper and divide it into separate chuncks with
some overlap between them. The chunks will be then stored as high dimensional vectors.
By doing this, we can then similarly vectorize the user's questions and consider the overlap
of the user vector_question with the set of vectors we have in the chunks. Thus 
this allows us to selectively pick what parts of the document should chatgpt read 
to answer a specific question, avoiding the problem of feeding too much information to it.'''
#### Extracting the paper & other info #####
paper_title = st.session_state['current_title'] # obtaining the title of the interesting paper into session state (session state will give us this info by moving to this page via the click of the "Ask GPT button)
paper_abstract = st.session_state['current_abstract'] # obtaining the abstract of the interesting paper into session state (session state will give us this info by moving to this page via the click of the "Ask GPT button)
URL = st.session_state['current_link'] # obtaining the link of the interesting paper into session state (session state will give us this info by moving to this page via the click of the "Ask GPT button)
paper = KnowledgeExtracter(URL) # here we use the URL to obtain the the string of text contained in the pdf we are interested in

#### splitting text into chunks with some overlap between them ####
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 3000, chunk_overlap = 500, add_start_index=True) # we’ll split our documents into chunks of 1000 characters with 200 characters of overlap between chunks
all_splits = text_splitter.split_text(paper) # this is now a list of stings with the specifized chunk_size 

#### storing chuncks into high dimensional vectors ####
_='''Now that we’ve got len(all_splits) text chunks in memory, we need to store and 
index them so that we can search them later in our RAG (Retrieval Augmented Generation) app. 
The most common way to do this is to embed the contents of each document split and upload
those embeddings to a vector store.

Then, when we want to search over our splits, we take the search query, embed it 
as well, and perform some sort of “similarity” search to identify the stored splits 
with the most similar embeddings to our query embedding. The simplest similarity measure 
is cosine similarity — we measure the cosine of the angle between each pair of embeddings 
(which are just very high dimensional vectors).

We can embed and store all of our document splits in a single command using the Chroma vector 
store and OpenAIEmbeddings model.'''


st.session_state["openai_model"] = 'gpt-4' #"gpt-3.5-turbo" # create it and set it to gpt-3.5-turbo
os.environ["OPENAI_API_KEY"] = st.session_state['API_key'] # set key


vectorstore = Chroma.from_texts(texts = all_splits, embedding = OpenAIEmbeddings()) # storing the chuncks as high dimensional vectors

####  Now, given a query (i.e. question) we should be able to find the snippets containing relevant information ####
_='''Now let’s write the actual application logic. We want to create a simple application 
that let’s the user ask a question, searches for documents relevant to that question, 
passes the retrieved documents and initial question to a model, and finally returns an answer.

LangChain defines a Retriever interface which wraps an index that can return relevant 
documents given a string query. All retrievers implement a common method get_relevant_documents() 
(and its asynchronous variant aget_relevant_documents()).

The most common type of Retriever is the VectorStoreRetriever, which uses the similarity 
search capabilities of a vector store to facillitate retrieval. Any VectorStore can easily
be turned into a Retriever.

Note that this process could be made better by using the MultiQueryRetriever method
which generates variants of the input question and uses those to better narrow down
the relevant chunks within a piece of text.'''


def ChunksRetriever_single_question(question, nr_of_chunks = 6):
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": nr_of_chunks})
    retrieved_chunks = retriever.get_relevant_documents(question)
    return retrieved_chunks

def ChunksRetriever_multi_query(question, vector_database, half_number_of_chunks = 3, number_of_variation_question = 5):
    ''' This function takes in a question and asks a llm to generate 3 (this 
    number is set by default and can be changed by changing the PROMPTTEMPLATE in
    MultiQueryRetriever) variations of the question. These quesries are then made into 
    vectors which are then projected onto the paper chunks to find the best suitable chunks 
    in terms of information to answer the original question.'''
    
    multi_query_prompt = PromptTemplate(
    input_variables=["question"],
    template='''You are an AI language model assistant. Your task is 
    to generate '''+str(number_of_variation_question)+''' different versions of the given user question to retrieve relevant 
    documents from a vector  database. By generating multiple perspectives on the user question, your goal is to 
    help the user overcome some of the limitations of distance-based similarity search. 
    Provide these alternative questions separated by newlines. Original question: ''' + question,
    )
    llm = ChatOpenAI(model_name = st.session_state["openai_model"], temperature=0) # defining which llm will provide the question variations
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever = vector_database.as_retriever(search_type="similarity", search_kwargs={"k": half_number_of_chunks}),
        llm=llm,
        prompt = multi_query_prompt
    )
    retrieved_chunks = retriever_from_llm.get_relevant_documents(query = question)
    return retrieved_chunks
#%% Setting up the initial state of the language model
sys_prompt = """You will now receive the abstract to a scientific paper. Furthermore, 
you will also receive snippets of the paper containing useful information to answer future questions. 
Try to produce formal answers, and abstain from using equations when possible. If the text does not contain the
required information to answer future questions you can try to be flexible and answer it anyways, however, 
it is imperative you make this clear in the message. Whenever the information is instead contained in the paper,
try to reference the pieces of text containing the answer when replying."""

gpt_answer = """Ok. I will mostly base my future answers on the content provided in 
the paper and I will try to be as formal as possible. Also, I will make it clear whenever an
answer I am providing does not stem from the content of the information received; on the other hand, 
I will try to reference the provided pieces of text if these do contain the requested information."""

sys_nudge = """To answer the following question use the previously provided information together 
with these new chunks of information: """ # this will be used to tell gpt where to look for answers

client = OpenAI(api_key = st.session_state['API_key'])

st.session_state.messages = [
    {'role':'system', 'content':sys_prompt},
    {'role':'assistant', 'content':gpt_answer},
    {'role':'system', 'content':'The paper in question is called '+paper_title+' and its abstract reads: '+paper_abstract}
]  # THIS SHOULD UPDATE EVERY TIME YOU ENTER THIS PAGE

#%%
half_number_of_chunks = 4 # this is roughly half the number of chunks of text that gpt will search through

st.title("Ask GPT (beta)") # adds title to page


for message in st.session_state.messages[3:]: # iterating through the messages avoiding the set up
    with st.chat_message(message["role"]): # st.chat_message(user = 'role') this will show who is writing
        st.markdown(message["content"]) # this will show the content of the message

if prompt := st.chat_input("What can I help you with?"): # within the chat bar
    relevant_info = ChunksRetriever_multi_query(question = prompt, 
                                                half_number_of_chunks = half_number_of_chunks,
                                                vector_database = vectorstore) # retrieving the chunks relevant to answer the question
    complete_info = '' # initializing a string
    nr_of_chunks = len(relevant_info) # number of relevant chunks found
    for i in range(nr_of_chunks): # iterating over all obtained chunks
        complete_info += 'Chunk['+str(i)+'] ' + str(relevant_info[i]).replace('page_content=','') # chaining the useful chunks
    st.session_state.messages.append({"role": "system", "content": sys_nudge + complete_info}) # appending prompt of system telling gpt to use the following information
    st.session_state.messages.append({"role": "user", "content": prompt}) # appending prompt of user to message history
    with st.chat_message("user"): # will show that the prompt has been composed by user
        st.markdown(prompt) #  will show the prompt input by the user
    
    with st.chat_message("assistant"): # showing that it is the assistant speaking
        message_placeholder = st.empty() 
        full_response = "" # initializing response string
        response = client.chat.completions.create(
                   model = st.session_state["openai_model"],
                   messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                   )
        full_response += response.choices[0].message.content
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    if len(st.session_state.messages) >= 9: # the chatbot will remember only the previous question (and corresponding answer)
        st.session_state.messages.pop(3) # removing the first chuncks of text
        st.session_state.messages.pop(3) # removing the first question
        st.session_state.messages.pop(3) # removing the first answer

    
    
    