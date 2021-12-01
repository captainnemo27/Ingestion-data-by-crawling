from config.config_ import *
from create_dic import split_prefix
from libs.or_utils_ import replace_characters

# STREET, WARD, DISTRICT, CITY
## COMMON FUNCTIONS
def replace_all(text, dic):
    """
    Replace a string with another string
    
    Parameters
    ----------
    text: str
        original text
    dic: dictionary
        dictionary replace with key is the old string and value is the new string 
    
    Return
    ------
    str
        replaced text       
    """
    for i, j in dic.items():
        if (i.find(".") == -1):
            text = re.sub(r"\b{}\b".format(i), j, text)
        else:
            text = text.replace(' '+i, ' '+j+' ')
            text = text.replace(','+i, ' , '+j+' ')
    text = ' '.join(text.split())
    return text

def find_whole_word(string1, string2):
    """
    Find a word in a string

    Parameters
    ----------
    w: str
        original text

    Return
    ------
    boolean
        True: whether the word in string. Ex: 123 in 123 => True
        False: word not in string. Ex: 12 in 123 => False 
    """
    if re.search(r"\b" + re.escape(string1) + r"\b", string2):
        return True
    return False

def find_deli(string):
    '''
        Find the delimiter occurs most frequent 

            Parameters:
                string (str): string with one or many delimiters

            Returns:
                pattern (str): delimiter most frequent
    '''
    dic = {}
    for d in LS_DELIMITER:
        dot = string.count(d)
        dic[d] = dot
    dic_tuple = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    pattern = dic_tuple[0][0]
    count_pattern = dic_tuple[0][1]
    return pattern, count_pattern

def split_delimiter(string,pattern):
    '''
        Split string by delimiter

            Parameters:
                string (str): string with delimiter
                pattern (str): delimiter

            Returns:
                arr (arr): array splitted string components
    '''
    l = [x for x in LS_DELIMITER if (x != pattern) and (x!='.')]
    for x in l:
        string = string.replace(x,pattern)
    arr = string.split(pattern)
    arr = [x.strip() for x in arr if x != '']
    return arr

def check_start_with(string,ls_val):
    '''
        Check whether string start up prefix, for example: quan, huyen

            Parameters:
                string (str): string need to be checked
                ls_val (arr)): list prefix

            Returns:
                result (bool)): true if string start with one of element in ls_val, else false
    '''
    if (string):
        for val in ls_val:
            if (string.startswith(val+' ')):
                return True
    return False

def return_unicode(string,dic_current_string):
    '''
        Add accent for string

            Parameters:
                string (str): string need to be solved
                dic_current_string (str): dic string with key is string not accent and value is string with accent

            Returns:
                string (str): string after added accent
    '''
    a = string.split(' ')
    a = [x for x in a if x!='']
    rt_remain = ''
    for s in a:
        try:
            rt_remain = rt_remain + ' ' + str(dic_current_string[s])
        except:
            rt_remain = rt_remain + ' ' + s
    string = rt_remain.strip()
    return string

def ls_to_str(ls,deli):
    '''
        Convert list to string with seperate delimiter

            Parameters:
                ls (arr): list need to concat elements
                deli (str): delimiter

            Returns:
                string (str): string converted
    '''
    string = ''
    for i in ls:
        string = string + ' ' + deli + ' ' + i
    string = string.strip()[2:]
    return string

def replace_stick_synonym(text,deli=","):
    '''
        Seperate text with splited value and 0 before number. For example P07 => phuong 7

            Parameters:
                text (str): text need to be converted

            Returns:
                sentence (str): text after converted
    '''
    text = unidecode(text.lower()).strip()
    s = text.split(deli)
    sentence = ''
    for w in s:
        # print("word",w)
        w = w.strip()
        if (w.isdigit()):
            w = str(int(w))
        if (re.findall(r'^p[.]?\d+',w)) or (re.findall(r'^phuong\d+',w)):
            a = w.split(r'p')[1]
            b = re.findall(r'\d+',a)
            if (b):
                if len(str(int(b[0]))) <= 2:
                    if deli in w:
                        w = "phuong " + str(int(b[0])) + " " + deli
                    else:
                        w = "phuong " + str(int(b[0]))
        if (re.findall(r'^f[.]?\d+',w)):
            a = w.split(r'f')[1]
            b = re.findall(r'\d+',a)
            if (b):
                if len(str(int(b[0]))) <= 2: 
                    if deli in w:
                        w = "phuong " + str(int(b[0])) + " " + deli
                    else:
                        w = "phuong " + str(int(b[0]))
        if (re.findall(r'^q[.]?\d+',w)) or (re.findall(r'^quan\d+',w)):
            a = w.split(r'q')[1]
            b = re.findall(r'\d+',a)
            if (b):
                if len(str(int(b[0]))) <= 2: 
                    if deli in w:
                        w = "quan " + str(int(b[0])) + " " + deli
                    else:
                        w = "quan " + str(int(b[0]))
        if (re.findall(r'^\d+[,]?$',w)):
            if (',' in w):
                w = str(int(w[:-1])) + ' ,'
            else:
                w = str(int(w))   
        sentence = sentence + ' ' + deli + ' ' + w
    sentence = " ".join(sentence.split())
    if (sentence.startswith(deli)):
        sentence = sentence[1:]
    return sentence

