from config.config_ import *

# ADS_DATE
def convert_date(ads_date):
    '''
        Convert date to standard format yyyy-mm-dd

            Parameters:
                ads_date (date): date need to format
                    
            Returns:
                format_date (date): date has been formated
    '''
    format_date = None
    if (ads_date is not None):
        ads_date = str(ads_date).lower()
        ads_date = ads_date.replace("\n", "")
    
        ads_date = ads_date.replace(" ", "")
        if ads_date.startswith("-") or ads_date.startswith("/") or ads_date.startswith(",") or ads_date.startswith("."):
            ads_date = ads_date[1:]
        if ads_date.endswith("-") or ads_date.endswith("/") or ads_date.endswith(".") or ads_date.endswith(","):
            ads_date = ads_date[:-1]

        pattern = ["/","-"]
        for p in pattern:
            if (p in ads_date):
                date = ads_date.split(p)
                if (len(date[0]) == 4):
                    if (int(date[1]) > 12 and int(date[2]) <= 12):
                        ads_date_obj = datetime.datetime.strptime(ads_date, '%Y'+p+'%d'+p+'%m')
                    elif (int(date[2]) > 12 and int(date[1]) <= 12):
                        ads_date_obj = datetime.datetime.strptime(ads_date, '%Y'+p+'%m'+p+'%d')
                    else:
                        ads_date_obj = datetime.datetime.strptime(ads_date, '%Y'+p+'%m'+p+'%d')
                else:
                    if (int(date[1]) > 12 and int(date[0]) <= 12):
                        ads_date_obj = datetime.datetime.strptime(ads_date, '%m'+p+'%d'+p+'%Y')
                    elif (int(date[0]) > 12 and int(date[1]) <= 12):
                        ads_date_obj = datetime.datetime.strptime(ads_date, '%d'+p+'%m'+p+'%Y')
                    else:
                        ads_date_obj = datetime.datetime.strptime(ads_date, '%d'+p+'%m'+p+'%Y')
                format_date = ads_date_obj.strftime('%Y-%m-%d')
                format_date = datetime.datetime.strptime(format_date, "%Y-%m-%d").date()
    return format_date

def convert_date_str(ads_date,created_date):
    '''
        Convert date string to date with format yyyy-mm-dd based on rules

            Parameters:
                ads_date (date): date post the ads
                created_date (date): date download the ads

            Returns:
                format_date (date): date post the ads has been formated
    '''
    format_date = None
    if (ads_date is not None and created_date is not None):
        created_date = created_date.strftime('%Y-%m-%d')
        created_date_obj = datetime.datetime.strptime(created_date, '%Y-%m-%d')
        ads_date = str(ads_date).lower().replace("ngày đăng","").strip()
        
        # 02/12 2020
        if (re.findall(r'[ ]\d{4}$',ads_date)):
            ads_date = ads_date.replace(" ","")
            format_date = datetime.datetime.strptime(ads_date, '%d/%m%Y').date()
            return format_date
        
        # 14:05 - 14/12/2020
        if (re.findall(r'\d{2}:\d{2}',ads_date)):
            ads_date = re.sub(r'\d{2}:\d{2}','',ads_date)

        # 26/06 
        if (re.findall(r'^\d{2}/\d{2}$',ads_date)):
            year = created_date.split('-')
            ads_date = ads_date + "/" + str(year[0]) 

        # standard format
        try:
            if (not (re.findall(r'[a-zA-Z]',ads_date))):
                return convert_date(ads_date)
        except:
            return None

        # hôm nay
        if ("hôm nay" in ads_date):
            format_date = created_date_obj.date()
        # hôm qua
        elif ("hôm qua" in ads_date):
            format_date = created_date_obj.date() - timedelta(days=1)
        # compound
        else:
            number = 0
            dic_number = {}
            pattern = [("năm",365),("tháng",30),("tuần",7),("ngày",1)]
            for p in pattern:
                if p[0] in ads_date:
                    val = ads_date.split(p[0])
                    x = val[len(val)-2]
                    xx = x.split(" ")
                    try:
                        dic_number[p[0]] = (int(xx[len(xx)-2]),p[1])
                    except:
                        return format_date
                else:
                    dic_number[p[0]] = (0,p[1])
            for i in dic_number:
                number = number + dic_number[i][0] * dic_number[i][1]
            format_date = created_date_obj.date() - timedelta(days=number)
    return format_date

