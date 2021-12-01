from config.config_ import *
from libs.or_utils_ import *

# SQL QUERY CHECK
def gen_statement(data_table,column,value,from_date,end_date):
    '''
        Generate sql from input 

            Parameters:
                data_table (str): dataframe table
                column (str): column
                value (str): value of column
                from_date (str): date begin. Ex: 20210401
                end_date (str): date end. Ex: 20210401

            Returns:
                sql_stm (str)): sql statement
    '''
    sql_stm = "SELECT * FROM " + data_table + " WHERE 1=1"
    if (from_date != ""):
        sql_stm = sql_stm.replace("1=1","")
        sql_stm = sql_stm + "`CREATED_DATE` >= '" + datetime.datetime.strptime(from_date,"%Y%m%d").strftime("%Y-%m-%d") + "' AND " 
    if (end_date != ""):
        sql_stm = sql_stm.replace("1=1","")
        sql_stm = sql_stm + "`CREATED_DATE` <= '" + datetime.datetime.strptime(end_date,"%Y%m%d").strftime("%Y-%m-%d") + "' AND "
    if (column != ""):
        sql_stm = sql_stm.replace("1=1","")
        if (value.lower() == "null"):
            sql_stm = sql_stm + "`" + column +"` IS NULL" + " AND "
        else:    
            sql_stm = sql_stm + "`" + column +"` LIKE " + "'%" + value + "%'" + " AND "
    sql_stm = re.sub(r'AND[ ]?$','',sql_stm)
    return sql_stm

def gen_statement_address(data_table,column,value,from_date,end_date):
    '''
        Generate sql address from input 

            Parameters:
                data_table (str): dataframe table
                column (str): column
                value (str): value of column
                from_date (str): date begin. Ex: 20210401
                end_date (str): date end. Ex: 20210401

            Returns:
                sql_stm (str)): sql statement
    '''
    sql_stm = "SELECT SPLIT_CITY,SPLIT_DISTRICT,SPLIT_WARD,FORMAT_STREET FROM " + data_table + " WHERE SPLIT_CITY IS NOT NULL AND SPLIT_DISTRICT IS NOT NULL AND SPLIT_WARD IS NOT NULL AND FORMAT_STREET IS NOT NULL"
    # if (from_date != ""):
    #     sql_stm = sql_stm.replace("1=1","")
    #     sql_stm = sql_stm + "`CREATED_DATE` >= '" + datetime.datetime.strptime(from_date,"%Y%m%d").strftime("%Y-%m-%d") + "' AND " 
    # if (end_date != ""):
    #     sql_stm = sql_stm.replace("1=1","")
    #     sql_stm = sql_stm + "`CREATED_DATE` <= '" + datetime.datetime.strptime(end_date,"%Y%m%d").strftime("%Y-%m-%d") + "' AND "
    # if (column != ""):
    #     sql_stm = sql_stm.replace("1=1","")
    #     if (value.lower() == "null"):
    #         sql_stm = sql_stm + "`" + column +"` IS NULL" + " AND "
    #     else:    
    #         sql_stm = sql_stm + "`" + column +"` LIKE " + "'%" + value + "%'" + " AND "
    # sql_stm = re.sub(r'AND[ ]?$','',sql_stm)
    return sql_stm


# GET LAT_OS, LON_OS
def convert_latlon(full_address):
    """
        Get Lattitude, longitude from openstreetmap api
        @param: str - Full address
        @return: double - longitude,lattitude or if error use api global
    """
    respData =""
    parameters = {"q":full_address, "format":"json"}
    try:        
        parameters = urllib.parse.urlencode(parameters)
        requests = API_URL_LOCAL + "?" + parameters
        resp = urllib.request.urlopen(requests)
        respData = resp.read()
        latlon =  json.loads(respData.decode('utf-8'))
        if len(latlon)>0:
            if ("lon" in latlon[0]) and ("lat" in latlon[0]):
                #print (latlon[0]["lon"],latlon[0]["lat"])
                return latlon[0]["lon"],latlon[0]["lat"]
    except:
        #print("An exception occurred !")
        return convert_latlon_global(full_address)
    
    return None,None

def convert_latlon_global(full_address):
    """
        Get Lattitude, longitude from openstreetmap api global
        @param: str - Full address
        @return: double - longitude,lattitude
    """
    respData =""
    parameters = {"q":full_address, "format":"json"}
    try:        
        parameters = urllib.parse.urlencode(parameters)
        requests = API_URL + "?" + parameters
        resp = urllib.request.urlopen(requests)
        respData = resp.read()
        latlon =  json.loads(respData.decode('utf-8'))
        if len(latlon)>0:
            if ("lon" in latlon[0]) and ("lat" in latlon[0]):
                #print (latlon[0]["lon"],latlon[0]["lat"])
                return latlon[0]["lon"],latlon[0]["lat"]
    except ValueError as vx:
        print(vx)
        raise
    except Exception as ex:   
        print(ex)
        raise

    return None,None

# GET PRICE FROM TEXT
def remove_char(text):
    '''
        Remove dot in text like t.oi di h.o.c => toi di hoc

            Parameters:
                    text (str): A text need to be removed dot

            Returns:
                    sentence (str): A text removed dot
    '''
    text = text.lower()
    text = unidecode(text)
    b = text.split(' ')
    sentence = ''
    for w in b:
        if (re.findall('[a-z]\.[a-z]',w)):
            w = re.sub('\.','',w)
        if ('.' in w):
            w = remove_delimiter(w)
        if (w):
            sentence = sentence + ' ' + w
    sentence = re.sub('m[ ]?2','m2',sentence)
    sentence = re.sub('/th ','/thang',sentence)
    sentence = re.sub('/thg','/thang',sentence)
    return sentence