def decode_synonym(string):
    '''
        Convert synonym to original form before looking up

            Parameters:
                string (str): string need to be converted

            Returns:
                string (str): string after converted
    '''
    if (string):
        for key in DIC_SYNONYM:
            string = replace_characters(string,DIC_SYNONYM[key],' '+key+' ')
        string = replace_all(string,DIC_REPLACE)
        string = " ".join(string.split())
    return string

def standard_output(dic_return,level,dic_current_string):
    '''
        Add accent to output hs_num, street, ward, district, city 

            Parameters:
                dic_return (dictionary): dictionary having hs_num, street, ward, district, city
                dic_current_string (str): dictionary having string with accent

            Returns:
                dic_return (dictionary): dictionary having hs_num, street, ward, district, city having accent
    '''
    string = dic_return.get(level)
    if (string) and (isinstance(string, tuple)):
        string = string[0]
    elif (string):
        # decode synonym
        for key in DIC_SYNONYM:
            if key in string:
                for x in DIC_SYNONYM[key]:
                    if (x in dic_current_string.keys()):
                        string = string.replace(key,x)
                        break
        # decode unidecode
        string = return_unicode(string,dic_current_string)
        for key in DIC_PREFIX:
            string = string.replace(key,DIC_PREFIX[key])
    else:
        string = None
    return string

## FUNCTION LOOKUP
def gen_dic_lk(level,dic_return):
    '''
        Generate dictionary lookup. If found city => look up in dic[city]

            Parameters:
                level (int): 1: city, 2: district, 3: ward, 4: street
                dic_return (dictionary): dictionary having hs_num, street, ward, district, city

            Returns:
                dic (dictionary): dictionary look up by level
    '''
    dic = None
    if (level == 1):
        dic = DIC_CITY
    if (level == 2):
        tp_city = dic_return.get(1)
        # if found city
        if (tp_city):
            city_prefix = tp_city[1]
            city_val = tp_city[2]
            try:
                dic = DIC_CITY_DISTRICT_WARD[city_prefix][city_val]
            except:
                dic = None
        # if not found city
        else:
            dic = DIC_DISTRICT
    if (level == 3):
        tp_city = dic_return.get(1)
        tp_district = dic_return.get(2)
        # if found city and district
        if (tp_city) and (tp_district):
            try:
                dic = DIC_CITY_DISTRICT_WARD[tp_city[1]][tp_city[2]][tp_district[1]][tp_district[2]]
            except:
                dic = None
        # if found city and not found district
        elif (tp_city) and (not tp_district):
            try:
                dic = DIC_CITY_WARD[tp_city[1]][tp_city[2]]
            except:
                dic = None
        # # if found district and not city
        # elif (tp_district) and (not tp_city):
        #     city,city_pref,city_val = predict_city_from_district(tp_district[0])
        #     try:
        #         dic = DIC_CITY_DISTRICT_WARD[city_pref][city_val][tp_district[1]][tp_district[2]]
        #         dic_return[1] = (city,city_pref,city_val)
        #     except:
        #         dic = None
        # if not found city and district
        else:
            dic = DIC_WARD
    if (level == 4):
        tp_city = dic_return.get(1)
        tp_district = dic_return.get(2)
        # if found city and district
        if (tp_city) and (tp_district):
            try:
                dic = DIC_CITY_DISTRICT_STREET[tp_city[1]][tp_city[2]][tp_district[1]][tp_district[2]]
            except:
                dic = None
        # if found city and not found district
        elif (tp_city) and (not tp_district):
            try:
                dic = DIC_CITY_STREET[tp_city[1]][tp_city[2]]
            except:
                dic = None
        # # if found district and not city
        # elif (tp_district) and (not tp_city):
        #     city,city_pref,city_val = predict_city_from_district(tp_district[0])
        #     try:
        #         dic = DIC_CITY_DISTRICT_STREET[city_pref][city_val][tp_district[1]][tp_district[2]]
        #         dic_return[1] = (city,city_pref,city_val)
        #     except:
        #         dic = None
        # if not found city and district
        else:
            dic = DIC_STREET
    return dic