# LAND_TYPE, LEGAL_STATUS, PRO_DIRECTION
def replace_characters(string,set_char,spe_char):
    '''
        Replace set of characters to a specific character

            Parameters:
                    string (str): A string need to be converted
                    set_char (array of str): An array of char need to be replaced
                    spe_char (str): Replace char

            Returns:
                    string (str): A string converted
    '''
    if (string is not None):
        for char in set_char:
            string = string.replace(char,spe_char)
    else:
        string = None
    return string

def normalize_land_type(item):
    '''
    Get exactly land_type from string
    Parameter:
        - item (str): crawled land type
    Return:
        - rt_item (str): land type in dictionary
    '''
    rt_item = None
    if item is not None:
        item = item.lower().strip()
        if (re.findall(r'^bán',item)):
            item = item.split('bán')[-1]
        elif (re.findall(r'^cho thuê',item)):
            item = item.split('cho thuê')[-1]
        rt_item = item.split('tại')[0].strip()
    return rt_item

def get_value(dic,string):
    '''
        Convert value crawled from site to standard value 

            Parameters:
                dic (dictionary): one of three types, including LEGAL_STATUS, LAND_TYPE, PRO_DIRECTION
                string (str): crawled value

            Returns:
                standard_string (str): standard value. In case there is no mapped value from the dictionary, return the crawled value
    '''
    standard_string = None
    if (string is not None):
        string = string.lower()
        string = re.sub(r'\.$','',string)
        string = string.replace("\"","").strip()
        if string in dic.keys():
            standard_string = dic[string]
        else:
            standard_string = limit_characters(string,255)
    return standard_string

def get_value_from_str(dic,string):
    '''
        Find one of the following words in the string then get value in the dictionary

            Parameters:
                dic (dictionary): dictionary for looking up
                string (str): string need to get value
                    
            Returns:
                value (date): value get from string after looking up dictionary. If not have return None
    '''
    value = None
    pattern = list(dic.keys())
    if (string is not None):
        string = string.lower()
        string = re.sub(r'\.$','',string)
        string = unidecode(string)
        string = replace_characters(string.lower(),["-","_","/"]," ")
        for i in pattern:
            if (re.search(i, str(string))):
                value = get_value(dic,i)
                break
    return value

def get_value_advance(dic,dic_short,string):
    '''
        Convert value crawled from site by mapping to dic to standard value, if string not have in dic then continue search in dic short

            Parameters:
                dic (dictionary): one of three types, including LEGAL_STATUS, LAND_TYPE, PRO_DIRECTION
                dic_short (dictionary): one of three types, including LEGAL_STATUS_SHORT, LAND_TYPE_SHORT, PRO_DIRECTION_SHORT
                string (str): crawled value

            Returns:
                standard_string (str): standard value. In case there is no mapped value from the dictionary, return the crawled value
    '''
    standard_string = None
    if (string is not None):
        string = string.lower()
        string = string.replace("\"","").strip()
        if string.startswith(".") or string.startswith(","):
            string = string[1:]
        if string.endswith(".") or string.endswith(","):
            string = string[:-1]
        if string in dic.keys():
            standard_string = dic[string]
        else:
            map_string = get_value_from_str(dic_short,string)
            if (map_string is not None):
                string = map_string
            standard_string = limit_characters(string,255)
    return standard_string

# PRO_WIDTH, PRO_LENGTH, NB_ROOMS, BEDROOM, BATHROOM
def check_empty(string):
    '''
        Check string empty or not

            Parameters:
                string (str): input string

            Returns:
                rt_string (str): none if string is empty, else input string
    '''
    rt_string = None
    if string is not None:
        string = str(string).strip()
        if (string == '--') or (string == '....') or (string == '') or (string == '-') or (string == '.'):
            rt_string = None
        else:
            rt_string = string
    return rt_string 