def get_price_from_text(text,surface_in_m2):
    '''
        Get price from text

            Parameters:
                text (str): A text need to be get price
                surface_in_m2 (float): surface has been converted in m2

            Returns:
                price (float): Price in trieu found from text. If price hasn't found, return price is 0
    '''
    if text is not None: #convention naming pep8
        org_text = text
        text = text.lower()
        text = unidecode(text)
        text = remove_char(text)
        ls_remove = [":","thuong luong","nhanh","tong",\
                     "nhinh","chao","chi","truc tiep","voi","chu nha",\
                     "hien","dang","phong","dau tu","tuy","vi tri","tu","la","con","it",
                     "vat lieu tri gia"]
        for e in ls_remove:
            text = text.replace(e, " ")
        text = text.replace('ty dong','ty').replace('ngan dong','ngan').replace('nghin dong','nghin').replace('trieu dong','trieu').replace('tr dong','trieu')
        text = text.replace('ty ruoi','ty 5 ').replace('ngan ruoi','ngan 5 ').replace('nghin ruoi','nghin 5 ').replace('trieu ruoi','trieu 5 ').replace('tr ruoi','trieu 5 ')
        text = re.sub(r'[ ]?/[ ]?m[ .,]',' /m2 ',text)
        text = ' '.join(text.split())
        
        pattern_of_combine_price_unit = [
                            # 3 ty 500 trieu / m2, 3 ti 500 trieu / m2
                            r'\d+[ ]?ty[ ]?\d+[ ]?trieu[ ]?/[ ]?m2',r'\d+[ ]?ti[ ]?trieu[ ]?/[ ]?m2',
                            r'\d+[ ]?ty[ ]?\d+[ ]?tr[ ]?/[ ]?m2',r'\d+[ ]?ti[ ]?tr[ ]?/[ ]?m2',
                            # 3 ty 500 trieu / hecta, 3 ti 500 trieu / hecta
                            r'\d+[ ]?ty[ ]?\d+[ ]?trieu[ ]?/[ ]?ha[ .,]',r'\d+[ ]?ti[ ]?trieu[ ]?/[ ]?ha[ .,]',
                            r'\d+[ ]?ty[ ]?\d+[ ]?tr[ ]?/[ ]?ha[ .,]',r'\d+[ ]?ti[ ]?tr[ ]?/[ ]?ha[ .,]',
                            r'\d+[ ]?ty[ ]?\d+[ ]?trieu[ ]?/[ ]?hec[ ]?ta',r'\d+[ ]?ti[ ]?trieu[ ]?/[ ]?hec[ ]?ta',
                            r'\d+[ ]?ty[ ]?\d+[ ]?tr[ ]?/[ ]?hec[ ]?ta',r'\d+[ ]?ti[ ]?tr[ ]?/[ ]?hec[ ]?ta',
                            # 3 ty 5 / m2, 3 ti 5 / m2
                            r'\d+[ ]?ty[ ]?\d+[ ]?/[ ]?m2',r'\d+[ ]?ti[ ]?\d+[ ]?/[ ]?m2',
                            # 3 ty 5 / hecta, 3 ti 5 / hecta
                            r'\d+[ ]?ty[ ]?\d+[ ]?/[ ]?hec[ ]?ta',r'\d+[ ]?ti[ ]?\d+[ ]?/[ ]?hec[ ]?ta',
                            r'\d+[ ]?ty[ ]?\d+[ ]?/[ ]?ha[ .,]',r'\d+[ ]?ti[ ]?\d+[ ]?/[ ]?ha[ .,]',
                            # 3 trieu 5 / m2
                            r'\d+[ ]?trieu\d+[ ]?/[ ]?m2',r'\d+[ ]?tr\d+[ ]?/[ ]?m2',
        ]
        
        pattern_of_price_unit = [
                            # 3.5 ty / ha
                            r'\d*[.,]?\d+[ ]?ty[ ]?/[ ]?ha[ .,]',r'\d*[.,]?\d+[ ]?ti[ ]?/[ ]?ha[ .,]',
                            r'\d*[.,]?\d+[ ]?ty[ ]?/[ ]?hec[ ]?ta',r'\d*[.,]?\d+[ ]?ti[ ]?/[ ]?hec[ ]?ta',
                            # 3.5 ty / m2
                            r'\d*[.,]?\d+[ ]?ty[ ]?/[ ]?m2', r'\d*[.,]?\d+[ ]?ti[ ]?/[ ]?m2',
                            # 3.5 trieu / ha
                            r'\d*[.,]?\d+[ ]?trieu[ ]?/[ ]?ha[ .,]',r'\d*[.,]?\d+[ ]?tr[ ]?/[ ]?ha[ .,]',
                            r'\d*[.,]?\d+[ ]?trieu[ ]?/[ ]?hec[ ]?ta',r'\d*[.,]?\d+[ ]?tr[ ]?/[ ]?hec[ ]?ta',
                            # 3.5 trieu / m2
                            r'\d*[.,]?\d+[ ]?trieu[ ]?/[ ]?m2', r'\d*[.,]?\d+[ ]?tr[ ]?/[ ]?m2',
                            # 3.5 ngan / m2
                            r'\d*[.,]?\d+[ ]?nghin[ ]?/[ ]?m2', r'\d*[.,]?\d+[ ]?ngan[ ]?/[ ]?m2', r'\d*[.,]?\d+[ ]?ng[ ]?/[ ]?m2',
                            # 3.5 / m2
                            r'\d*[.,]?\d+[ ]?/[ ]?m2',
                            # 3.5 / hecta
                            r'\d*[.,]?\d+[ ]?/ha[ .,]',r'\d*[.,]?\d+[ ]?/hec[ ]?ta',
        ]
        
        pattern_of_combine_price = [
                            # 3 ty 500 trieu, 3 ti 500 trieu
                            r'\d+[ ]?ty[ ]?\d+[ ]?trieu',r'\d+[ ]?ti[ ]?trieu',
                            r'\d+[ ]?ty[ ]?\d+[ ]?tr[ .,]',r'\d+[ ]?ti[ ]?tr[ .,]',
                            # 3 ty 5, 3 ti 5
                            r'\d+[ ]?ty[ ]?\d+[ ]?\w*',r'\d+[ ]?ti[ ]?\d+[ ]?\w*',
                            # 3 trieu 5, 3 tr 5
                            r'\d+[ ]?trieu[ ]?\d+[ ]?\w*',r'\d+[ ]?tr[ ]?\d+[ ]?\w*',
        ]
        
        pattern_of_price_time = [
                            # 3.5 ngan, 3.5 nghin / thang
                            r'gia d*[.,]?\d+[ ]?ngan[ ]?/[ ]?thang', r'gia \d*[.,]?\d+[ ]?nghin[ ]?/[ ]?thang',r'gia \d*[.,]?\d+[ ]?ng[ ]?/[ ]?thang', 
                            # 3.5 dong / thang, 3.5 d/thang
                            r'gia \d*[.,]?\d+[ ]?dong[ ]?/[ ]?thang',r'gia \d*[.,]?\d+[ ]?d[ ]?/[ ]?thang',
                            # 3.5 ty, 3.5 ti / thang
                            r'gia \d*[.,]?\d+[ ]?ty[ ]?/[ ]?thang',r'gia \d*[.,]?\d+[ ]?ti[ ]?/[ ]?thang',
                            # 3.5 trieu, 3.5 tr / thang
                            r'gia \d*[.,]?\d+[ ]?trieu[ ]?/[ ]?thang',r'gia \d*[.,]?\d+[ ]?tr[ ]?/[ ]?thang',
                            # 3.5 trieu, 3.5 tr / thang
                            r'gia \d*[.,]?\d+[ ]?dong[ ]?/[ ]?thang',r'gia \d*[.,]?\d+[ ]?d[ ]?/[ ]?thang',

                            # 3.5 ngan, 3.5 nghin / thang
                            r'thue d*[.,]?\d+[ ]?ngan[ ]?/[ ]?thang', r'thue \d*[.,]?\d+[ ]?nghin[ ]?/[ ]?thang', r'thue \d*[.,]?\d+[ ]?ng[ ]?/[ ]?thang', 
                            # 3.5 dong / thang, 3.5 d/thang
                            r'thue \d*[.,]?\d+[ ]?dong[ ]?/[ ]?thang',r'thue \d*[.,]?\d+[ ]?d[ ]?/[ ]?thang',
                            # 3.5 ty, 3.5 ti / thang
                            r'thue \d*[.,]?\d+[ ]?ty[ ]?/[ ]?thang',r'thue \d*[.,]?\d+[ ]?ti[ ]?/[ ]?thang',
                            # 3.5 trieu, 3.5 tr / thang
                            r'thue \d*[.,]?\d+[ ]?trieu[ ]?/[ ]?thang',r'thue \d*[.,]?\d+[ ]?tr[ ]?/[ ]?thang',
                            # 3.5 trieu, 3.5 tr / thang
                            r'thue \d*[.,]?\d+[ ]?dong[ ]?/[ ]?thang',r'thue \d*[.,]?\d+[ ]?d[ ]?/[ ]?thang',
                           ]
        
        pattern_of_price = [
                            # 3.5 ngan, 3.5 nghin 
                            r'ban \d*[.,]?\d+[ ]?ngan[ ]?[.,/]?[ ]?m[ ]?2', r'ban \d*[.,]?\d+[ ]?nghin[ ][.,/]?[ ]?m[ ]?2',r'ban \d*[.,]?\d+[ ]?ng[ ][.,/]?[ ]?m[ ]?2', 
                            # 3.5 dong,
                            r'ban \d*[.,]?\d+[ ]?dong[ ]?[.,/]?[ ]?m[ ]?2', r'ban \d*[.,]?\d+[ ]?d[ ][.,/]?[ ]?m[ ]?2',
                            # 3.5 ty, 3.5 ti
                            r'ban \d*[.,]?\d+[ ]?ty[ ]?[.,/]?[ ]?m[ ]?2',r'ban \d*[.,]?\d+[ ]?ti[ ][.,/]?[ ]?m[ ]?2',
                            # 3.5 trieu, 3.5 tr
                            r'ban \d*[.,]?\d+[ ]?trieu[ ]?[.,/]?[ ]?m[ ]?2',r'ban \d*[.,]?\d+[ ]?tr[ ][.,/]?[ ]?m[ ]?2',

                            # 3.5 ngan, 3.5 nghin 
                            r'gia \d*[.,]?\d+[ ]?ngan[ ]?[.,/]?[ ]?m[ ]?2', r'gia \d*[.,]?\d+[ ]?nghin[ ][.,/]?[ ]?m[ ]?2',r'gia \d*[.,]?\d+[ ]?ng[ ][.,/]?[ ]?m[ ]?2' 
                            # 3.5 dong,
                            r'gia \d*[.,]?\d+[ ]?dong[ ]?[.,/]?[ ]?m[ ]?2', r'gia \d*[.,]?\d+[ ]?d[ ][.,/]?[ ]?m[ ]?2',
                            # 3.5 ty, 3.5 ti
                            r'gia \d*[.,]?\d+[ ]?ty[ ]?[.,/]?[ ]?m[ ]?2',r'gia \d*[.,]?\d+[ ]?ti[ ][.,/]?[ ]?m[ ]?2',
                            # 3.5 trieu, 3.5 tr
                            r'gia \d*[.,]?\d+[ ]?trieu[ ]?[.,/]?[ ]?m[ ]?2',r'gia \d*[.,]?\d+[ ]?tr[ ][.,/]?[ ]?m[ ]?2',
            
                            # 3.5 ngan, 3.5 nghin 
                            r'ban \d*[.,]?\d+[ ]?ngan[ ]?[.,/]?', r'ban \d*[.,]?\d+[ ]?nghin[ ][.,/]?',r'ban \d*[.,]?\d+[ ]?ng[ ][.,/]?', 
                            # 3.5 dong,
                            r'ban \d*[.,]?\d+[ ]?dong[ ]?[.,/]?', r'ban \d*[.,]?\d+[ ]?d[ ][.,/]?',
                            # 3.5 ty, 3.5 ti
                            r'ban \d*[.,]?\d+[ ]?ty[ ]?[.,/]?',r'ban \d*[.,]?\d+[ ]?ti[ ][.,/]?',
                            # 3.5 trieu, 3.5 tr
                            r'ban \d*[.,]?\d+[ ]?trieu[ ]?[.,/]?',r'ban \d*[.,]?\d+[ ]?tr[ ][.,/]?',

                            # 3.5 ngan, 3.5 nghin 
                            r'gia \d*[.,]?\d+[ ]?ngan[ ]?[.,/]?', r'gia \d*[.,]?\d+[ ]?nghin[ ][.,/]?',r'gia \d*[.,]?\d+[ ]?ng[ ][.,/]?' 
                            # 3.5 dong,
                            r'gia \d*[.,]?\d+[ ]?dong[ ]?[.,/]?', r'gia \d*[.,]?\d+[ ]?d[ ][.,/]?',
                            # 3.5 ty, 3.5 ti
                            r'gia \d*[.,]?\d+[ ]?ty[ ]?[.,/]?',r'gia \d*[.,]?\d+[ ]?ti[ ][.,/]?',
                            # 3.5 trieu, 3.5 tr
                            r'gia \d*[.,]?\d+[ ]?trieu[ ]?[.,/]?',r'gia \d*[.,]?\d+[ ]?tr[ ][.,/]?',

                            # 3.5 ngan, 3.5 nghin 
                            r'=[ ]?\d*[.,]?\d+[ ]?ngan[ ]?[.,/]?', r'=[ ]?\d*[.,]?\d+[ ]?nghin[ .,]',r'[ ]?\d*[.,]?\d+[ ]?ng[.,]?'
                            # 3.5 dong,
                            r'=[ ]?\d*[.,]?\d+[ ]?dong[ ]?[.,/]?', r'=[ ]?\d*[.,]?\d+[ ]?d[ .,]',
                            # 3.5 ty, 3.5 ti
                            r'=[ ]?\d*[.,]?\d+[ ]?ty[ ]?[.,/]?',r'=[ ]?\d*[.,]?\d+[ ]?ti[ .,]',
                            # 3.5 trieu, 3.5 tr
                            r'=[ ]?\d*[.,]?\d+[ ]?trieu[ ]?[.,/]?',r'=[ ]?\d*[.,]?\d+[ ]?tr[ .,]',

                            # 3.5 ngan / nen, 3.5 nghin / nen 
                            r'\d*[.,]?\d+[ ]?ngan[ ]?/[ ]?nen', r'=\d*[.,]?\d+[ ]?nghin[ ]?/[ ]?nen', r'=\d*[.,]?\d+[ ]?ng[ ]?/[ ]?nen' 
                            # 3.5 dong / nen, 3.5d / nen
                            r'\d*[.,]?\d+[ ]?dong[ ]?/[ ]?nen', r'=\d*[.,]?\d+[ ]?d[ ]?/[ ]?nen',
                            # 3.5 ty / nen, 3.5 ti / nen
                            r'\d*[.,]?\d+[ ]?ty[ ]?/[ ]?nen',r'=\d*[.,]?\d+[ ]?ti[ ]?/[ ]?nen',
                            # 3.5 trieu / nen, 3.5 tr / nen
                            r'\d*[.,]?\d+[ ]?trieu[ ]?/[ ]?nen',r'\d*[.,]?\d+[ ]?tr[ ]?/[ ]?nen',
            
                            # 3.5 ngan / can, 3.5 nghin / can 
                            r'\d*[.,]?\d+[ ]?ngan[ ]?/[ ]?can', r'=\d*[.,]?\d+[ ]?nghin[ ]?/[ ]?can',r'=\d*[.,]?\d+[ ]?ng[ ]?/[ ]?can' 
                            # 3.5 dong / can, 3.5d / can
                            r'\d*[.,]?\d+[ ]?dong[ ]?/[ ]?can', r'=\d*[.,]?\d+[ ]?d[ ]?/[ ]?can',
                            # 3.5 ty / can, 3.5 ti / can
                            r'\d*[.,]?\d+[ ]?ty[ ]?/[ ]?can',r'=\d*[.,]?\d+[ ]?ti[ ]?/[ ]?can',
                            # 3.5 trieu / can, 3.5 tr / can
                            r'\d*[.,]?\d+[ ]?trieu[ ]?/[ ]?can',r'\d*[.,]?\d+[ ]?tr[ ]?/[ ]?can',
            
                           ]
        
        price = []
        
        for i in range(len(pattern_of_combine_price_unit)):
            price = price + re.findall(pattern_of_combine_price_unit[i], text)
        
        for i in range(len(pattern_of_combine_price)):
            price = price + re.findall(pattern_of_combine_price[i], text)

        for i in range(len(pattern_of_price)):
            price = price + re.findall(pattern_of_price[i], text)

        for i in range(len(pattern_of_price_unit)):
            price = price + re.findall(pattern_of_price_unit[i], text)
        
        for i in range(len(pattern_of_price_time)):
            price = price + re.findall(pattern_of_price_time[i], text)

        # print(price)

        price_combine = []
        pr = 0
        
        for text in price:
            if ('khach' in text or 'lau' in text or 'phong' in text or 'hem' in text):
                continue
            if (re.findall(r'\d+[ ]?ty[ ]?\d+\w*',text)) or (re.findall(r'\d+[ ]?ti[ ]?\d+\w*',text)) or (re.findall(r'\d+[ ]?trieu[ ]?\d+\w*',text)) or (re.findall(r'\d+[ ]?tr[ ]?\d+\w*',text)):
                # 1 ty 500 fix, 1 ty 750 xay, giá bán 155 triệu10x30= 300m² giá bán 300 triệu15x30= 450m² 
                if ('x' in text):
                    if (re.findall(r'\d+x\d',text)):
                        text = ''
                    else:
                        if ('ty' in text):
                            spl = re.findall(r'\d+[ ]?ty[ ]?\d+[ ]?',text)
                        elif ('ti' in text):
                            spl = re.findall(r'\d+[ ]?ti[ ]?\d+',text)
                        elif ('trieu' in text):
                            spl = re.findall(r'\d+[ ]?trieu[ ]?\d+[ ]?',text)
                        elif ('tr' in text):
                            spl = re.findall(r'\d+[ ]?tr[ ]?\d+',text)
                        try:
                            text = spl[0]
                        except:
                            text = ''
                else:
                    spl = text.split(' ')
                    a = ''
                    for i in range(0,len(spl)):
                        a = a + ' ' + spl[i]
                    text = a
                    
            if text.startswith(".") or text.startswith(","):
                text = text[1:]
            if text.endswith(".") or text.endswith(","):
                text = text[:-1]
            if text.endswith("/"):
                text = "" 
            text = text.replace('gia','').replace('ban','').replace('thue','').replace('=','').strip()
            text = re.sub(r'[ ]?/[ ]?nen','',text)
            text = re.sub(r'[ ]?/[ ]?can','',text)
            if (re.findall(r'trieu[ ]?m2$',text)) or (re.findall(r'tr[ ]?m2$',text)) \
            or  (re.findall(r'ty[ ]?m2$',text)) or (re.findall(r'ti[ ]?m2$',text)) \
            or (re.findall(r'tram[ ]?m2$',text))  \
            or (re.findall(r'ngan[ ]?m2$',text)) or (re.findall(r'nghin[ ]?m2$',text)) or (re.findall(r'ng[ ]?m2$',text))\
            or (re.findall(r'dong[ ]?m2$',text)) or (re.findall(r'd[ ]?m2$',text)):
                text = text.split("m2")[0] + "/m2"
            text = text.replace(',','.')
            if (text != ""):
                price_combine.append(text) 

        # print(price_combine)

        if (price_combine):
            # nhà bán nhưng đang cho thuê
            if ('bán' in org_text.lower() and 'th' in price_combine[0]):
                pr = 0
            # đất bán nhưng đang cho thuê
            elif ('đất nền' in org_text.lower() and 'th' in price_combine[0]):
                pr = 0
            else:
                try:
                    # use surface input first
                    if (surface_in_m2 != 0):
                        pr = get_price(price_combine[0],'',surface_in_m2)
                    # if not found surface input, then use surface from text
                    else:
                        sf = get_surface_from_text(org_text)
                        pr = get_price(price_combine[0],'',sf)
                except:
                    pr = 0    
        return pr
    return 0