def gen_search_str(level,prefix,k):
    '''
        Generate search string. Some cases search string is prefix and val, some cases only val

            Parameters:
                level (int): 1: city, 2: district, 3: ward, 4: street
                prefix (str): prefix in dictionary look up. Example: tinh, thanh pho
                k (str): val in dictionary look up. Example: ho chi minh

            Returns:
                search_str (str): search string
    '''
    if (str(k).isdigit()):
        search_str = prefix + ' ' + unidecode(str(k).lower())
    elif (level == 4) and (prefix != 'duong'):
        search_str = prefix + ' ' + unidecode(str(k).lower())
    # 288/5E
    elif (level == 4) and (prefix == 'duong') and (len(str(k)) <=3) and ("/" not in str(k)):
        search_str = prefix + ' ' + unidecode(str(k).lower())
    # huyen ninh hoa, tinh khanh hoa = thi xa ninh hoa, tinh khanh hoa
    # thi tran khanh vinh, tinh khanh hoa
    # elif (level in [2,3]) and ((str(prefix).count(' ') == 1) and (str(prefix) not in ['thanh pho'])):
    # elif (level in [3]) and ((str(prefix).count(' ') == 1)):
    #     search_str = prefix + ' ' + unidecode(str(k).lower())
    elif (level in [1,2,3,4] and (str(k).count(' ') == 0)):
        search_str = prefix + ' ' + unidecode(str(k).lower())
    else:
        search_str = unidecode(str(k).lower())
    return search_str

def look_up(level,dic_return,string,deli=','):
    '''
        Look up value from dictionary in string having delimiters

            Parameters:
                level (int): 1: city, 2: district, 3: ward, 4: street
                dic_return (dictionary): dictionary having hsnum, street, ward, district, city
                string (str): string need to be looked up
                deli (str): delimiter

            Returns:
                dic_return (dictionary): dictionary having updated hsnum, street, ward, district 
                flag (bool): if flag = 1, find value in string else not found
    '''
    #print("string",string)
    flag = 0
    dic = gen_dic_lk(level,dic_return)
    if (dic):
        for prefix in dic.keys():
            ls = dic[prefix]
            for k in ls:
                search_str = gen_search_str(level,prefix,k)
                if find_whole_word(search_str,str(string).lower()):
                    # format value
                    val = DIC_PREFIX[prefix] + ' ' + str(k)
                    # add value to ls_return
                    dic_return[level] = (val,prefix,str(k))
                    # replace found string in dic_return[5]
                    a = dic_return[5].split(deli)
                    b = a[::-1]
                    if (a):
                        x = ''
                        # find index found
                        for i in range(0,len(b)):
                            if (b[i].strip() == string.strip()):
                                b.remove(b[i])
                                break
                        a = b[::-1]
                        # edit search string
                        for i in range(0,len(a)):
                            if (re.findall(r'[a-z0-9]',a[i])):
                                x = x + ' ' + deli + ' ' + a[i].strip()
                        dic_return[5] = x.strip()[1:]
                    else:
                        dic_return[5] = ''
                    # save remain string after found
                    string_after = string.replace(unidecode(str(k).lower()),'').replace(unidecode(str(prefix).lower()),'').strip()
                    level_ext = str(level) + "_extend"
                    if (re.findall(r'[a-z0-9]',string_after)):
                        dic_return[level_ext] = string_after
                    flag = 1
                    break
            if (flag == 1):
                break
    return dic_return,flag

def lookup_extend(level,dic_return,string):
    '''
        Look up value from dictionary in string not having delimiters

            Parameters:
                level (int): 1: city, 2: district, 3: ward, 4: street
                dic_return (dictionary): dictionary having hsnum, street, ward, district, city
                string (str): string need to be looked up

            Returns:
                dic_return (dictionary): dictionary having updated hsnum, street, ward, district, city
                flag (bool): if flag = 1, find value in string else not found
    '''
    flag = 0
    dic = gen_dic_lk(level,dic_return)
    if (dic):
        for prefix in dic.keys():
            ls = list(dic[prefix])
            for k in ls:
                search_str = gen_search_str(level,prefix,k)
                if find_whole_word(search_str,str(string).lower()):
                    # format value
                    val = DIC_PREFIX[prefix] + ' ' + str(k)
                    # add value to ls_return
                    dic_return[level] = (val,prefix,str(k))
                    # replace found string in dic_return[5]
                    string = string.replace(search_str,'').strip()
                    flag = 1
                    break
            if (flag == 1):
                break
    return string,dic_return