# SURFACE, USED_SURFACE
def remove_delimiter(string):
    '''
        Remove delimiter Ex: 1.500.000

            Parameters:
                string (str): crawled value

            Returns:
                rt_str (str): string has convert to float format
    '''
    rt_str = None
    if string is not None:
        string = string.replace(' ','').strip()
        if string.startswith(".") or string.startswith(","):
            string = string[1:]
        if string.endswith(".") or string.endswith(","):
            string = string[:-1]
        # 2.029,7
        if (string.count(',') ==1):
            if (re.findall(r'\d+\.\d{3}[,]',string)):
                string = re.sub("\.","",string)
        if (string.count('.') ==1):
            # 2,029.7
            if (re.findall(r'\d+[,]\d{3}[.]',string)):
                string = re.sub(",","",string)
            # 1.799 => 1799, not 0.799 => 799
            elif (re.findall(r'\d+\.\d{3}$',string)) and (not string.startswith("0")):
                string = re.sub("\.","",string)
        # 12,000,000 - 2,029,123.7
        if (string.count(',') >1):
            string = re.sub(",","",string)
        # 12.000.000
        if (string.count('.') >1):
            string = re.sub("\.","",string)
        # 1,029
        if (string.count(',') ==1) and (string.count('.') == 0):
            string = re.sub(",",".",string)
    return string

def handle_exponent(sf):
    '''
        Solve cases 1e3 = 10000

            Parameters:
                sf (str): string with exponent

            Returns:
                v (float): value after handle exponent
    '''
    if sf is None:
        return None
    else:
        sf = str(sf).lower().replace("&#x2b;","+").replace('e-','e*')
        pattern = ["-"]
        for i in pattern:
            if (re.search(i, str(sf))):
                sf_range = str(sf).split(i)
                sf = sf_range[len(sf_range)-1]
        if (sf.find("e") == -1):
            v = sf
        else:
            t = sf.split("e")
            m = t[1].replace('*','-')
            v = float(t[0]) * (10**int (m))
        return v

def get_surface_in_m2(surface,surface_unit):
    '''
        Calculate surface in m2

            Parameters:
                surface (str): surface calculated by any unit
                surface_unit (str): unit of the surface

            Returns:
                sf_m2 (float): surface calculated by m2
    '''
    sf_m2 = 0
    surface = check_empty(surface)
    surface_unit = check_empty(surface_unit)
    # check surface, surface_unit not null 
    if (surface is not None and surface_unit is not None):
        surface = unidecode(str(surface))
        if ('-' in surface):
            s = surface.split('-')
            surface = s[len(s)-1]
        surface = remove_delimiter(surface)
        surface_unit = unidecode(str(surface_unit))
        sf = surface

        if (not re.search(r'[a-zA-Z]', str(surface))):
            surface = handle_exponent(surface)
            surface = float(surface)
            surface_unit = surface_unit.lower()
            surface_unit = surface_unit.replace(" ","")
            if (("hecta" in surface_unit) or ("hec" in surface_unit) or ("ha" in surface_unit)):
                sf_m2 = float(float(surface)*10000)
            elif ("m2" in surface_unit):
                sf_m2 = float(surface)
    return sf_m2

def get_surface_original_in_m2(string):
    '''
        Calculate surface origin in m2

            Parameters:
                string (str): surface containing surface units

            Returns:
                surface_in_m2 (float): surface calculated by m2
    '''
    surface_in_m2 = 0
    if (string):
        string = unidecode(str(string).lower())
        string = string.replace(" ","")
        ls_surface_unit = LS_SF_UNIT
        for x in ls_surface_unit:
            if (x in string):
                a = string.split(x)
                surface_unit = x
                surface = a[0]
                if (re.findall(r'[0-9]+',surface)):
                    surface_in_m2 = get_surface_in_m2(surface,surface_unit)
                break
    return surface_in_m2