# GET SURFACE FROM TEXT
def parsing_surface(text):
    '''
        Parsing surface from surface pattern

            Parameters:
                text (str): surface pattern
                
            Returns:
                surface (float): Surface parsing from surface pattern
    '''
    text = str(text).strip().replace(' ','').replace('m2','').replace('m','')
    text = remove_delimiter(text)
    surface = 0
    if (text is not None):
        if text.startswith(".") or text.startswith(","):
            text = text[1:]
        if text.endswith(".") or text.endswith(","):
            text = text[:-1]
        try:
            surface = float(text)
        except:
            surface = 0
    return surface
    
def get_surface_from_text(text):
    '''
        Get surface from text

            Parameters:
                text (str): A text need to be get surface
                
            Returns:
                surface (float): Surface in m2 found from text. If surface hasn't found, return surface is 0
    '''
    if text is not None: #convention naming pep8
        # print(text)
        text = text.lower()
        text = unidecode(text)
        ls_remove = [":","dat","tu","can ban","la","ha noi","ha dong","ha bac","ha tay","ha nam","ha giang","thong thuy","=>",")","(","vuong vuc"]
        for e in ls_remove:
            text = text.replace(e, " ")
        text = text.replace("vuong","2").replace("mv","m2")
        #no hau 21.23m2
        text = re.sub(r'no hau \d+[.,]?\d*[ ]?m[ ]?2','',text)
        text = re.sub(r't1m2','m2',text)
        text = ' '.join(text.split())

        pattern_of_surface = [r'\d+[.,]?\d*[ ]?m2[ ]?x[ ]?\d+[.,]?\d*[ ]?[a-ln-z][ ]?=?[ ]?\w*',
                              r'\d+[.,]?\d{3}[ ]?[.,]\d+m[ ]?2[ ]?\w*',
                              r'x?\d+[.,]?\d*[ ]?m[ ]?2[ ]?\w*[ ]?\w*[ ]?=?',
                              r'dien tich[ ]?\d+[.,]?\d*[ ]?m?[ ]?\d*[ ]?x?[ ]?\d*[.,]?\d*\w*[ ]?=?[ ]?\w*', 
                              r'dt[ ]?\d+[.,]?\d*[ ]?m?[ ]?\d*[ ]?x?[ ]?\d*[.,]?\d*\w*[ ]?=?[ ]?\w*',
                              r'dat[ ]*\d+[.,]?\d*[ ]?ha[ \.,]',r'dat[ ]*\d+[.,]?\d*[ ]?hecta',r'dat[ ]*\d+[.,]?\d*[ ]?hec[ \.,]',
                              r'\d+[.,]?\d*[ ]?ha[ \.,]dat',r'\d+[.,]?\d*[ ]?hecta dat',r'\d+[.,]?\d*[ ]?hec[ \.,]dat',                         
                             ]
        surface = []
        for i in range(len(pattern_of_surface)):
            surface = surface + re.findall(pattern_of_surface[i], text)

        # print(surface)

        sf_collect = []
        sf = 0
        
        for s in surface:
            s = s.strip()
            # 105 m2
            #Giá: 16 triệu/ 1m2 
            if (re.findall(r'/[ ]?1m2',s)):
                sf = 0
            # dt 1 ha7
            elif ((re.findall(r'\d+[.,]?\d*[ ]?ha[ ]?\d*',s)) or (re.findall(r'\d+[.,]?\d*[ ]?hecta[ ]?\d*',s)) or (re.findall(r'\d+[.,]?\d*[ ]?hec[ ]?\d*',s))):
                # 280/389,4 m2 HA01-15
                if (re.findall(r'm[ ]?2',s)):
                    continue
                s = s.replace('hec','hecta').replace('ha','hecta').replace(',','.')
                s4 = re.findall(r'\d+[.,]?\d*[ ]?hecta[ ]?\d*',s)
                if (s4):
                    # print("s4",s4)
                    s4a = s4[0].split("hecta")
                    if ('.' in s4a[0]):
                        sf = float(s4a[0])*10000
                    else:
                        ss4 = s4[0].strip().replace('hecta','.').replace(' ','')
                        sf = float(ss4)*10000
                        break
            elif (re.findall(r'\d+[.,]?\d{3}[ ]?[.,]\d+m[ ]?2[ ]?\w*',s)):
                s = s.replace(' ','')
                s0 = re.findall(r'\d+[.,]?\d{3}[ ]?[.,]\d+m[ ]?2',s)
                if (s0):
                    sf_collect.append(s0[0])
            elif (re.findall(r'\d+[.,]?\d*[ ]?m2[ ]?x[ ]?\d+[.,]?\d*[ ]?[a-ln-z][ ]?=?[ ]?\w*',s)):
                s1 = re.findall(r'\d+[.,]?\d*[ ]?m2[ ]?x[ ]?\d+[.,]?\d*[ ]?[a-ln-z][ ]?=?[ ]?\w*',s)
                if (s1):
                    # print("s1",s1)
                    if (re.findall(r'\d+[ ]?m2[ ]?x[ ]?\d+',s1[0])) or ('x' not in s1[0]):
                        ss1 = re.findall(r'\d+[.,]?\d*[ ]?m2[ ]?x',s1[0])
                        if (ss1):
                            sf_collect.append(ss1[0].replace('x',''))
            elif (re.findall(r'dien tich[ ]?\d+[.,]?\d*[ ]?m?[ ]?\d*[ ]?x?[ ]?\d*[.,]?\d*\w*[ ]?=?[ ]?\w*',s)) or (re.findall(r'dt[ ]?\d+[.,]?\d*[ ]?m?[ ]?\d*[ ]?x?[ ]?\d*[.,]?\d*\w*[ ]?=?[ ]?\w*',s)):
                s2 = re.findall(r'\d+[.,]?\d*[ ]?m?[ ]?\d*[ ]?x?[ ]?\d*[.,]?\d*\w*[ ]?=?[ ]?\w*',s)
                if (s2):
                    # print("s2",s2)
                    if ('=' not in s2[0]) and (not re.findall(r'^0\d',s2[0])):
                        if (not re.findall(r'\d+[ ,]?\d+',s2[0])):
                            pass
                        #diện tích 6x20 thổ cư
                        elif (re.findall(r'x[ ]?\d+[.,]?\d*[ ]?tang',s2[0])) or (re.findall(r'x[ ]?\d+[.,]?\d*[ ]?t[ ]',s2[0])) or (re.findall(r'x[a-z]',s2[0])) or ('x' not in s2[0]):
                            ss2 = re.findall(r'\d+[.,]?\d*[ ]?m?',s2[0])
                            #print("sss2",ss2)
                            if (ss2):
                                sf_collect.append(ss2[0])
                        #dien tich 600m2 20x30m gia, dien tich 40 m 3,9 x 11
                        elif (' ' in s2[0]):
                            ss2 = s2[0].split(' ')
                            if ('x' not in ss2[0]) and (re.findall('\d+[ ]?m[ ]?2?',ss2[0])):
                                sf_collect.append(ss2[0])
            elif (re.findall(r'x?\d+[.,]?\d*[ ]?m[ ]?2[ ]?\w*[ ]?\w*[ ]?=?',s)):
                s3 = re.findall(r'x?\d+[.,]?\d*[ ]?m[ ]?2[ ]?\w*[ ]?\w*[ ]?=?',s)
                if (s3):
                    # print("s3",s3)
                    if ('=' not in s3[0]) and (not re.findall(r'^1m2',s3[0])) and (not re.findall(r'^x\d+m[ ]?2',s3[0])):
                        if (re.findall(r'x[ ]?\d+[ ]?tang',s3[0])) or (re.findall(r'x[ ]?\d+[ ]?t[ ]',s3[0])) or (re.findall(r'x[a-z]',s3[0])) or ('x' not in s3[0]):
                            ss3 = re.findall(r'\d+[.,]?\d*[ ]?m[ ]?2',s3[0])
                            sf_collect.append(ss3[0])
                        #600m2 20x30m
                        elif (' ' in s3[0]):
                            #print("ss3")
                            ss3 = s3[0].split(' ')
                            if (re.findall('\d+[ ]?m[ ]?2',ss3[0])):
                                sss3 = re.findall('\d+[ ]?m[ ]?2',ss3[0])
                                sf_collect.append(sss3[0])
                    #5 x 30 = 150m2
                    elif (re.findall(r'=[ ]?$',s3[0])):
                        ss3 = s3[0].split('=')
                        if ('x' not in ss3[0]) and (re.findall('\d+[ ]?m[ ]?2',ss3[0])):
                            n = ss3[0].split("m2")
                            sf_collect.append(n[0] + " m2")
        if len(sf_collect)> 0:
            sf = parsing_surface(sf_collect[0])
        return sf
    return 0

