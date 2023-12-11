import streamlit as st
import sys
import os 
dir_path = os.path.dirname(os.path.realpath(__file__)) # directory containing this file
sys.path.append(dir_path+'/Modules') 
from streamlit_extras.switch_page_button import switch_page # needed to switch page upon button click
from st_pages import hide_pages # needed to hide pages
from SubmissionsBarChart import Bars
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
#%%
st.set_page_config(page_title = 'Arxiv Scanner', 
                   layout = 'centered', 
                   page_icon = ':house:',
                   menu_items={
                   'Get Help': 'https://arxiv.org/list/cond-mat/new/',
                   'Report a bug': "https://arxiv.org/list/cond-mat/new/",
                   'About': "# This is a header. This is an *extremely* cool app!"},
                   initial_sidebar_state="collapsed")


st.title('Welcome to ArxivPal!')
st.write('## To start, open the sidebar on the left and select the field you would like to scan.')
st.write('''ArxivPal emerges to address the need of researchers to stay on top of the vast publication material published every day on the ArXiv.
         Developed with the discerning researcher in mind, ArxivPal seamlessly integrates two useful features that will hopefully help 
         the way you engage with newly released scholarly literature.\

### 1. Smart Paper Discovery\

Navigate the vast landscape of newly uploaded academic research effortlessly with ArxivPal's paper discovery feature. Stay ahead
 in your field by customizing your search based on specific research areas and keywords. ArxivPal employs a web scraping algorithm
 to scan abstracts and titles, delivering to you a curated selection of newly released papers from the arXiv repository. Whether
 you're delving into condensed matter physics, high energy physics, or any other niche within the vast expanse of phyiscs literature, ArxivPal 
 ensures you never miss a release. \

### 2. AskGPT Integration\

ArxivPal goes beyond traditional search functionalities with its integrated AskGPT feature. Engage in
conversations with ChatGPT about any paper that piques your interest. Unleash the power of dialogue to gain deeper insights, 
discuss methodologies, or simply brainstorm ideas. AskGPT opens up a new dimension in your research journey, providing a 
conversational bridge between you and the vast knowledge contained within arXiv. \

### Why ArxivPal?

**Precision in Discovery**: ArxivPal's tailored search narrows down the overwhelming sea
of information to provide you with papers that truly matter to your research.

**Effortless Engagement**: Seamlessly transition from paper discovery to insightful 
conversations with AskGPT. Discuss theories, seek clarifications, and explore the implications of groundbreaking research.

**Time Efficiency**: Save valuable time by letting ArxivPal handle the initial stages of 
literature review, allowing you to focus on the aspects of research that truly demand your expertise.

**Intuitive Interface**: ArxivPal boasts a user-friendly interface designed with researchers 
in mind. Navigate effortlessly through the app, ensuring a smooth and productive user experience.

Embark on a journey of intellectual exploration with ArxivPal – your indispensable companion 
in the pursuit of knowledge. Stay informed, engage in meaningful discussions, and elevate your research 
experience with this innovative app tailored for the curious minds shaping the future of physics.
         ''')
        
with st.sidebar:
    option = st.multiselect(
    'What field of reaserch are you interested in?',
    ['Condensed Matter', 'Astrophysics', 'H.E.P-Lattice', 
      "H.E.P.-Phenomenology","H.E.P.-Experiment", "H.E.P.-Theory",
      'Quantum Physics',  "General Physics","G.R. & Q. Cosmology", 
      'Mathematical Physics', 'Nonlinear Sciences', 'Nuclear Experiment',
      'Nuclear Theory'])

    if 'Condensed Matter' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/cond-mat/new'
        switch_page('page')
    elif 'Astrophysics' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/astro-ph/new'
        switch_page('page')    
    elif 'H.E.P-Lattice' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/hep-lat/new'
        switch_page('page')
    elif 'Quantum Physics' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/quant-ph/new'
        switch_page('page') 
    elif 'G.R. & Q. Cosmology' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/gr-qc/new'
        switch_page('page')
    elif 'H.E.P.-Phenomenology' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/hep-ph/new'
        switch_page('page') 
    elif 'General Physics' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/physics/new'
        switch_page('page')
    elif 'H.E.P.-Experiment' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/hep-ex/new'
        switch_page('page') 
    elif 'H.E.P.-Theory' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/hep-th/new'
        switch_page('page') 
    elif 'Mathematical Physics' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/math-ph/new'
        switch_page('page')
    elif 'Nonlinear Sciences' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/nlin/new'
        switch_page('page') 
    elif 'Nuclear Experiment' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/nucl-ex/new'
        switch_page('page') 
    elif 'Nuclear Theory' in option:
        st.session_state['research_field_url'] = 'https://arxiv.org/list/nucl-th/new'
        switch_page('page') 

st.session_state['pages_to_hide'] = ['ChatGPT', 'page'] # list of all the pages that won't show up in the sidebar
hide_pages(st.session_state['pages_to_hide'])

#%%
y_pos, n_new_submissions, names = Bars() # data required for bar plot
#### plot settings ####
fntsize = 23
fntweight = 'normal'
ticks_size_factor = 0.6
cbars = (1, 0.294, 0.294, 1)
bckgrnd_color = 'white'
bar_alpha = 1
rttn_xticks = 45
bckgrnd_color ='#0E1117'    
#### setting axis ####
plt.style.use('classic')
# fig, ax = plt.subplots()
ax = plt.axes()
fig = plt.figure(facecolor = bckgrnd_color)
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.set_ylabel('nr. of new submission', fontsize = fntsize, fontweight = fntweight)
ax.set_facecolor(bckgrnd_color)
# fig.patch.set_facecolor(bckgrnd_color)
#### plotting ####
plt.bar(y_pos, n_new_submissions, align='center', alpha = bar_alpha, color = cbars )
plt.xticks(y_pos, names)
plt.title(r'nr. of new submission for each field', fontsize = fntsize)
#### change all spines ####
for axis in ['top','bottom','left','right']:
    ax.spines[axis].set_linewidth(2)
#### increase tick width ####
ax.tick_params(width=2)
plt.yticks(fontsize = fntsize * ticks_size_factor)
plt.xticks(fontsize = fntsize * ticks_size_factor, rotation = rttn_xticks)

st.pyplot(fig, clear_figure=False, use_container_width=True)


    
