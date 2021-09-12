import re
#used to scrap URLs
from lxml import etree
import sys
import html
import unicodedata

parser = etree.HTMLParser()

def delete_special_character(string):
    '''
    Returns the string deleted special character

        Parameters:
                string (str): The string has many character (number, char, ...)

        Returns:
                string (str): The string after being deleted special character
    '''
    string = html.unescape(unicodedata.normalize("NFKD",string))
    string = string.replace("\n", "").replace("\r", "")
    string = string.replace('"', '')
    string = string.replace("'", "")
    string = string.replace(";", "")
    return string

def extract(html_file, fields):
    '''
    Returns the fields of site
            Parameters:
                    html_file (string): File html contains ads's details
                    fields (dict): fields & xpath to collect real estate infos

            Returns:
                    data (dict): Dictionary of ads's details
    '''
    row = {}
    tree = etree.parse(html_file, parser)
    for field in fields:
        try:
            row[field] = " ".join([i.strip() for i in tree.xpath(fields[field]) if i.strip()])
        except Exception as e:
            # for just the message, or str(e), since print calls str under the hood
            print(e)
    for (key, value) in row.items():
        row[key] = delete_special_character(row[key])
    
    #print (html.unescape(tree.xpath("//div[@class='pd-desc-content']/descendant::text()")))
    return row
    

def sql_query(ads):
    '''
    Returns SQL command line to insert datas into database

        Parameters:
                ads (dict): The dictionary of ads's fields

        Returns:
                result[0:len(result) - 1]: The string of SQL command line
                Example:
                ID_CLIENT="BAN23653",SITE="dothinet",PRICE="9.9"
    '''
    
    result = ""
    for (key, value) in ads.items():
        if len(value)>0:
            result += str(key) + '=' + '"' + str(value) + '",'
    return result[0:len(result) - 1] 


