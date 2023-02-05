# this module is responsible for calculating 
# the correlation between a dataset's features

import io
import seaborn as sns
import matplotlib.pyplot as plt

from .utils import random_colormap

# global
FIG_WIDTH = 20
FIG_HEIGHT = 15


class Correlation:
    """
        calculate the correlation of the features
    """
    def __init__(self, df):
        self.df = df
    
    def perform_corr(self):
        corr_mat = self.df.corr()
        fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))
        
        heat = sns.heatmap(data=corr_mat, cmap=random_colormap(), ax=ax, annot=True)
        ax.set_title("correlation matrix")
        
        heat_fig = heat.get_figure()
        
        # no need to save a file
        buffer = io.BytesIO()
        heat_fig.savefig(buffer, format='png')
        buffer.seek(0)
        
        return buffer
        