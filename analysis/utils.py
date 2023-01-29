import numpy as np
import pandas as pd
import requests
import random
import io
import math

from numpy import array, max, vectorize
from urllib.parse import urlparse

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

def makeTable(headerRow, columnizedData, columnSpacing=2) -> str:
    """Creates a technical paper style, left justified table

    Author: Christopher Collett
    Date: 6/1/2019"""
    
    table = ""

    cols = array(columnizedData,dtype=str)
    colSizes = [max(vectorize(len)(col)) for col in cols]

    header = ''
    rows = ['' for i in cols[0]]

    for i in range(0,len(headerRow)):
        if len(headerRow[i]) > colSizes[i]: colSizes[i]=len(headerRow[i])
        headerRow[i]+=' '*(colSizes[i]-len(headerRow[i]))
        header+=headerRow[i]
        if not i == len(headerRow)-1: header+=' '*columnSpacing

        for j in range(0,len(cols[i])):
            if len(cols[i][j]) < colSizes[i]:
                cols[i][j]+=' '*(colSizes[i]-len(cols[i][j])+columnSpacing)
            rows[j]+=cols[i][j]
            if not i == len(headerRow)-1: rows[j]+=' '*columnSpacing

    line = '-'*len(header)
    
    table += line + '\n' + header + '\n' + line + '\n'
    for row in rows:
        table += row + '\n'    
    table += line
    
    return table