# PRICE
def get_price_in_trieu(price,price_unit):
    '''
        Calculate price in trieu

            Parameters:
                price (str): price calculated in any unit
                price_unit (str): unit of the price

            Returns:
                pr (float): price calculated in trieu
    '''
    pr = 0
    price = check_empty(price)
    price_unit = check_empty(price_unit)    
    # check price not null
    if (price is not None and price_unit is not None):
        price = unidecode(str(price))
        price = remove_delimiter(price)
        price_unit = unidecode(str(price_unit))
        if (re.search(r'\d', str(price))):
            price = handle_exponent(price)
            try:
                price = float(price)
            except:
                return pr
            price_unit = price_unit.lower()
            price_unit = price_unit.replace(" ","").replace("ngu00e0n","ngan")

            if (("ty" in price_unit) or ("ti" in price_unit)):
                pr = float(price*1000)
            elif (("trieu" in price_unit) or ("tr" in price_unit)):
                pr = float(price)
            elif (("ngan" in price_unit) or ("nghin" in price_unit)):
                pr = float(price/1000)
            elif ("tram" in price_unit):
                pr = float(price/10000)
            elif ("usd" in price_unit):
                pr = float(price*DOLLAR_PRICE/1000000)
            elif ("cayvang" in price_unit):
                pr = float(price*GOLD_PRICE/1000000)
            elif (("dong" in price_unit) or ("d" in price_unit)): 
                pr = float(price/1000000)
    return pr

def get_price(price,price_unit,surface_in_m2):
    '''
        Calculate price in trieu if price unit is per m2

            Parameters:
                price (str): price calculated in any unit per m2
                price_unit (str): unit of the price
                surface_in_m2 (str): surface calculated in m2

            Returns:
                new_price (float): price calculated in trieu
    '''
    new_price = 0
    area_unit = ""
    pr_pattern = []
    area_pattern = LS_SF_UNIT
    price_pattern = LS_PR_UNIT
    price = check_empty(price)
    surface_in_m2 = check_empty(surface_in_m2)
    # check price, price_unit not null and surface_in_m2 not null
    if (price is not None and price.count(' ')<=3 and surface_in_m2 is not None):
        price = str(price).lower()
        price = price.replace("null","").replace("none","")
        price = unidecode(price).replace(" ","").replace('e-','e*')
        #print(price)

        price_unit = str(price_unit).lower()
        price_unit = price_unit.replace("null","").replace("none","")
        price_unit = unidecode(price_unit).replace(" ","")
        
        # price: 1 ty/thang, price_unit: ty/thang
        if (price_unit in price):
            combined_price = price
        # price: 600 trieu, price_unit:ty
        elif (not (re.findall(r'\d',price_unit)) and (re.findall(r'[a-z]$',price))):
            combined_price = price
        # price: 3 trieu/m2, price_unit: trieu
        elif (re.findall(r'/',price)):
            combined_price = price
        # price: 3, price_unit:ty800trieu
        else: 
            combined_price = price + price_unit
        
        # combine price: 45m2 or combine price: Đã bán
        if (re.findall(r'^\d+m2$',combined_price)) or (not re.findall(r'\d',combined_price)):
            combined_price = '0'

        # 26,5 tỷ, 200 triệu, Liên hệ # 100 triệu, Liên hệ
        if (re.findall(r',lienhe',combined_price)):
            combined_price = re.sub(",lienhe","",combined_price)

        combined_price = combined_price.lower().replace(" ","").replace("ngu00e0n","ngan").replace("mill","trieu").replace("bill","ty").replace("k","ngan").replace("tramnghin","tram")        
        if (re.findall(r'\d+[ ]?ng/m2$',combined_price)):
            combined_price = re.sub(r'ng/m2$',"ngan/m2",combined_price)
        if (re.findall(r'\d+[ ]?ng$',combined_price)):
            combined_price = re.sub(r'ng$',"ngan",combined_price)
        #print(combined_price)

        # 3.65 ty - 3.65 ty
        if ('-' in combined_price):
            spl = combined_price.split('-')
            combined_price = spl[len(spl)-1]

        # 3.6 ty . 3.65 ty
        if (re.findall(r'[a-z]\.\d+',combined_price)):
            spl = re.split(r'[a-z]\.',combined_price)
            combined_price = spl[len(spl)-1]

        # 3.6 ty , 3.65 ty
        if (re.findall(r'[a-z],\d+',combined_price)):
            spl = re.split(r'[a-z],',combined_price)
            combined_price = spl[len(spl)-1]

        arr = combined_price.split("/")
        amount_price = arr[0]
        unit_price = combined_price.replace(amount_price,'')

        # search price unit
        for pr in price_pattern:
            if pr in amount_price:
                arr = amount_price.split(pr)
                pr_pattern.append((arr[0],pr))
                amount_price = arr[1]

        #print("amount_price",amount_price)

        # case do not enough price pattern: 1 ty 100 or 1450
        if (amount_price):
            # 1 ty 100
            if (len(pr_pattern)>=1):
                exp = len(str(amount_price))
                refer_unit = pr_pattern[len(pr_pattern)-1][1]
                pr_pattern.append((float(amount_price)/10**exp,refer_unit))
            # 1450
            else:
                # 2.500.000/m2
                if (re.findall(r'000$',amount_price)):
                    pr_pattern.append((amount_price,"dong"))
                # 1450
                else:
                    pr_pattern.append((amount_price,"trieu"))

        # print("pr_pattern",pr_pattern)

        # calculate total price
        # N ty M trieu L tram D dong
        if (pr_pattern):
            for element in pr_pattern:
                new_price = new_price + get_price_in_trieu(element[0],element[1])

        # print(new_price)

        # search area unit
        for area in area_pattern:
            # /150m2
            if (re.findall("/\d+"+area,unit_price)):
                area_unit = area
                unit_price = unit_price.replace('m2','')
                base_amount = re.findall(r'\d+',unit_price)
                base_amount = float(base_amount[0])
                break
            # /m2, #/hecta
            elif (re.findall("/"+area,unit_price)):
                area_unit = area
                base_amount = 1
                break

        # calculate actual price 
        if (area_unit != ""):
            new_price = float(new_price)*float(surface_in_m2)/float(get_surface_in_m2(base_amount,area_unit))
        else:
            new_price = float(new_price)
    return new_price

