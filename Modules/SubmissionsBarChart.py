import sys
import os 
dir_path = os.path.dirname(os.path.realpath(__file__)) # directory containing this file
sys.path.append(dir_path)
import numpy as np
from ArticlesExtracter import ArticlesExtracter
#%%
def Bars(URLS = None):
    if URLS == None:
        URLS = ['https://arxiv.org/list/astro-ph/new', 
                'https://arxiv.org/list/cond-mat/new',
                'https://arxiv.org/list/gr-qc/new',
                'https://arxiv.org/list/hep-ex/new',
                'https://arxiv.org/list/hep-lat/new',
                'https://arxiv.org/list/hep-ph/new',
                'https://arxiv.org/list/hep-th/new',
                'https://arxiv.org/list/math-ph/new',
                'https://arxiv.org/list/nlin/new',
                'https://arxiv.org/list/nucl-ex/new',
                'https://arxiv.org/list/nucl-th/new',
                'https://arxiv.org/list/physics/new',
                'https://arxiv.org/list/quant-ph/new'] # list of all urls whose bar plots will be shown
    
    n_links = len(URLS) # number of urls
    
    names = np.zeros(n_links, object) # storing the names of each subfield
    n_new_submissions = np.zeros(n_links) # number of new submissions for each url
    
    for i in range(n_links): 
        submissions = ArticlesExtracter(URLS[i])[0] # this returns a list containing [new_submissions, cross_list, replacements] however one of these may be missing depending on the URL
        new_submissions = submissions[0] # extracting all new submissions (neglecting the rest) WARNING: this assumes that there will always be new_submissions
        n_new_submissions[i] = len(new_submissions) # counting the number of new subnmissions
        
        idx_final = URLS[i].rfind('/') # finds the index of the LAST / in the url
        idx_start = URLS[i][:idx_final].rfind('/') # find the secont to last / in url
        names[i] = URLS[i][idx_start + 1: idx_final] # adds names of bars (they are all list/NAME/new)
    
    y_pos = np.arange(n_links)

    return y_pos, n_new_submissions, names