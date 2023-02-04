# this module is responsible to find out the outliers
# present in the dataset for every feature

import numpy as np
from scipy import stats


def z_score_out(df, col):
    zscores_col = df[np.abs(stats.zscore(df[col], nan_policy="omit") < 3)][col]
    num_outliers = df[col].shape[0] - zscores_col.shape[0]
    
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
        """
        Counts the number of outliers for a specific
        column of a dataframe using Z-score.
        """
        num_features = [self.df.select_dtypes(include=["number"]).count()][0].index
        num_features = list(num_features)
        feats_len = len(num_features)
        
        zouts = np.zeros(shape=feats_len, dtype=np.int64)
        
        for i, col in enumerate(num_features):
            zouts[i] = z_score_out(self.df, col)
            
        return (num_features, zouts)
    
    def perform_quantile_out(self):
        """
            Counts the number of outliers for a specific
            column of a dataframe using quantile method.
        """
        num_features = [self.df.select_dtypes(include=["number"]).count()][0].index
        num_features = list(num_features)
        feats_len = len(num_features)
        
        upper_outliers = np.zeros(shape=feats_len, dtype=np.int64)
        lower_outliers = np.zeros(shape=feats_len, dtype=np.int64)
        
        for i, feat in enumerate(num_features):
            q1 = self.df[feat].quantile(q=0.25)
            q3 = self.df[feat].quantile()
            # interquantile range
            iqr = q3 - q1
            
            lower_limit = q1 - (1.5 * iqr)
            upper_limit = q3 + (1.5 * iqr)
            
            a = self.df[self.df[feat] < lower_limit].shape[0]
            b = self.df[self.df[feat] > upper_limit].shape[0]
            
            lower_outliers[i] = a
            upper_outliers[i] = b
            
        return (num_features, lower_outliers, upper_outliers)