# ALLEY_ACCESS, FRONTAGE
def get_val_with_m(text):
    '''
        convert values containing m to float. If string not in pattern => return 0

            Parameters:
                text (str): crawled value

            Returns:
                number (float): alley or frontage in float
    '''
    s = 0
    if text is not None:
        text = str(text)
        if ("-" in text):
            ar = text.split("-")
            text = ar[len(ar)-1]
        text = text.strip()
        if (re.findall(r'\d+\.\d{3}$',text)) or (re.findall(r'\d+\.\d{3}[,]',text)):
            text = text.replace('.','')
        text = text.strip().replace(' ','').replace(',','.')

        # 5m5
        if re.findall(r'^\d+m\d+$', text):
            s = text.replace('m','.')
        # 5.5m or 5m
        elif re.findall(r'^\d*[.]?\d+m$', text):
            s = re.findall(r'\d*[.]?\d+',text)
            s = s[0]
        # 5 
        elif re.findall(r'^\d*[.]?\d+$',text):
            s = text

        if str(s).startswith("."):
            s = s[1:]
    return float(s)

# NB_FLOORS
def get_nb_floors(text):
    '''
    Returns extract nb of floors

        Parameters:
            text(string): Detailed brief field of ads

        Returns:
            result (float): Extract nb of floors based on the following patterns:
                            1 trệt, 1 tầng thượng, 1 gác suốt + 3 lầu => 4
                            1 trệt, 1 lửng => 1.5
                            1 trệt, 1 lửng, 1 tầng thượng + 5 lầu => 6.5
                            1 trệt, 1 lửng, 1 tầng thượng, 1 gác suốt + 2 lầu => 3.5
                            1 trệt, 1 lửng, 1 tầng thượng, 1 áp mái + 4 lầu => 5.5
    '''
    if (text):
        text = text.lower()
        text = unidecode(text)
        text = text.replace('+', ',')
        result = 0.000000000
        tret = 1
        tang_thuong = 1
        gac_suot = 0
        ap_mai = 0
        lung = 0.5
        lau = 1
        text = text.split(',')
        for i in range(len(text)):
            pattern = r'\d+'
            number = re.search(pattern, text[i])
            if (number == None):
                return None
            number = number.group()
            number = int(number)
            if text[i].find('tret') >= 0:
                result = result + tret * number
            elif text[i].find("tang thuong") >= 0:
                result = result + tang_thuong * number
            elif text[i].find("gac suot") >= 0:
                result = result + gac_suot * number
            elif text[i].find("ap mai") >= 0:
                result = result + ap_mai * number
            elif text[i].find("lau") >= 0:
                result = result + lau * number
            elif text[i].find("lung") >= 0:
                result = result + lung * number
        return result
    return 0