## FUNCTION SPLIT ADDRESS
def split_address_deli(dic_return,deli):
    '''
        Split address string having delimiters

            Parameters:
                dic_return (dictionary): dictionary having hsnum, street, ward, district, city
                deli (str): delimiter

            Returns:
                dic_return (dictionary): dictionary having updated hsnum, street, ward, district, city
    '''
    ls_comp = split_delimiter(dic_return[5],deli)

    # FIND LEVEL 1
    for i in range(0,len(ls_comp)):
        # if tim thay don vi khac bac => continue
        if (check_start_with(ls_comp[i],set(list(LS_LEVEL_DISTRICT + LS_LEVEL_WARD + LS_LEVEL_STREET)) - set(['thanh pho']))):
            continue
        else:
            dic_return,flag_1 = look_up(1,dic_return,ls_comp[i],deli)
            if (flag_1 == 1):
                break
    # print("1",dic_return)
            
    # FIND LEVEL 2
    ls_comp = dic_return[5].split(deli)
    for i in range(0,len(ls_comp)):
        # if tim thay don vi khac bac => continue
        if (check_start_with(ls_comp[i],set(list(LS_LEVEL_CITY + LS_LEVEL_WARD + LS_LEVEL_STREET)) - set(['thanh pho']))):
            continue
        else:
            dic_return,flag_2 = look_up(2,dic_return,ls_comp[i],deli)
            if (flag_2 == 1):
                break
    # print("2",dic_return)

    # FIND LEVEL 3
    ls_comp = dic_return[5].split(deli)
    for i in range(0,len(ls_comp)):
        # if tim thay don vi khac bac => continue
        if (check_start_with(ls_comp[i],set(list(LS_LEVEL_DISTRICT + LS_LEVEL_CITY + LS_LEVEL_STREET)))):
            continue
        else:
            dic_return,flag_3 = look_up(3,dic_return,ls_comp[i],deli)
            if (flag_3 == 1):
                break
    # print("3",dic_return)

    # FIND LEVEL 4
    ls_comp = dic_return[5].split(deli)
    # if found city and district    
    for i in range(0,len(ls_comp)):
        # if tim thay don vi khac bac => continue
        if (check_start_with(ls_comp[i],set(list(LS_LEVEL_DISTRICT + LS_LEVEL_WARD + LS_LEVEL_CITY)))):
            continue
        else:
            dic_return,flag_4 = look_up(4,dic_return,ls_comp[i],deli)
            if (flag_4 == 1):
                break
    # print("4",dic_return)

    str_found_level = [dic_return.get(x) for x in dic_return.keys() if ('extend') in str(x)]
    str_found_level = str_found_level[::-1]
    if (str_found_level):
        str_found_level = str_found_level[0]
    else:
        str_found_level = ''
    
    for x in LS_PREFIX:
        if (str_found_level.lower() == x.lower()):
            str_found_level = None
            break

    if (not dic_return.get(4)):
        if (dic_return.get(5)):
            temp = dic_return.get(5).split(deli)
            temp = temp[::-1]
            dic_return[4] = temp[-1].strip()
            dic_return[5] = ls_to_str(temp[0:len(temp)-1],deli)
        else:
            dic_return[4] = str_found_level
    elif (dic_return.get(4)) and (not (dic_return.get(5))):
        dic_return[5] = str_found_level
    elif (dic_return.get(4)) and (dic_return.get(5)):
        a = dic_return[5].split(deli)
        str_found_level = ls_to_str(a[::-1],deli)
        dic_return[5] = str_found_level

    return dic_return

def split_address_no_deli(dic_return):
    '''
        Split address string not having delimiters

            Parameters:
                dic_return (dictionary): dictionary having hsnum, street, ward, district, city
                
            Returns:
                dic_return (dictionary): dictionary having updated hsnum, street, ward, district, city
    '''

    str_found_level = dic_return[5]

    # FIND LEVEL 1
    str_found_level,dic_return = lookup_extend(1,dic_return,str_found_level)

    # FIND LEVEL 2
    if (1 in dic_return):
        str_found_level,dic_return = lookup_extend(2,dic_return,str_found_level)

    # FIND LEVEL 3
    if (1 in dic_return) and (2 in dic_return):
        str_found_level,dic_return = lookup_extend(3,dic_return,str_found_level)

    # FIND LEVEL 4
    if (1 in dic_return) and (2 in dic_return) and (3 in dic_return):
        str_found_level,dic_return = lookup_extend(4,dic_return,str_found_level)

    # nguyen tri phuong => nguyen tri
    for x in DIC_PREFIX:
        if (x.count(' ')>=1):
            if (str_found_level.endswith(x)):
                str_found_level = str_found_level[0:(len(str_found_level)-len(x))].strip()

    if (not dic_return.get(4)):
        dic_return[4] = str_found_level
        dic_return[5] = None
    else:
        dic_return[5] = str_found_level
    
    return dic_return

