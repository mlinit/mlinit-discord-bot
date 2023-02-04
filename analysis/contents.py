# module for getting the contents of different commands

def get_general_help() -> str:
    helpstr = f"""
here is the list of commands available in me...
        

• **info**
use this command for getting the _information_ such as **null values** and **data type** of each column in the dataset.

for more, type:
```<bot-prefix>help info```

• **des**
use this command to get the statistical measures like **mean**, **standard deviation**, **minimum**, and more for each column in the dataset

for more, type:
```<bot-prefix>help des```

• **dup**
use this command to get the count of duplicate rows (if any) residing in the dataset

for more, type:
```<bot-prefix>help dup```

• **out**
use this command to find the number of outliers in each column of the dataset using well known methods like **z-score** test and **quantile range** test

for more, type:
```<bot-prefix>help out```
        
    """
    
    return helpstr


def get_info_help() -> str:
    helpstr = f"""

        usage:
        
        ```<bot_prefix>info <dataset_url> <user>```
        
        a concise summary of a dataset.
        
        required parameters:
        • **dataset_url**: the discord CDN URL of an uploaded CSV file
        • **user**: the user to send the analysis to
        
        use this command for getting the _information_ of each column in the dataset.
        
        this command prints the information about a dataset including the **data-type**, **columns**, **null values** and **memory usage**.
    """
    
    return helpstr

def get_des_help() -> str:
    helpstr = f"""
    
        usage:
        
        ```<bot_prefix>des <dataset_url> <user>```
        
        generate descriptive statistics.
        
        required parameters:
        • **dataset_url**: the discord CDN URL of an uploaded CSV file
        • **user**: the user to send the analysis to
        
        use this command to get the statistical measures like **mean**, **standard deviation**, **minimum**, and more for each column in the dataset.
        
        descriptive statistics include those that summarize the **central tendency**, **dispersion** and **shape** of a dataset’s distribution, excluding NaN values.
    """
    
    return helpstr

def get_dup_help() -> str:
    helpstr = f"""
    
        usage:
        
        ```<bot_prefix>dup <dataset_url> <user>```
        
        find the number of duplicate rows in a dataset
        
        required parameters:
        • **dataset_url**: the discord CDN URL of an uploaded CSV file
        • **user**: the user to send the analysis to 

    """
    
    return helpstr

def get_out_help() -> str:
    helpstr = f"""
    
        usage:
        
        ```<bot_prefix>out <dataset_url> <user>```
        
        find the number of outliers (if any) present in each column of a dataset 
        
        required parameters:
        • **dataset_url**: the discord CDN URL of an uploaded CSV file
        • **user**: the user to send the analysis to 
        
        this command uses well known methods like **z-score** and **quantile ranges** test to find the outliers.
        
        lower (25%) and upper outliers (75%) are calculated using interquantile ranges.
    """
    
    return helpstr