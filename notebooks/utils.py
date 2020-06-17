import os
import pandas as pd


def load_ingr_comps():
    file_dir = os.path.dirname(os.path.abspath(""))
    data_dir = os.path.join(file_dir, 'data/')
    comp_info = pd.read_csv(data_dir + 'comp_info.tsv', sep='\t', header=0, index_col=0)
    ingr_info = pd.read_csv(data_dir + 'ingr_info.tsv', sep='\t', header=0, index_col=0)
    ingr_comp = pd.read_csv(data_dir + 'ingr_comp.tsv', sep='\t', header=0)
    return comp_info, ingr_info, ingr_comp