def pre_process_address(full_address):
    '''
        Preprocess full address

            Parameters:
                full_address (str)): full address before pre_processing                
            Returns:
                full_address (str): full address after pre_processing
                dic_current_string (dictionary): dictionary of word in text
    '''
    # DECODE
    full_address = html.unescape(full_address)
    full_address = full_address.replace("&#xE8;","è").replace("--","")
    full_address = re.sub(r'Đường \d+[.,][ ]?\d+m','',full_address)
    full_address = re.sub(r'đường \d+[.,][ ]?\d+m','',full_address)
    if (full_address.startswith('.')):
        full_address = full_address[1:]
    if (full_address.endswith('.')):
        full_address = full_address[:-1]
    full_address = re.sub(r'[.]{3}',' ',full_address)
    # print(full_address)
    
    # CONVERT DIC CURRENT STRING
    dic_current_string = {k: k for k in LS_DELIMITER}
    a = replace_characters(full_address,LS_DELIMITER,' ')
    a = a.split(' ')
    for s in a:
        if (unidecode(s.lower()) not in dic_current_string):
            dic_current_string[unidecode(s.lower())] = s
    
    # PRE PROCESS
    full_address = unidecode(full_address.strip().lower())
    full_address = decode_synonym(" " + full_address)

    return full_address,dic_current_string

def split_address(full_address):
    '''
        Look up value from dictionary in string having delimiters

            Parameters:
                full_address (str): string need to be splitted
                
            Returns:
                dic_return (dictionary): dictionary having hsnum, street, ward, district, city
    '''       
    dic_return = {}
    if (full_address):
        # PRE_PROCESS ADDRESS
        full_address,dic_current_string = pre_process_address(full_address)
        
        # SPLIT ADDRESS BASED ON DELIMITER
        deli,count_deli = find_deli(full_address)
        full_address = replace_stick_synonym(full_address,deli)
        # print(full_address)

        if (count_deli == 1 and deli == '-' and re.findall(r'\d+[ ]?-[ ]?\d+',full_address)):
            spl_address = [full_address]
        # elif (count_deli == 1 and deli != ','):
        #     full_address = full_address.replace(deli,"")
        #     spl_address = split_delimiter(full_address,deli)
        else:
            spl_address = split_delimiter(full_address,deli)
        ls_comp = [x.strip() for x in spl_address]
        ls_comp = ls_comp[::-1]
        cnt = len(ls_comp)
        ls_comp = ['thanh pho vinh' if (re.findall(r'^vinh$',x.strip())) else x for x in ls_comp]
        ls_comp = ['thanh pho vinh' if (re.findall(r'^huyen vinh$',x.strip())) else x for x in ls_comp]
        ls_comp = ['thanh pho pleiku' if (re.findall(r'^pleiku$',x.strip())) else x for x in ls_comp]
        ls_comp = ['thanh pho pleiku' if (re.findall(r'^huyen pleiku$',x.strip())) else x for x in ls_comp]
        ls_comp = ['thanh pho hue' if (re.findall(r'^huyen hue$',x.strip())) else x for x in ls_comp]
        ls_comp = ['co nhue 1' if (re.findall(r'^co nhue$',x.strip())) else x for x in ls_comp]
        f = 0
        for x in ls_comp:
            if (x=='thua thien hue'):
                f = 1
                break
        if (f == 0):
            ls_comp = ['thua thien hue' if (re.findall(r'^hue$',x.strip())) else x for x in ls_comp]
        else:
            ls_comp = ['thanh pho hue' if (re.findall(r'^hue$',x.strip())) else x for x in ls_comp]
        f = 0
        ls_btl = DIC_CITY_DISTRICT_WARD['thanh pho']['Hà Nội']['quan']['Bắc Từ Liêm']['phuong']
        ls_btl = [unidecode(x.lower()) for x in ls_btl] + ['co nhue']
        ls_ntl = DIC_CITY_DISTRICT_WARD['thanh pho']['Hà Nội']['quan']['Nam Từ Liêm']['phuong']
        ls_ntl = [unidecode(x.lower()) for x in ls_ntl] + ['my dinh']
        for x in ls_comp:
            if (x in ls_btl):
                f = 1
                break
            elif (x in ls_ntl):
                f = 2
                break
        if (f == 1):
            ls_comp = ['bac tu liem' if (re.findall(r'^tu liem$',x.strip())) else x for x in ls_comp]
        elif (f == 2):
            ls_comp = ['nam tu liem' if (re.findall(r'^tu liem$',x.strip())) else x for x in ls_comp]
        full_address = ls_to_str(ls_comp,deli)
        dic_return = {5:full_address}
        
        # IF HAVE DELIMTER
        if (cnt > 1):
            dic_return = split_address_deli(dic_return,deli)

        # IF DO NOT HAVE DELIMITER
        if (cnt == 1):
            dic_return = split_address_no_deli(dic_return)

        #print("dic_return",dic_return)
    
        # ADD ACCENT FORMAT
        for k in dic_return:
            dic_return[k] = standard_output(dic_return,k,dic_current_string)

    # # IF NOT FOUND CITY -> RETURN NONE
    # if (dic_return.get(1)):
    #     return (dic_return.get(1),dic_return.get(2),dic_return.get(3),dic_return.get(4),dic_return.get(5))
    # else:
    #     return None,None,None,None,None
    return (dic_return.get(1),dic_return.get(2),dic_return.get(3),dic_return.get(4),dic_return.get(5))