# GET ROAD WIDTH    
def parsing_alley_frontage(text):
    '''
        Parsing alley frontage from alley frontage pattern

            Parameters:
                text (str): alley frontage pattern
                
            Returns:
                nb (float): alley frontage from alley frontage pattern
    '''
    text = str(text).strip().replace(',','.')
    if text.startswith(".") or text.startswith(","):
        text = text[1:]

    if text.endswith("m2") or text.endswith("m"):
        text= text.replace('m2','m').replace('m','')
    else:
        text = text.replace('m','.')
    try:
        nb = float(text)
    except:
        nb = 0
    return nb
    
def get_road_width(text):
    '''
    Returns alley access and frontage fields

        Parameters:
            text(string): Detailed brief field of ads

        Returns:
            List A: ALLEY_ACCESS = A[0], FRONTAGE=A[1]
                        Extract width of road in front of the property based on the following patterns:
                            hẻm trước nhà: Wm
                            đường trước nhà: Wm
                            Hẻm oto | hẻm ôtô | hẻm xe hơi | hẻm xe máy | hẻm xe ba gác ba gac : Wm

                            if pattern is Hẻm ba gác, W=2m; hẻm xe máy W=1m
                            HXH, W=3m or W=4m
                            HXT, W=5m

                            FRONTAGE :
                            đường mặt tiền: Wm
                            nhà mặt tiền: Wm
    '''
    if text is not None: #convention naming pep8
        text = text.lower()
        text = text.strip().replace(":", "")
        text = unidecode(text)
        ls= ("ben hong","rong","ngang","khung","hon","lon","gan","toi","sieu","hien huu","truoc dat","len den", "va hau deu")
        text= replace_characters(text,ls," ")
        text= re.sub(' +', ' ', text)

        pattern_of_alley_access = [
            r'\w*[ ]?hem truoc nha \d+[.,]?\d*m\d*',
            r'\w*[ ]?duong truoc nha \d+[.,]?\d*m\d*', 
            r'\w*[ ]?duong nhua \d+[.,]?\d*m\d*',
            r'\w*[ ]?duong vao xe hoi \d+[.,]?\d*m\d*', r'\w*[ ]?duong hien trang \d+[.,]?\d*m\d*', 
            r'\w*[ ]?duong hem \d+[.,]?\d*m\d*', 
            r'\w*[ ]?duong be tong o[ ]?to \d+[.,]?\d*m\d*', r'\w*[ ]?duong be tong \d+[.,]?\d*m\d*',
            r'\w*[ ]?hem o[ ]?to \d+[.,]?\d*m\d*', r'\w*[ ]?hem thong o[ ]?to \d+[.,]?\d*m\d*',
            r'\w*[ ]?hem xe hoi \d+[.,]?\d*m\d*', r'\w*[ ]?hem thong xe hoi \d+[.,]?\d*m\d*',
            r'\w*[ ]?hem xe may \d+[.,]?\d*m\d*', r'\w*[ ]?hem thong xe may \d+[.,]?\d*m\d*',
            r'\w*[ ]?hem xe tai \d+[.,]?\d*m\d*', r'\w*[ ]?hem thong xe tai \d+[.,]?\d*m\d*',
            r'\w*[ ]?hem rong \d+[.,]?\d*m\d*',
            r'\w*[ ]?[ ]hem \d+[.,]?\d*m\d*', r'\w*[ ]?[ ]hem thong \d+[.,]?\d*m\d*', r'\w*[ ]?[ ]hem cut \d+[.,]?\d*m\d*', r'\w*[ ]?[ ]hem nhua \d+[.,]?\d*m\d*', r'\w*[ ]?[ ]hem be tong \d+[.,]?\d*m\d*',
            r'\w*[ ]?hem xe tai', r'\w*[ ]?duong xe tai',
            r'\w*[ ]?hem xe may',
            r'\w*[ ]?hem xe hoi', r'\w*[ ]?hem xe oto', r'\w*[ ]?hem oto', r'\w*[ ]?hem o to', r'\w*[ ]?hem xe o to',
            r'\w*[ ]?hem xe ba gac', r'\w*[ ]?hem ba gac']
    
        alley_access = []

        for i in range(len(pattern_of_alley_access)):
            alley_access = alley_access + \
                re.findall(pattern_of_alley_access[i], text)

        # print(alley_access)

        for i in range(len(alley_access)):
            if ('cach' in alley_access[i]):
                alley_access[i] = ''
            if ('hem' in alley_access[i]) and (re.findall(r'[0-9]+',alley_access[i])):
                s = alley_access[i].split('hem')
                alley_access[i] = s[1]
            elif ('duong' in alley_access[i]):
                s = alley_access[i].split('duong')
                alley_access[i] = s[1]
                
            if (re.findall(r"\d+[.,]?\d*m\d*", alley_access[i])):
                alley_access[i] = re.findall(r"\d+[.,]?\d*m\d*", alley_access[i])
            elif (re.findall(r"hem xe may", alley_access[i])):
                alley_access[i] = [HEM_XEMAY]
            elif (re.findall(r"hem xe ba gac", alley_access[i]) or re.findall(r"hem ba gac", alley_access[i])):
                alley_access[i] = [HEM_XEBAGAC]
            elif (re.findall(r"hem xe tai", alley_access[i]) or re.findall(r"duong xe tai", alley_access[i])):
                alley_access[i] = [HEM_XETAI]
            elif (re.findall(r"hem xe hoi", alley_access[i]) or re.findall(r"hem xe o to", alley_access[i]) or re.findall(r"hem oto", alley_access[i]) or re.findall(r"hem xe oto", alley_access[i]) or re.findall(r"hem o to", alley_access[i])):
                alley_access[i] = [HEM_XEHOI]
        
        alley_access = [x for x in alley_access if x != '']

        pattern_of_frontage = [
            r'\w*[ ]?mat tien \d+ \d+[.,]?\d*m\d*', r'\w*[ ]?mat tien \d+[.,]?\d*m\d*', r'mat tien duong \d+[.,]?\d*m\d*', 
            r'mat tien duong nhua \d+[.,]?\d*m\d*', r'duong mat tien \d+[.,]?\d*m\d*', 
            r'nha mat tien \d+[.,]?\d*m\d*']
        frontage = []
        for i in range(len(pattern_of_frontage)):
            frontage = frontage + re.findall(pattern_of_frontage[i], text)

        # print(frontage)
        
        for i in range(len(frontage)):
            if ('2' in frontage[i]):
                frontage[i] = ''
            else:
                if ('mat tien' in frontage[i]):
                    s = frontage[i].split('mat tien')
                    frontage[i] = s[1]
                elif ('duong' in frontage[i]):
                    s = frontage[i].split('duong')
                    frontage[i] = s[1]
                frontage[i] = re.findall(r"\d+[.,]?\d*m\d*", frontage[i])

        frontage = [x for x in frontage if x != '']

        # print(frontage)

        ##Alleyaccess )(duong nhua)
        pattern_of_alleyaccess = [r'\w*[ ]?duong nhua[ ]?\d+[.,]?\d*m\d*']
        alleyaccess=[]
        for i in range(len(pattern_of_alleyaccess)):
            alleyaccess = alleyaccess + re.findall(pattern_of_alleyaccess[i], text)

        for i in range(len(alleyaccess)):
            alleyaccess[i] = re.findall(r"\w*[ ]?duong nhua[ ]?\d+[.,]?\d*m\d*", alleyaccess[i])
        
        for x in alleyaccess:
            sub= x[0].split('duong nhua')

            if re.findall(r"\w*?[ ]?duong[ ]?nhua", text):
                x[0]= re.sub(r'\w*?[ ]?duong[ ]?nhua', '', x[0])

            if sub[0].startswith("cach") or sub[0].startswith("gan"):
                alleyaccess.remove(x)

        alley = 0
        front = 0

        if len(alleyaccess)> 0:
            alley = parsing_alley_frontage(alleyaccess[0][0])

        if len(alley_access)> 0:
            alley = parsing_alley_frontage(alley_access[0][0])
        
        if len(frontage)> 0:
            front = parsing_alley_frontage(frontage[0][0])

        return alley,front
    return 0, 0

