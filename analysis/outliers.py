# this module is responsible to find out the outliers
# present in the dataset for every feature

import numpy as np
from scipy import stats


def z_score_out(df, col):
    """
        Counts the number of outliers for a specific
        column of a dataframe using Z-score.
    """
    zscores_df = df[np.abs(stats.zscore(df[col]) < 3)][col]
    num_outliers = df[col].shape[0] - zscores_df.shape[0]
    
    return num_outliers

def quant_out(df, col):
    pass

# -------------------------------------------------------

class Outliers:
    """
        all the dataset outliers for each column
        will be an instance of this
                
        params:
        
        df: dataframe under consideration
    """
    def __init__(self, df):
        self.out_str = ""
        self.zscore = []
        self.lowquan = []
        self.highquan = []
        
        self.df = df
        
    def perform_zscore_out(self):
        pass