## FUNCTION STANDARDLIZE ADDRESS
def predict_city_from_district(district):
    '''
        Predict city from district

            Parameters:
                district (str): district including prefix and val

            Returns:
                city (str): city predicted 
                city_pref (str): prefix of city predicted
                city_val (str): value of city predicted
    '''
    # load vn_tinh_huyen
    vn_tinh_huyen = pd.read_csv('json/data_vn_tinh_huyen.csv')
    df = vn_tinh_huyen[vn_tinh_huyen['district']==district]
    ls_city = list(df['city'].unique())
    if (ls_city):
        city = ls_city[0]
        d = df[df["city"]==city]
        city_pref = d.iloc[0]["city_prefix"]
        city_val = d.iloc[0]["city_val"]
        return city,city_pref,city_val
    return None,None,None

def predict_district_from_city_ward(city,ward):
    '''
        Predict district from city, ward

            Parameters:
                city (str): city including prefix and val
                ward (str): ward including prefix and val

            Returns:
                district (str): district predicted 
                district_pref (str): prefix of district predicted
                district_val (str): value of district predicted
    '''
    # load vn_tinh_huyen
    vn_tinh_huyen = pd.read_csv('json/data_vn_tinh_huyen.csv')
    df = vn_tinh_huyen[(vn_tinh_huyen['city']==city) & (vn_tinh_huyen['ward']==ward)]
    ls_district = list(df['district'].unique())
    if (ls_district):
        district = ls_district[0]
        d = df[df["district"]==district]
        district_pref = d.iloc[0]["district_prefix"]
        district_val = d.iloc[0]["district_val"]
        return district,district_pref,district_val
    return None,None,None

def standardize_crawling(string,level,dic):
    '''
        Standard format crawling value

            Parameters:
                string (str): crawling values
                level (int): 1: city, 2: district, 3: ward, 4: street

            Returns:
                string (str): string after standardized based on level
    '''
    if (string is not None):
        # if (level == 1):
        #     dic = DIC_CITY
        # elif (level == 2):
        #     dic = DIC_DISTRICT
        # elif (level == 3):
        #     dic = DIC_WARD
        # elif (level == 4):
        #     dic = DIC_STREET
        for prefix in dic:
            ls_val = dic[prefix]
            for val in ls_val:
                val = str(val)
                # standard_str = unidecode(val.lower())
                standard_str = gen_search_str(level,prefix,val)
                find_str = unidecode(string.lower())
                if find_whole_word(standard_str,find_str):
                    actual_val = DIC_PREFIX[prefix] + ' ' + val
                    return actual_val,prefix,val
    return None,None,None

def check_level_address(city,district,ward):
    '''
        Check ward in district, district in city

            Parameters:
                city (str): city including prefix and val
                district (str): district including prefix and val
                ward (str): ward including prefix and val 

            Returns:
                city_check (str): city after checked level 
                district_check (str): district after checked level
                ward_check (str): ward after checked level
    '''
    if (city) and (unidecode(city.lower()) in DIC_COMBINE_LEVEL):
        city_ = unidecode(city.lower())
        if (district) and (unidecode(district.lower()) in DIC_COMBINE_LEVEL[city_]):
            district_ = unidecode(district.lower())
            if (ward) and (unidecode(ward.lower()) in DIC_COMBINE_LEVEL[city_][district_]):
                return city,district,ward
            else:
                return city,district,None
        else:
            return city,None,None
    else:
        return None,None,None
            
