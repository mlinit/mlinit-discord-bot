# this module is responsible for describing
# the dataset in various ways.

from .utils import makeTable, read_dataset_from_url

class Describe:
    """
        all the dataset descriptions will be instance of this
        
        params:
        
        df: dataframe under consideration
    """
    def __init__(self, df):
        self.info_data = []
        self.info_str = ""
        self.summ_data = []
        self.summ_str = ""
        
        self.df = df
        
    def total_memory_usage(self) -> str:
        mem_use = self.df.memory_usage(deep=True).sum()
        mem_use_str = str(mem_use / 1000) + "MB"
        return mem_use_str
    
    def perform_info(self) -> str:
        features = list(self.df.columns)
        for i, _ in enumerate(features):
            features[i] = "**" + features[i] + "**"
        
        null = list(self.df.isnull().sum())
        dtypes = list(self.df.dtypes)
        
        for i in range(len(features)):
            self.info_str += '✅ ' + features[i] + '\n'
            self.info_str += '\t\t• ' + str(null[i]) + " null values\n"
            self.info_str += '\t\t• ' + str(dtypes[i]) + '\n'
        
        # info_table = makeTable(headers, [features, null, dtypes], columnSpacing=5)
        mem_use = self.total_memory_usage()
        self.info_str += '\n' + "memory usage: " + mem_use
        
        return self.info_str
        
        