# DEALER_TEL
def limit_characters(string,number):
    '''
        Truncate string to string has fixed number length

            Parameters:
                string (str): crawled value
                number (int): fixed number length

            Returns:
                rt_string (str): string truncated to fixed number length
    '''
    rt_string = string
    if (string is not None):
        len_utf8 = len(string.encode('utf-8'))
        if (len_utf8 > number):
            rt_string = string[0:int(len(string)/len_utf8*number)]
    return rt_string

def split_tel(tel):
    '''
        Convert multi telephone to one

            Parameters:
                tel (str): crawling telephone
                    
            Returns:
                tel_return (str): telephone splited remain the first one
    '''
    tel_return = None
    pattern = ["-",";","/"," "]
    if (tel is not None):
        if not (re.findall(r'\d{10}[ ]',tel)):
            tel = tel.replace(" ","")
        if (re.search(r'XXX', str(tel))):
            tel_return = None
        elif (re.search(r'\d', str(tel))):
            tel_return = replace_characters(str(tel),[",","."],"")
            for p in pattern:
                if (re.search(p, str(tel_return))):
                    tel_array = str(tel_return).split(p)
                    tel_return = tel_array[0]
                    break
            tel_return = limit_characters(tel_return,20)
    return tel_return

# DEALER_JOIN_DATE
def count_days(date_now, str_date):
    '''
    Returns date before a period

        Parameters:
            date_now (datetime)
            str_date (str): a period

        Returns:
            result (datetime): raw splited address for after solving
    '''
    if (date_now is None) or (str_date is None):
        return None
    
    str_split = str_date.split(' ')
    years = None
    months = None
    days = None
    
    year, month, day = date_now.year, date_now.month, date_now.day
    
    num_days = 0
    
    if 'năm' in str_split:
        index = str_split.index('năm')
        years = int(str_split[index-1])
    if 'tháng' in str_split:
        index = str_split.index('tháng')
        months = int(str_split[index-1])
    if 'ngày' in str_split:
        index = str_split.index('ngày')
        days = int(str_split[index-1])
    
    month_current = month
    year_current = year

    if days is not None:
        num_days = days

    if (years is not None) and (months is None):
        month_ = month
        for i in range(years):
            list_months = []
            for i in range(12):
                month_ = month_ - 1
                if month_ <= 0:
                    list_months.append(month_ + 12)
                else:
                    list_months.append(month_)

            list_months = list_months[::-1]
            list_months.append(month_current)
            list_months = list_months[::-1]

            for m in list_months[:-1]:
                if m in [1,3,5,7,8,10,12]:
                    num_days = num_days + 31
                else:
                    if m in [4,6,9,11]:
                        num_days = num_days + 30
                    else:
                        if m - list_months[0] >= 0:
                            year_prev = year_current - 1
                        else:
                            year_prev = year_current

                        if (year_prev % 4 == 0 and not(year_prev % 100 == 0)) or (year_prev % 400 == 0):
                            num_days = num_days + 28
                        else:
                            num_days = num_days + 29
            
            month_current = list_months[-1]
            month_ = month_current
            year_current -= 1
            
        
    if (months is not None):
        month_ = month
        list_months_start = []
        pos = None
        for i in range(months):
            month_ = month_ - 1
            if month_ <= 0:
                list_months_start.append(month_ + 12)
            else:
                list_months_start.append(month_)
        
        list_months_start = list_months_start[::-1]
        list_months_start.append(month)
        list_months_start = list_months_start[::-1]
        
        for m in list_months_start[:-1]:
            if m in [1,3,5,7,8,10,12]:
                num_days = num_days + 31
            else:
                if m in [4,6,9,11]:
                    num_days = num_days + 30
                else:
                    if m - list_months_start[0] >=0:
                        year_prev = year - 1
                    else:
                        year_prev = year
                    
                    if (year_prev % 4 == 0 and not(year_prev % 100 == 0)) or (year_prev % 400 == 0):
                        num_days = num_days + 28
                    else:
                        num_days = num_days + 29
        
        month_current = list_months_start[-1]
        
        if month_current - list_months_start[0] >= 0:
            year_current = year - 1
        else:
            year_current = year
        
        if (years is not None):
            month_ = month_current
            for i in range(years):
                list_months = []
                for i in range(12):
                    month_ = month_ - 1
                    if month_ <= 0:
                        list_months.append(month_ + 12)
                    else:
                        list_months.append(month_)

                list_months = list_months[::-1]
                list_months.append(month_current)
                list_months = list_months[::-1]

                for m in list_months[:-1]:
                    if m in [1,3,5,7,8,10,12]:
                        num_days = num_days + 31
                    else:
                        if m in [4,6,9,11]:
                            num_days = num_days + 30
                        else:
                            if m - list_months_start[0] >= 0:
                                year_prev = year_current - 1
                            else:
                                year_prev = year_current

                            if (year_prev % 4 == 0 and not(year_prev % 100 == 0)) or (year_prev % 400 == 0):
                                num_days = num_days + 28
                            else:
                                num_days = num_days + 29
                                
                month_current = list_months[-1]
                month_ = month_current
                year_current -= 1

    return num_days