def standardize_address(full_address,crw_city,crw_district,crw_ward,crw_street):
    '''
        Standardize crawling full_address, city, district, ward and street

            Parameters:
                full_address (str): full address crawling
                crw_city (str): city crawling
                crw_distirct (str): district crawling
                crw_ward (str): ward crawling
                crw_street (str): street crawling

            Returns:
                city (str): city standardized
                district (str): district standardized
                ward (str): ward standardized
                street (str): street standardized
    '''
    city = None
    district = None
    ward = None
    street = None
    hsnum = None
    full_address_org = full_address
    
    # SPLIT ADDRESS
    if (not crw_city) or (not crw_district) or (not crw_ward) or (not crw_street):
        city,district,ward,street,hsnum = split_address(full_address)

    # DECODE CRAWLING, REMOVE PREFIX, FORMAT CRAWLING
    if (crw_city):
        # print("crw_city:",crw_city,end="\t")
        crw_city = pre_process_address(crw_city)[0]
        crw_city = decode_synonym(crw_city.lower())
        crw_city = split_prefix(crw_city,LS_LEVEL_CITY_ORIGINAL)[0][1]
        crw_city,city_prefix,city_name = standardize_crawling(crw_city,1,DIC_CITY)
    
    if (crw_district):
        # print("crw_district:",crw_district,end="\t")
        crw_district = pre_process_address(crw_district)[0]
        crw_district = decode_synonym(crw_district.lower())
        crw_district_1 = split_prefix(crw_district,LS_LEVEL_DISTRICT_ORIGINAL)[0][1]
        if (crw_district_1.count(' ') != 0):
            crw_district = crw_district_1
        if (unidecode(crw_district_1.lower()) in ["hue","vinh","pleiku"]):
            crw_district = "Thành phố " + crw_district_1
        if ("-" in crw_district_1):
            crw_district = crw_district_1.replace("-"," ").strip()
        if (crw_city):
            dic = DIC_CITY_DISTRICT_WARD[city_prefix][city_name]
        else:
            dic = DIC_DISTRICT
        crw_district,district_prefix,district_name = standardize_crawling(crw_district,2,dic)

    if (crw_ward):
        # print("crw_ward",crw_ward,end="\t")
        crw_ward = pre_process_address(crw_ward)[0]
        crw_ward = decode_synonym(crw_ward.lower())
        crw_ward_1 = split_prefix(crw_ward,LS_LEVEL_WARD_ORIGINAL)[0][1]
        if (crw_ward_1.count(' ') != 0):
            crw_ward = crw_ward_1
        if (crw_city) and (crw_district):
            dic = DIC_CITY_DISTRICT_WARD[city_prefix][city_name][district_prefix][district_name]
        elif (crw_city):
            dic = DIC_CITY_WARD[city_prefix][city_name]
        else:
            dic = DIC_WARD
        crw_ward,ward_prefix,ward_name = standardize_crawling(crw_ward,3,dic)

    # RETRY IF SPLIT CITY NULL
    if (full_address_org) and (crw_city) and (not city):
        full_address = pre_process_address(full_address_org)[0]
        deli,count_deli = find_deli(full_address)
        if (count_deli == 0):
            full_address = full_address_org + ' ' + crw_city
        else:
            full_address = full_address_org + ' ' + deli + ' ' + crw_city
        city,district,ward,street,hsnum = split_address(full_address)

    if (crw_city):
        city = crw_city
    if (crw_district) and (crw_city):
        district = crw_district
    if (crw_ward) and (crw_city):
        ward = crw_ward
    if (crw_street):
        street = crw_street
        
    # # PREDICT CITY
    # # district = Tân Bình -> city = Đồng Nai
    # if (district) and (not city):
    #     city,city_pref,city_val = predict_city_from_district(district)
    
    # PREDICT DISTRICT
    if (city) and (ward) and (not district):
        district,district_pref,district_val = predict_district_from_city_ward(city,ward)
    
    # # CHECK LEVEL
    if (city):
        city,district,ward = check_level_address(city,district,ward)

    return city,district,ward,street,hsnum

def map_street(street):
    '''
        Map wrong format street with street

            Parameters:
                street (str): street need to solve

            Returns:
                rt_street (str): if street in key of DIC_FORMAT_STREET, return value else return street
    '''
    rt_street = ""
    for x in DIC_FORMAT_STREET:
        if (street == x):
            rt_street = DIC_FORMAT_STREET[x]
        else:
            rt_street = street
    return rt_street

