# this module is responsible for describing
# the dataset in various ways.

import numpy as np

class Describe:
    """
        all the dataset descriptions will be instance of this
        
        params:
        
        df: dataframe under consideration
    """
    def __init__(self, df):
        self.info_str = ""
        self.summ_str = ""
        
        self.df = df
        
    def total_memory_usage(self) -> str:
        mem_use = self.df.memory_usage(deep=True).sum()
        mem_use_str = str(mem_use / 1000) + " MB"
        return mem_use_str
    
    
    def perform_dupl(self):
        """
            Method to perform duplicate rows in a dataset
        """
        ndf = self.df[self.df.duplicated() == True]
        dup_rows = ndf.shape[0]
        dup_feats = list(ndf)

        return (dup_rows, dup_feats)
        
    
    def perform_summ(self):
        """
            Method to perform summary of dataset
        """
        ndf = self.df.describe(include="all")
        feats = list(ndf)
        rows = ndf.shape[0]
                
        count = [np.NaN for i in range(len(feats))]
        unique = [np.NaN for i in range(len(feats))]
        top = [np.NaN for i in range(len(feats))]
        freq = [np.NaN for i in range(len(feats))]
        mean = [np.NaN for i in range(len(feats))]
        std = [np.NaN for i in range(len(feats))]
        mini = [np.NaN for i in range(len(feats))]
        q25 = [np.NaN for i in range(len(feats))]
        q50 = [np.NaN for i in range(len(feats))]
        q75 = [np.NaN for i in range(len(feats))]
        maxi = [np.NaN for i in range(len(feats))]

        for i, _ in enumerate(feats):
            count[i] = list(ndf[feats[i]])[0]
            unique[i] = list(ndf[feats[i]])[1]
            top[i] = list(ndf[feats[i]])[2]
            freq[i] = list(ndf[feats[i]])[3]
            mean[i] = list(ndf[feats[i]])[4]
            std[i] = list(ndf[feats[i]])[5]
            mini[i] = list(ndf[feats[i]])[6]
            q25[i] = list(ndf[feats[i]])[7]
            q50[i] = list(ndf[feats[i]])[8]
            q75[i] = list(ndf[feats[i]])[9]
            maxi[i] = list(ndf[feats[i]])[10]
            feats[i] = "**" + feats[i] + "**"
                        
        # for i in range(len(feats)):
        #     self.summ_str += '✅ ' + feats[i] + '\n'
        #     self.summ_str += '\t\t• Count: ' + str(count[i]) + "\n"
        #     self.summ_str += '\t\t• Mean: ' + str(mean[i]) + '\n'
        #     self.summ_str += '\t\t• Standard Deviation: ' + str(std[i]) + '\n'
        #     self.summ_str += '\t\t• Minimum: ' + str(mini[i]) + '\n'
        #     self.summ_str += '\t\t• Quantile 1 (25%): ' + str(q25[i]) + '\n'
        #     self.summ_str += '\t\t• Quantile 2 (50%): ' + str(q50[i]) + '\n'
        #     self.summ_str += '\t\t• Quantile 3 (75%): ' + str(q75[i]) + '\n'
        #     self.summ_str += '\t\t• Maximum: ' + str(maxi[i]) + '\n'
        
        return (rows, feats, count, unique, top, freq, mean, std, mini, q25, q50, q75, maxi)
    
    def perform_info(self):
        """
            Information of the dataset
        """
        features = list(self.df.columns)
        rows = self.df.shape[0]
        for i, _ in enumerate(features):
            features[i] = "**" + features[i] + "**"
        
        null = list(self.df.isnull().sum())
        dtypes = list(self.df.dtypes)
        
        mem_use = self.total_memory_usage()
        return (rows, features, null, dtypes, mem_use)
        
        