# GET WIDTH LENGTH
def parsing_width_length(s):
    '''
        Parsing width length from width length pattern

            Parameters:
                s (str): with length pattern
                
            Returns:
                nb (float): width length from with length pattern
    '''
    s = s.strip().replace(',','.')
    if s.startswith(".") or s.startswith(","):
        s = s[1:]    
        
    if s.startswith("ngang") or s.startswith("rong") or s.startswith("dai") or s.startswith("sau") or s.startswith("chieu dai") or s.startswith("chieu sau"):
        s = s.replace("ngang",'').replace("rong",'').replace("dai",'').replace("sau",'').replace("chieu dai",'').replace("chieu sau",'').strip()

    if s.startswith("be ngang sieu rong") or s.startswith("be the") or s.startswith("tren") or s.startswith("gan") or s.startswith("hon") or s.startswith("chieu"):
        s= s.replace("be ngang sieu rong",'').replace("be the",'').replace("tren",'').replace("gan",'').replace("hon",'').replace("chieu",'').strip()
    
    if s.startswith("r"):
        s= s.replace("r",'')

    if s.startswith("="):
         s = s.replace("=",'')

    if s.startswith(" ngang"):
        s = re.sub('\s+', '', s)

    if s.split(' '):
        s= s.split(" ", maxsplit=1)[0]

    if s.endswith('.') or  s.endswith(';'):
        s= s[:-1]

    if s.endswith("m2") or s.endswith("m"):
        wl= s.replace('m2','m').replace('m','')
    else:
        wl = s.replace('m','.').strip()
    try:
        nb = float(wl)
    except:
        nb = 0
    return nb

