import re
#used to scrap URLs
from lxml import etree
import sys
import html
import unicodedata

parser = etree.HTMLParser(encoding="utf-8")

def notEmptyOrBlankString (myString):
    if myString and not myString.isspace():
        # the string is non-empty
        return True
    else:
        return False
    return False


def delete_special_character(string):
    '''
    Returns the string deleted special character

        Parameters:
                string (str): The string has many character (number, char, ...)

        Returns:
                string (str): The string after being deleted special character
    '''
    string = html.unescape(unicodedata.normalize("NFKD",string)).strip()
    string = string.replace("\n", "").replace("\r", "")
    string = string.replace('"', '')
    string = string.replace("'", "")
    string = string.replace("\\", "")
    return string

def get_value(html_file, field, list_xpath):
    result = ""
    tree = etree.parse(html_file, parser)
    for index in list_xpath:
        try:
            if tree.xpath(index): 
                
                if index.startswith('count'):
                    result = str(int(tree.xpath(index))) 
                else:
                    if field == 'DETAILED_BRIEF':
                        result = str(" ".join(i for i in tree.xpath(index)))
                    elif index.startswith('concat') or index.startswith('substring'):
                        result = str(tree.xpath(index))
                    else:
                        result = str(tree.xpath(index)[0])
                    
                if notEmptyOrBlankString(result):
                    return delete_special_character(result)
        except:
            pass     
    return result
                  
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
    for field in fields:
        try:
            row[field] = get_value(html_file,field,fields[field])
        except:
            pass
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
        if notEmptyOrBlankString(value):
            result += str(key) + '=' + '"' + value + '",'
    return result[0:len(result) - 1] 