# STANDARD STREET AND HOUSE NUMBER
def standardize_street_hs(street,house_num):
    '''
        Standardize street, house number

            Parameters:
                street (str): split street from full address
                house_num (str): split house_number from full address

            Returns:
                street (str): format street
                hs (str): house number split from street
    '''
    hs = None
    if (street):
        flag = 0
        street = street.lower().strip()
        if (re.findall(r'^tl[ ]?\d+$',street)) or (re.findall(r'^đường tl[ ]?\d+$',street)) or (re.findall(r'^đường tỉnh lộ[ ]?\d+$',street)):
            street = street.replace('tl','tỉnh lộ ').replace('đường','')
        if (re.findall(r'^tx[ ]?\d+$',street)):
            street = street.replace('tx','thạnh xuân ')
        if (re.findall(r'^ht[ ]?\d+$',street)):
            street = street.replace('ht','hiệp thành ')
        if (re.findall(r'^xtt[ ]?\d+$',street)):
            street = street.replace('xtt','xuân thới thượng ')
        if (re.findall(r'^tth[ ]?\d+$',street)):
            street = street.replace('tth','tân thới hiệp ')
        # if have ls_remove -> return None
        for x in LS_NOISE:
            if x in street:
                return None,None
        # Số 1A -> return hs
        if (re.findall(r'^\d+[/0-9]*[a-z]*$',street)) \
        or ((re.findall(r'^số \d+[/0-9]*[a-z]*$',street))) \
        or ((re.findall(r'^hẻm \d+[/0-9]*[a-z]*$',street))) \
        and (hs == None):
            hs = street.title()
            street = None
            return street,hs
        # If contain Đường
        for x in LS_PREFIX_STREET_ORIGINAL:
            x = x + ' '
            if x in street:
                ar = street.split(x)
                hs = ar[0].strip()
                t = ar[1].strip()
                if (t != ''):
                    street = street.replace(hs,"").strip()
                else:
                    street = None
                flag = 1
                break
        if (flag == 0):
            # 20 tháng 10 = 20/10 -> look up dic synonym
            for key in DIC_SYNONYM_STREET:
                street = replace_characters(street,DIC_SYNONYM_STREET[key],' '+key+' ')
            for x in LS_PREFIX_STREET:
                if x in street:
                    ar = street.split(x)
                    hs = ar[0].strip()
                    street = street.replace(hs,"").strip()
            # 130 au co
            if (re.findall(r'^\d+[/0-9]*[a-z]*',street)) \
            or ((re.findall(r'^số \d+[/0-9]*[a-z]*',street))) \
            or ((re.findall(r'^hẻm \d+[/0-9]*[a-z]*',street))):
                s = re.findall(r'\d+[/0-9]*[a-z]*',street)
                hs = s[0].strip()
                if ('số' in street):
                    hs = 'số ' + hs
                if ('hẻm' in street):
                    hs = 'hẻm' + hs
                street = street.replace(hs,"").strip()
            street_org = street
            # 20/10 = Đường 20/10 look up dic street
            street,street_prefix,street_name = standardize_crawling(street,4,DIC_STREET)
            #if (not street):
                #street = street_org
        if (hs):
            hs = hs.title()
        elif (hs == ''):
            hs = None
        if (street):
            if (street.startswith('phố ')):
                ar = street.split(' ')
                street = 'đường '
                for i in range(1,len(ar)):
                    street = street + ' ' + ar[i] 
                    street = " ".join(street.split())
            if (re.findall(r'^đường \d+$',street)):
                name = re.findall(r'\d+',street)
                street = 'đường số ' + name[0]
            street = street.title().strip()
            if (not hs) and (house_num):
                if (re.findall(r'^\d+[/0-9]*[a-z]*',house_num)) \
                or ((re.findall(r'^số \d+[/0-9]*[a-z]*',house_num))) \
                or ((re.findall(r'^hẻm \d+[/0-9]*[a-z]*',house_num))):
                    s = re.findall(r'\d+[/0-9]*[a-z]*',house_num)
                    hs = s[0].strip()
                    if ('số' in street):
                        hs = 'số ' + hs
                    if ('hẻm' in street):
                        hs = 'hẻm' + hs
                    hs = hs.title()
        elif (street == ''):
            street = None
        if (not street):
            hs = None
        if (hs):
            if (not re.findall(r'\d+',hs)):
                hs = None
            else:
                for x in LS_NOISE_HOUSE_NUM:
                    if (x in str(hs).lower()):
                        hs = None
                        break
        street = map_street(street)
        if (street):
            street = re.sub('Đường Quốc Lộ','Quốc lộ',street)
            street = re.sub('Đường Hương Lộ','Hương lộ',street)
            street = re.sub('Quốc Lộ','Quốc lộ',street)
            street = re.sub('Hương Lộ','Hương lộ',street)
            street = re.sub('Đường Số','Đường số',street)
            street = re.sub(r' Tỉnh$','',street)
            street = re.sub(r' Huyện$','',street)
    return street,hs