def solve_dealer_joined_date(date_now, str_date):
    '''
    Returns date before a period

        Parameters:
            date_now (datetime): yyyy-mm-dd
            str_date (string): period of time

        Returns:
            result (string): dd/mm/yyyy

    '''
    if (str_date is None):
        return None
    
    date = date_now - datetime.timedelta(count_days(date_now,str_date))
    return date

# REPORT
def report(dict_raw,dict_cleaned,site,source_mysql_host,source_mysql_db,des_mysql_host,des_mysql_db,total_time):
    COLUMNS = ['Created Date', 'Number of Raw Ads', 'Number of Cleaned Ads']
    '''
        Print Report after cleansing
            Parameters:
                dict_raw (str): dict sort by created date on raw data
                dict_cleaned (str): dict sort by created date on cleaned data
                site (str): sitename

            Returns:
                None
    '''
    print("*** REPORT ***")
    
    print("source_mysql_host=",source_mysql_host)
    print("source_mysql_db=",source_mysql_db)

    print("des_mysql_host=",des_mysql_host)
    print("des_mysql_db=",des_mysql_db)

    print("Site name = " + site)
    if (dict_cleaned):
        print("Site volumn = " + str(sum(dict_cleaned.values())))
    else:
        print("Site volumn = 0")
    print("Total time = " + total_time)


    t = PrettyTable(COLUMNS)
    
    if dict_raw:
        date_list = list(dict_raw.keys())
        date_list.sort()
        for date in date_list:
            date_show = date.strftime("%d/%m/%Y")
            num_raw = dict_raw[date]
            num_cleaned = 0
            if date in dict_cleaned:
                num_cleaned = dict_cleaned[date]
            t.add_row([date_show, num_raw, num_cleaned])
        print(t)
    else:
        print('Nothing to report')

# TRUNCATE STRING
def limit_characters(string,number):
    '''
        Truncate string to string has fixed number length

            Parameters:
                string (str): crawled value
                number (int): fixed number length

            Returns:
                rt_string (str): string truncated to fixed number length
    '''
    rt_string = string
    if (string is not None):
        len_utf8 = len(string.encode('utf-8'))
        if (len_utf8 > number):
            rt_string = string[0:int(len(string)/len_utf8*number)]
    return rt_string