def get_width_length(text):
    '''
    Returns width and length field of ads

        Parameters:
            text(string): Detailed brief field of ads

        Returns:
            List A: WIDTH = A[0], LENGTH=A[1]
                Extract width & length of the property based on the following patterns:
                    DTXD: WxLm
                    Diện tich: WxLm | WmxLm
                    Bề ngang: Wm
                    Bề dài: Lm
                    chiều dài: Lm
                    Chiều rộng: Wm
    '''
    #Check if text= None return 0. Not none execution 
    if text is not None: #convention naming pep8
        text = text.lower()
        text = text.replace(":", " ")
        #text = text.replace("(", " ").replace(")", "")
        text = re.sub(r'_*',"",text)
        text= text.replace('mét', "m").replace("met","m")
        text = unidecode(text)
        ls= ("khung", "la", "khoang", "tren","hon", "len den")
        text= replace_characters(text,ls," ")
        text= re.sub(' +', ' ', text)   

        return_wl = []

        ##Pattern width##
        pattern_of_widths = [
            r'chieu ngang \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'chieu ngang nha \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'chieu rong \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'be ngang \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'be ngang nha \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'be ngang rong \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'mat sau \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'mat sau nha \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'ngang nha \d*[.,]?m?\d+[ ]?m?[ ]?']
        widths = []
        for i in range(len(pattern_of_widths)):
            widths = widths + re.findall(pattern_of_widths[i], text)

        for i in range(len(widths)):
            widths[i] = re.findall(r"\d*[.,]?m?\d+[ ]?m?[ ]?", widths[i])

        ##Pattern length##
        pattern_of_lengths = [
            r'chieu dai \d*[.,]?m?\d+[ ]?m?[ ]?', 
            r'be dai \d*[.,]?m?\d+[ ]?m?[ ]?', 
            r'chieu sau \d*[.,]?m?\d+[ ]?m?[ ]?', 
            r'be sau \d*[.,]?m?\d+[ ]?m?[ ]?']
        lengths = []
        for i in range(len(pattern_of_lengths)):
            lengths = lengths + re.findall(pattern_of_lengths[i], text)

        for i in range(len(lengths)):
            lengths[i] = re.findall(r"\d*[.,]?m?\d+[ ]?m?[ ]?", lengths[i])

        w=0
        l=0

        if len(widths) > 0:
            w= parsing_width_length(widths[0][0])

        if len(lengths) > 0: 
            l= parsing_width_length(lengths[0][0])
        
        if w != 0 or l!=0:
            return_wl.append((w,l))

        ##Pattern DT all cases##
        pattern_of_areas= [
            ##ngang Wm, no hau Nm, dai Lm
            r'ngang \d*[.,]?m?\d+[ ]?m?[ ]?[.,]?[ ]?\w*[ ]?\w*[ ]?[\d+]?[.,]?[\d+]?m?[.,]?[ ]?dai \d*[.,]?m?\d+[ ]?m?[ ]?',
            #ngang x chieu dai/ chieu sau
            r'ngang \d*[.,]?m?\d+[ ]?m?[ ]?[,.x\*]?[ ]?chieu dai \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'ngang \d*[.,]?m?\d+[ ]?m?[ ]?[,.x\*]?[ ]?chieu sau \d*[.,]?m?\d+[ ]?m?[ ]?',

            #Wm x chieu dai/ chieu sau
            r'\d*[.,]?m?\d+[ ]?m?[ ]?[,.x\*]?[ ]?chieu dai \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'\d*[.,]?m?\d+[ ]?m?[ ]?[-,.x\*]?[ ]?dai \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'\d*[.,]?m?\d+[ ]?m?[ ]?[,.x\*]?[ ]?chieu sau \d*[.,]?m?\d+[ ]?m?[ ]?',

            #Wm ngang x Lm dai, Wm ngang, dai Lm
            r'\d*[.,]?m?\d+[ ]?m?[ ]?ngang[ ]?[,.x\*]?[ ]?\d*[.,]?m?\d+[ ]?m?[ ]?dai',
            r'\d*[.,]?m?\d+[ ]?m?[ ]?ngang[ ]?[,.x\*]?[ ]?dai \d*[.,]?m?\d+[ ]?m?[ ]?',

            #Wm ngang (tre/gan) x Lm dai (tren/gan, hon), be ngang sieu rong Wm va dai Lm
            r'be ngang sieu rong \d*[.,]?m?\d+[ ]?m?[.]?[ ]?va[ ]?dai \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'ngang tren \d*[.,]?m?\d+[ ]?m?[.]?[ ]?[-,.x\*]?[ ]?dai tren \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'ngang gan \d*[.,]?m?\d+[ ]?m?[.]?[ ]?[-,.x\*]?[ ]?dai hon \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'ngang be the \d*[.,]?m?\d+[ ]?m?[.]?[ ]?[-,.x\*]?[ ]?dai hon \d*[.,]?m?\d+[ ]?m?[ ]?',

            #ngang Wm dai tren Lm, ngang Wm dai gan Lm
            r'ngang \d*[.,]?m?\d+[ ]?m?[.]?[ ]?[-,.x\*]?[ ]?dai tren \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'ngang \d*[.,]?m?\d+[ ]?m?[.]?[ ]?[-,.x\*]?[ ]?dai gan \d*[.,]?m?\d+[ ]?m?[ ]?',
             r'ngang \d*[.,]?m?\d+[ ]?m?[.]?[ ]?[-,.x\*]?[ ]?dai hon \d*[.,]?m?\d+[ ]?m?[ ]?',

            #ngang/rong x dai/ sau
            r'ngang \d*[.,]?m?\d+[ ]?m?[ ]?[-,.x\*]?[ ]?dai \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'rong[ ]?[=]?[ ]?\d*[.,]?m?\d+[ ]?m?[;]?[ ]?[-,.x\*]?[ ]?dai[ ]?[=]?[ ]?\d*[.,]?m?\d+[ ]?m?[ ]?',
            r'ngang[ ]?\d*[.,]?m?\d+[ ]?m?[ ]?[,.x\*]?[ ]?sau \d*[.,]?m?\d+[ ]?m?[ ]?',
            r'rong \d*[.,]?m?\d+[ ]?m?[ ]?[,.x\*]?[ ]?sau \d*[.,]?m?\d+[ ]?m?[ ]?',
            #r=Wm; d=Lm;
            r'r[ ]?[=]?[ ]?\d*[.,]?m?\d+[ ]?m?[ ]?[;,.x\*]?[ ]?d[ ]?[=]?[ ]?\d*[.,]?m?\d+[ ]?m?[ ]?'

        ]
        areas = []
        
        for i in range(len(pattern_of_areas)):
            areas = areas + re.findall(pattern_of_areas[i], text)

        ##Parsing pattern DT and return  width, length 
        if areas: #convention if naming pep8
            values= ''
            index=['x', '*', '-','chieu dai', 'chieu sau', 'dai', 'sau','d', 'va']
            for temp in index:
                if temp in areas[0]:
                    values = temp
                    break
            #Parsing pattern area
            a = areas[0].split(values)
            w= parsing_width_length(a[0])
            l= parsing_width_length(a[1])
            
            if (w != 0 or l!=0):
                return_wl.append((w,l))

        ##Pattern dai Lm x ngang Wm, Lm sau x Wm ngang
        pattern_of_lengthwidths= [
            r'dai \d*[.,]?m?\d+[ ]?m?[ ]?[-,.x\*]?[ ]?ngang \d*[.,]?m?\d+[ ]?m?',
            r'dai \d*[.,]?m?\d+[ ]?m?[ ]?[-,.x\*]?[ ]?rong \d*[.,]?m?\d+[ ]?m?',
            r'\d*[.,]?m?\d+[ ]?m?[ ]?sau[ ]?[,.x\*]?[ ]?\d*[.,]?m?\d+[ ]?m?[ ]?ngang']

        lengthwidths = []
        
        for i in range(len(pattern_of_lengthwidths)):
            lengthwidths = lengthwidths+ re.findall(pattern_of_lengthwidths[i], text)

        if lengthwidths:
            values= ''
            dilimiter=['x', '*', '-', 'ngang', 'rong']
            for temp in dilimiter:
                if temp in lengthwidths[0]:
                    values = temp
                    break
            #Parsing pattern length & width
            lw = lengthwidths[0].split(values)
            w= parsing_width_length(lw[1])
            l= parsing_width_length(lw[0])
            
            if (w != 0 or l!=0):
                return_wl.append((w,l))

        ##Patern ngang Wm (letter) dai Lm ## "ngang 40m tiep giap lo nhua dai 22 m" ###
        pattern_of_widthlength=[r'ngang \d*[.,]?m?\d+[ ]?m? .*[,]? dai \d*[.,]?m?\d+[ ]?m?[ ]?']
        widthlength = [] 

        for i in range(len(pattern_of_widthlength)):
            widthlength = widthlength + re.findall(pattern_of_widthlength[i], text)

        for i in range(len(widthlength)):
            widthlength[i] = re.findall(r"\d*[.,]?m?\d+[ ]?m?", widthlength[i])
        
        if widthlength:
            w= parsing_width_length(widthlength[0][0])
            l= parsing_width_length(widthlength[0][1])
                
            if (w != 0 or l!=0):
                return_wl.append((w,l))


        ##Patter general##
        pattern_of_general=[r'\d*[.,]?m?\d+[ ]?m?[ ]?[x\*][ ]?\d*[.,]?m?\d+[ ]?m?\w*']   
        general = [] 

        for i in range(len(pattern_of_general)):
            general = general + re.findall(pattern_of_general[i], text)

        for x in general:
            if 'tret' not in x:
                if 'tang' in x or 'lau' in x or re.findall(r'\dt', x):
                    general.remove(x)

        if general:
            values= ''
            index=['x', '*']
            for temp in index:
                if temp in general[0]:
                    values = temp
                    break
            ##Parsing pattern area
            g = general[0].split(values)
            if re.findall(r'[a-ln-z]*', g[1]):
                g[1]= re.sub(r'[a-ln-z]*', '', g[1])
            w= parsing_width_length(g[0])
            l= parsing_width_length(g[1])
                
            if (w != 0 or l!=0):
                return_wl.append((w,l))


        ##Pattern only width##
        pattern_of_width=[r'\w*?[ ]?ngang \d*[.,]?m?\d+[ ]?m?[ ]?']
        width = []

        for i in range(len(pattern_of_width)):
            width = width + re.findall(pattern_of_width[i], text)

        for i in range(len(width)):
            width[i] = re.findall(r"\w*?[ ]?ngang \d*[.,]?m?\d+[ ]?m?[ ]?", width[i])

         ##Pattern only length##
        pattern_of_length=[r'\w*?[ ]?sau \d*[.,]?m?\d+[ ]?m?[ ]?']
        length= []

        for i in range(len(pattern_of_length)):
            length = length + re.findall(pattern_of_length[i], text)

        for i in range(len(length)):
            length[i] = re.findall(r"\w*?[ ]?sau \d*[.,]?m?\d+[ ]?m?[ ]?", length[i])

        ## if width, length and parsing special case (Wm2, Lm2, WmW, LmL)
        for x in width:
            sub= x[0].split('ngang')
            
            if re.findall(r"\w*?[ ]?ngang", text):
                x[0]= re.sub(r'\w*?[ ]?ngang', '', x[0])

            if sub[0].startswith("lon") or sub[0].startswith("tien"):
                width.remove(x)


        for x in length:
            sub= x[0].split('sau')

            if re.findall(r"\w*?[ ]?sau", text):
                x[0]= re.sub(r'\w*?[ ]?sau', '', x[0])

            if sub[0].startswith("boi") or sub[0].startswith("tho") or sub[0].startswith("truoc") or sub[0].startswith("lung"):
                length.remove(x)

        w=0
        l=0

        if len(width) > 0: 
            w= parsing_width_length(width[0][0]) 

        if len(length) > 0: 
            l= parsing_width_length(length[0][0]) 
        
        if w != 0 or l!=0:
            return_wl.append((w,l))

        if (return_wl):
            return return_wl[0][0], return_wl[0][1]
            
    return 0, 0
