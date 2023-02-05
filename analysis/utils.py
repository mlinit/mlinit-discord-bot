import pandas as pd
import requests
import random
import io
import math

from urllib.parse import urlparse


def random_colormap():
    colors = [
        'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 
        'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 
        'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 
        'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 
        'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 
        'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 
        'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r',
        'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 
        'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 
        'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 
        'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 
        'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 
        'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 
        'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 
        'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 
        'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 
        'cubehelix_r', 'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 
        'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 
        'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 
        'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 
        'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r',
        'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'icefire', 
        'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 
        'magma_r', 'mako', 'mako_r', 'nipy_spectral', 'nipy_spectral_r', 
        'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism',
        'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic', 
        'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 
        'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 
        'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight',
        'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 
        'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r'
    ]
    
    rand_cmap = random.choice(colors)
    return rand_cmap


def split_into_parts(msg: str, chars: int):
    """
        Split a string into equal parts,
        each part having {chars} characters
    """
    msgs = []
    if len(msg) > 2000:
        bins = math.ceil(len(msg) / chars)
        for i in range(bins-1):
            msgs.append(msg[chars*i: chars*(i+1)])
        msgs.append(msg[2000*(bins-1): ])

    return msgs


def request_headers() -> dict:
    """
        Random user agents
    """
        
    usr_agent_str: list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    ]
    # select random
    rand_usr_agent_str: str = random.choice(usr_agent_str)
    headers: dict = {"User-Agent": rand_usr_agent_str}
    return headers


def check_url_valid(url: str) -> bool:
    """
        Checks if a given url is valid
        (discord cdn, csv file)
    """
    
    cdn = "cdn.discordapp.com"
    parse_res = urlparse(url)
    
    if parse_res.netloc == cdn and parse_res.path.endswith(".csv"):
        return True
    
    return False
    

def read_dataset_from_url(url: str):
    """
        For reading a CSV file from discord cdn 
        to a pandas dataframe
    """
    error_msg = "oops 😔\n\ni was not able to read any data from the URL.\nmaybe it's not valid?"
    
    if check_url_valid(url):
        try:
            header = request_headers()
            header["X-Requested-With"] = "XMLHttpRequest"
            
            response = requests.get(url, headers=header)
            
            # for unsuccesful response
            if response.status_code != 200:
                raise
            
            # in-memory file
            content = io.StringIO(response.text)
            df = pd.read_csv(content, sep=",")
            
            return df
        except Exception as e:
            return error_msg
    else:
        return error_msg
