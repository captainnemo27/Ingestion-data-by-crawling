from config.config_ import *

# CREATE VN_TINH_HUYEN
def split_prefix(string,ls_prefix):
    '''
        Split string based on prefix

            Parameters:
                string (str): string need to be splitted
                ls_prefix (arr): list prefix
                    
            Returns:
                list (arr): tuple 0 is prefix, tuple 1 is value
    '''
    ls_prefix_2 = [x for x in ls_prefix if (x.count(' ')==1)]
    ls_prefix_1 = [x for x in ls_prefix if (x.count(' ')==0)]
    if (string.startswith(tuple(ls_prefix_2))):
        string = string.split()
        pref = ' '.join(string[0:2])
        val = ' '.join(string[2:])
        return [(pref,val)]
    if (string.startswith(tuple(ls_prefix_1))):
        string = string.split()
        pref = string[0]
        val = ' '.join(string[1:])
        return [(pref,val)]
    return [('',string)]

def pre_vn_quan_huyen(data,column):
    '''
        Preprocessing data vn_quan_huyen

            Parameters:
                data (dataframe): dataframe
                column (str): name column
                    
            Returns:
                df (dataframe): dataframe has been preprocessed column
    '''
    pref_col = column + '_prefix'
    val_col = column + '_val'
    spl_col = column + '_split'
       
    if (column == "street"):
        ls = ['Tỉnh lộ','Tỉnh Lộ' ,'Quốc lộ','Quốc Lộ'] #LS_LEVEL_STREET_ORIGINAL
    if (column == "ward"):
        ls = LS_LEVEL_WARD_ORIGINAL
    if (column == "district"):
        ls = LS_LEVEL_DISTRICT_ORIGINAL
    if (column == "city"):
        ls = LS_LEVEL_CITY_ORIGINAL
   
    data[column] = data[column].str.replace('Bà Rịa - Vũng Tàu','Bà Rịa Vũng Tàu')
    data[column] = data[column].str.replace('Phan Rang-Tháp Chàm','Phan Rang Tháp Chàm')
    data[column] = data[column].apply(lambda x: " ".join(x.split()) if (pd.notnull(x)) else x)
    
    # split street = street_pref and street_val 
    if (column == "street"):
        data[pref_col] = data[column].apply(lambda x:split_prefix(x,ls)[0][0] if (pd.notnull(x)) else x)
        data[val_col] = data[column].apply(lambda x:split_prefix(x,ls)[0][1] if (pd.notnull(x)) else x)
        data[pref_col] = data[pref_col].apply(lambda x: 'Đường' if (x == '') else x)
    else:
        data[spl_col] = data[column].apply(lambda x:split_prefix(x,ls)[0] if (pd.notnull(x)) else x)
        data[[pref_col, val_col]] = pd.DataFrame(data[spl_col].tolist(), index=data.index)
    data = data[data[val_col].notna()]
    data[val_col] = data[val_col].apply(lambda x: int(x) if (x.isdigit()) else x)
    
    # drop dupciate
    df = data.drop_duplicates(subset=[pref_col, val_col], keep='last')
    df['length_pref'] = df[pref_col].apply(lambda x: x.count(' ') if (pd.notnull(x)) else 0)
    df['length'] = df[val_col].apply(lambda x: len(str(x)) if (pd.notnull(x)) else 0)
    df = df.sort_values(['length_pref','length'], ascending=[False,False])
    df = df.reset_index(drop=True)
    df = df[df["length"] >= 1]
    df.drop(['length_pref','length'], axis=1, inplace=True)
    df = df.fillna('')
    return df

def create_vn_tinh_huyen(save_file,write_mode=False):
    '''
        Create dataframe vn_tinh_huyen

            Parameters:
                save_file (str): name of save file
                write_mode (bool): True if write file else False
                    
            Returns:
                df (dataframe): dataframe vn_tinh_huyen
    '''
    # Read vn_units from file
    vn_units = pd.read_csv("json/Data Cleaning - vn tinh-huyen.csv")
    vn_units = vn_units.rename(
        columns={
            'Tỉnh Thành Phố': "city",
            'Mã TP': "city_code",
            'Quận Huyện': "district",
            'Mã QH': 'district_code',
            'Phường Xã': 'ward',
            'Mã PX': 'ward_code',
            'Cấp': 'level_ward',
            'Tên Tiếng Anh': 'english_name'})
    vn_units = vn_units[['city','district','ward']]
    
    # Split column
    vn_city = pre_vn_quan_huyen(vn_units,'city')
    vn_district = pre_vn_quan_huyen(vn_units,'district')
    vn_ward = pre_vn_quan_huyen(vn_units,'ward')
    
    # Format value
    vn_units['city_val'] = vn_units['city_val'].apply(lambda x: int(x) if ((pd.notnull(x)) and (x.isdigit())) else x)
    vn_units['district_val'] = vn_units['district_val'].apply(lambda x: int(x) if ((pd.notnull(x)) and (x.isdigit())) else x)
    vn_units['ward_val'] = vn_units['ward_val'].apply(lambda x: int(x) if ((pd.notnull(x)) and (x.isdigit())) else x)
    
    # Format prefix
    vn_units['city_prefix'] = vn_units['city_prefix'].apply(lambda x: unidecode(x).lower().strip() if (pd.notnull(x)) else x)
    vn_units['district_prefix'] = vn_units['district_prefix'].apply(lambda x: unidecode(x).lower().strip() if (pd.notnull(x)) else x)
    vn_units['ward_prefix'] = vn_units['ward_prefix'].apply(lambda x: unidecode(x).lower().strip() if (pd.notnull(x)) else x)

    # Drop split columns
    vn_units.drop(['city_split','district_split','ward_split'], axis=1, inplace=True)
    
    df_hcm = vn_units[(vn_units['city_prefix']=='thanh pho') & (vn_units['city_val']=='Hồ Chí Minh')]
    df_thuduc = df_hcm[(df_hcm['district_prefix']=='quan') & (df_hcm['district_val'].isin([2,9,'Thủ Đức']))]
    df_thuduc['district_prefix'] = 'thanh pho'
    df_thuduc['district_val'] = 'Thủ Đức'
    df_thuduc['district'] = 'Thành phố Thủ Đức'
    df = pd.concat([vn_units,df_thuduc])
    
    # Save file
    if (write_mode):
        df.to_csv(save_file,index=False)
        
    return df

# CREATE VN_TINH_DUONG
def remove_space(string):
    '''
        Remove extra spaces from string

            Parameters:
                string (str): string need to be remove spaces
                    
            Returns:
                string (str): string after remove spaces
    '''
    string = " ".join(string.split())
    return string

def create_vn_tinh_duong(street_folder,save_file,write_mode=False):
    '''
        Create dataframe vn_tinh_duong

            Parameters:
                street_folder (name):name of folder json
                save_file (str): name of save file
                write_mode (bool): True if write file else False
                    
            Returns:
                df (dataframe): dataframe vn_tinh_duong
    '''
    d = []
    for fn in os.listdir(street_folder):
        if (fn == ".DS_Store"):
            continue
        with open (street_folder+fn) as f:
            data = json.load(f)
            city_name = data['name']
            if (unidecode(city_name.lower()) in ["ho chi minh", "hai phong", "da nang", "can tho", "ha noi"]):
                city = 'Thành phố'
            else:
                city = 'Tỉnh'
            for i in range(0,len(data['district'])):
                district = data['district'][i]['pre']
                district_name = data['district'][i]['name']
                street_name = data['district'][i]['street']
                # Case Quận 3,...
                if (district == '') and (re.findall(r'^Quận',district_name)):
                    district = 'Quận'
                    district_name = re.sub(r'^Quận','',district_name).strip()
                for s in street_name:
                    d.append([remove_space(city),remove_space(city_name),remove_space(district),remove_space(district_name),remove_space(s)])
    
    df = pd.DataFrame(d,columns=['city_prefix','city_val','district_prefix','district_val','street'])
    df['district_val'] = df['district_val'].str.replace('Phan Rang - Tháp Chàm','Phan Rang Tháp Chàm')
    data = pre_vn_quan_huyen(df,'street')

    # Format prefix
    data['city_prefix'] = data['city_prefix'].apply(lambda x: unidecode(x).lower().strip() if (pd.notnull(x)) else x)
    data['district_prefix'] = data['district_prefix'].apply(lambda x: unidecode(x).lower().strip() if (pd.notnull(x)) else x)
    data['street_prefix'] = data['street_prefix'].apply(lambda x: unidecode(x).lower().strip() if (pd.notnull(x)) else x)

    # Format value
    data["street_val"] = data["street_val"].apply(lambda x:split_prefix(str(x),["Số"])[0][1] if (pd.notnull(x)) else x)
    data = data[data['street_val']!='']
    
    df_hcm = data[(data['city_prefix']=='thanh pho') & (data['city_val']=='Hồ Chí Minh')]
    df_thuduc = df_hcm[(df_hcm['district_prefix']=='quan') & (df_hcm['district_val'].isin([2,9,'Thủ Đức']))]
    df_thuduc['district_prefix'] = 'thanh pho'
    df_thuduc['district_val'] = 'Thủ Đức'
    d = pd.concat([data,df_thuduc])
    
    if (write_mode):
        d.to_csv(save_file,sep=';',index=False)
    return d
    
# CREATE DIC 3 LEVEL: DIC_CITY_DISTRICT_WARD, DIC_CITY_DISTRICT_STREET
def get_dis_in_city(df,city):
    '''
        Get list prefix of district in city

            Parameters:
                df (dataframe): name of dataframe
                city (string): name of city
                    
            Returns:
                ls_dis_pref (arr): list of prefix of district in city
    '''
    df_city = df[df["city_val"]==city]
    ls_dis_pref = list(df_city["district_prefix"].unique())
    ls_dis_pref.sort(key=lambda s: str(s).count(' '),reverse=True)
    return ls_dis_pref


def get_ward_in_dis(df,dis):
    '''
        Get list prefix of ward in district

            Parameters:
                df (dataframe): name of dataframe
                ward (string): name of ward
                    
            Returns:
                ls_ward_pref (arr): list of prefix of ward in district
    '''
    df_dis = df[df["district_val"]==dis]
    ls_ward_pref = list(df_dis["ward_prefix"].unique())
    ls_ward_pref.sort(key=lambda s: str(s).count(' '),reverse=True)
    return ls_ward_pref


def get_street_in_dis(df,dis):
    '''
        Get list prefix of street in district

            Parameters:
                df (dataframe): name of dataframe
                dis (string): name of district
                    
            Returns:
                ls_street_pref (arr): list of prefix of street in district
    '''
    df_dis = df[df["district_val"]==dis]
    ls_street_pref = list(df_dis["street_prefix"].unique())
    ls_street_pref.sort(key=lambda s: str(s).count(' '),reverse=True)
    return ls_street_pref


def gen_dic_3_level(df,value):
    '''
        Create dictionary 3 level

            Parameters:
                df (dataframe): name of dataframe
                value (string): ward or street
                    
            Returns:
                dic (dictionary): dic 3 level ward or dic 3 level street
    '''
    # distinct city prefix
    ls_city_pref = list(df["city_prefix"].unique())
    dic = {}
    for i in ls_city_pref:
        dic[i] = {}
        df1 = df[df["city_prefix"]==i]
        # distinct city in city prefix
        ls_city_val = list(df1["city_val"].unique())
        ls_city_val.sort(key=lambda x: len(str(x)), reverse=True)
        ls_city_val.sort(key=lambda s: str(s).count(' '),reverse=True)
        for j in ls_city_val:
            dic[i][j] = {}
            # distinct district prefix in city
            ls_dis_pref = get_dis_in_city(df,j)
            for k in ls_dis_pref:
                dic[i][j][k] = {}
                df2 = df1[(df1["city_val"]==j) & (df["district_prefix"]==k)]
                # distinct district value in prefix
                ls_dis_val = list(df2["district_val"].unique())
                ls_dis_val.sort(key=lambda x: len(str(x)), reverse=True)
                ls_dis_val.sort(key=lambda s: str(s).count(' '),reverse=True)
                for l in ls_dis_val:
                    dic[i][j][k][l] = {}
                    if (value == "ward"):
                        # distinct ward prefix in district
                        ls_ward_pref = get_ward_in_dis(df,l)
                        for m in ls_ward_pref:
                            df3 = df2[(df2["district_val"]==l) & (df2["ward_prefix"]==m)]
                            # distinct ward value in district
                            ls_ward_val = list(df3["ward_val"].unique())
                            ls_ward_val.sort(key=lambda x: len(str(x)), reverse=True)
                            ls_ward_val.sort(key=lambda s: str(s).count(' '),reverse=True)
                            dic[i][j][k][l][m] = ls_ward_val
                    elif (value == "street"):
                        # distinct street prefix in district
                        ls_street_pref = get_street_in_dis(df,l)
                        for m in ls_street_pref:
                            df3 = df2[(df2["district_val"]==l) & (df2["street_prefix"]==m)]
                            # distinct street value in district
                            ls_street_val = list(df3["street_val"].unique())
                            ls_street_val.sort(key=lambda x: len(str(x)), reverse=True)
                            ls_street_val.sort(key=lambda s: str(s).count(' '),reverse=True)
                            dic[i][j][k][l][m] = ls_street_val
    return dic

def create_dic_tinh_huyen(mode_write=False):
    '''
        Create dictionary tinh huyen

            Parameters:
                mode_write: True if write to file else False
                    
            Returns:
                dic_vn_tinh_huyen (dictionary): dictionary vn_tinh_huyen
    '''    
    # Read vn_tinh_huyen from file
    vn_tinh_huyen = pd.read_csv('json/data_vn_tinh_huyen.csv')

    # Create dictionary
    dic_vn_tinh_huyen = gen_dic_3_level(vn_tinh_huyen,"ward")
    
    # Save dictionary
    if (mode_write == True):
        with open('json/DIC_CITY_DISTRICT_WARD.json', 'w') as f:
            json.dump(dic_vn_tinh_huyen, f, ensure_ascii=False)
        
    return dic_vn_tinh_huyen

def create_dic_tinh_duong(mode_write=False):
    '''
        Create dictionary tinh duong

            Parameters:
                mode_write: True if write to file else False
                    
            Returns:
                dic_vn_tinh_huyen (dictionary): dictionary vn_tinh_duong
    '''    
    # Read vn_tinh_duong from file
    vn_tinh_duong = pd.read_csv('json/data_vn_tinh_duong.csv',sep=';')
    
    # Split column
    pre_vn_quan_huyen(vn_tinh_duong,'street')
    
    # Format value
    vn_tinh_duong['city_val'] = vn_tinh_duong['city_val'].apply(lambda x: str(int(x)) if ((pd.notnull(x)) and (x.isdigit())) else x)
    vn_tinh_duong['district_val'] = vn_tinh_duong['district_val'].apply(lambda x: str(int(x)) if ((pd.notnull(x)) and (x.isdigit())) else x)
    vn_tinh_duong['street_val'] = vn_tinh_duong['street_val'].apply(lambda x: str(int(x)) if ((pd.notnull(x)) and (x.isdigit())) else x)
    
    # Format prefix
    vn_tinh_duong['city_prefix'] = vn_tinh_duong['city_prefix'].apply(lambda x: unidecode(x).lower().strip() if (pd.notnull(x)) else x)
    vn_tinh_duong['district_prefix'] = vn_tinh_duong['district_prefix'].apply(lambda x: unidecode(x).lower().strip() if (pd.notnull(x)) else x)
    vn_tinh_duong['street_prefix'] = vn_tinh_duong['street_prefix'].apply(lambda x: unidecode(x).lower().strip() if (pd.notnull(x)) else x)
    
    # Create dictionary
    dic_vn_tinh_duong = gen_dic_3_level(vn_tinh_duong,"street")
    
    # Save dictionary
    if (mode_write == True):
        with open('json/DIC_CITY_DISTRICT_STREET.json', 'w') as f:
            json.dump(dic_vn_tinh_duong, f, ensure_ascii=False)
    
    return dic_vn_tinh_duong


# CREATE DIC 2 LEVEL: DIC_CITY_WARD, DIC_CITY_STREET
def gen_dic_2_level(dic_all,city,city_name):
    '''
        Create dictionary 2 level

            Parameters:
                dic_all (dictionary): dictionary 3 level
                city (str): city prefix
                city_name (str): city name
                    
            Returns:
                dic (dictionary): dic 3 level ward or dic 3 level street
    '''
    ls_dis_prefix = list(dic_all[city][city_name].keys())
    ls_dis_prefix.sort(key=lambda s: str(s).count(' '),reverse=True)
    dic_gen = {}
    for district in ls_dis_prefix:
        ls_dis_val = list(dic_all[city][city_name][district].keys())
        ls_dis_val.sort(key=lambda x: len(str(x)), reverse=True)
        ls_dis_val.sort(key=lambda s: str(s).count(' '),reverse=True)
        for district_name in ls_dis_val:
            ls_prefix = list(dic_all[city][city_name][district][district_name].keys())
            ls_prefix.sort(key=lambda s: str(s).count(' '),reverse=True)
            for prefix in ls_prefix:
                ls_val = list(dic_all[city][city_name][district][district_name][prefix])
                ls_val.sort(key=lambda x: len(str(x)), reverse=True)
                ls_val.sort(key=lambda s: str(s).count(' '),reverse=True)
                if (prefix not in dic_gen):
                    dic_gen[prefix] = ls_val
                else:
                    dic_gen[prefix] = list(set(dic_gen[prefix] + ls_val))
                    
    for key in dic_gen:
        dic_gen[key].sort(key=lambda x: len(str(x)), reverse=True)
        dic_gen[key].sort(key=lambda s: str(s).count(' '),reverse=True)
        
    d = {}
    l = list(dic_gen.keys())
    l.sort(key=lambda s: str(s).count(' '),reverse=True)
    for key in l:
        d[key] = dic_gen[key]
    return d


def create_dic_city_ward(write_mode=False):
    '''
        Create dictionary city_ward

            Parameters:
                mode_write: True if write to file else False
                    
            Returns:
                dic_city_ward (dictionary): dictionary city_ward
    '''    
    # Load dictionary all
    with open("json/DIC_CITY_DISTRICT_WARD.json", "r", encoding="utf8") as f:
        DIC_CITY_DISTRICT_WARD = json.load(f)
    # Solve problem
    dic_city_ward = {}
    ls_city = list(DIC_CITY_DISTRICT_WARD.keys())
    ls_city.sort(key=lambda s: str(s).count(' '),reverse=True)
    for city in ls_city:
        dic_city_ward[city] = {}
        ls_city_name = list(DIC_CITY_DISTRICT_WARD[city].keys())
        ls_city_name.sort(key=lambda x: len(str(x)), reverse=True)
        ls_city_name.sort(key=lambda s: str(s).count(' '),reverse=True)
        for city_name in ls_city_name:
            dic_city_ward[city][city_name] = gen_dic_2_level(DIC_CITY_DISTRICT_WARD,city,city_name)
    # Save dictionary
    if (write_mode == True):
        with open('json/DIC_CITY_WARD.json', 'w') as f:
            json.dump(dic_city_ward, f, ensure_ascii=False)
    return dic_city_ward


def create_dic_city_street(write_mode=False):
    '''
        Create dictionary city_street

            Parameters:
                mode_write: True if write to file else False
                    
            Returns:
                dic_city_street (dictionary): dictionary city_street
    '''    
    # Load dictionary all
    with open("json/DIC_CITY_DISTRICT_STREET.json", "r", encoding="utf8") as f:
        DIC_CITY_DISTRICT_STREET = json.load(f)
    # Solve problem
    dic_city_street = {}
    ls_city = list(DIC_CITY_DISTRICT_STREET.keys())
    ls_city.sort(key=lambda s: str(s).count(' '),reverse=True)
    for city in ls_city:
        dic_city_street[city] = {}
        ls_city_name = list(DIC_CITY_DISTRICT_STREET[city].keys())
        ls_city_name.sort(key=lambda x: len(str(x)), reverse=True)
        ls_city_name.sort(key=lambda s: str(s).count(' '),reverse=True)
        for city_name in ls_city_name:
            dic_city_street[city][city_name] = gen_dic_2_level(DIC_CITY_DISTRICT_STREET,city,city_name)
    # Save dictionary
    if (write_mode == True):
        with open('json/DIC_CITY_STREET.json', 'w') as f:
            json.dump(dic_city_street, f, ensure_ascii=False)
    return dic_city_street


# CREATE DIC 1 LEVEL: DIC_STREET, DIC_WARD, DIC_DISTRICT, DIC_CITY
def create_dic_distinct(column,mode_write=False):
    '''
        Create dictionary distinct street, ward, district, city

            Parameters:
                column: street or ward or district or city
                mode_write: True if write to file else False
                    
            Returns:
                dic (dictionary): dictionary distinct street, ward, district, city
    '''    
    pref_col = column + '_prefix'
    val_col = column + '_val'
    dic_file = 'json/DIC_' + column.upper() + '.json'

    # load dataframe
    if (column != "street"):
        df = pd.read_csv("json/data_vn_tinh_huyen.csv")
    else:
        df = pd.read_csv("json/data_vn_tinh_duong.csv",sep=';')
        
    # convert dataframe to dic
    d = df[[pref_col,val_col]]
    d = d.drop_duplicates(subset=[pref_col,val_col], keep='first')
    dic_df = d.groupby(pref_col)[[val_col]].apply(lambda g: g.values.tolist()).to_dict()
    
    # flatten dic value
    dic = {}
    ls_key = list(dic_df.keys())
    ls_key.sort(key=lambda s: str(s).count(' '),reverse=True) 
    for key in ls_key:
        l = [a for c in list(dic_df[key]) for a in c ]
        l.sort(key=lambda x: len(str(x)), reverse=True)
        l.sort(key=lambda s: str(s).count(' '),reverse=True)
        dic[key] = l

    # Save dictionary
    if (mode_write == True):
        with open(dic_file, 'w') as f:
            json.dump(dic, f, ensure_ascii=False)

    return dic

# CREATE DIC_COMBINE_LEVEL
def df_to_nested_dic(df,cols):
    """
    Generate nested dictionary from dataframe
    
    Parameters
    ----------
    df: dataframe
        dataframe need to be converted
    cols: array
        list hierarchical keys of nested dictionary 
    
    Return
    ------
    dictionary
        nested dictionary       
    """
    d = defaultdict(dict)

    for i, row in df.iterrows():
        if (row[cols[0]] not in d):
            d[row[cols[0]]][row[cols[1]]] = [row.drop(cols).to_list()]
        elif (row[cols[1]] not in d[row[cols[0]]]):
            d[row[cols[0]]][row[cols[1]]] = [row.drop(cols).to_list()]
        else:
            d[row[cols[0]]][row[cols[1]]].append(row.drop(cols).to_list())
    for city in d:
        for district in d[city]:
            d[city][district] = [x for l in d[city][district] for x in l] 
    return dict(d)


def create_dic_combine(write_mode=False):
    '''
        Create dictionary combine key1 = city, key2 = district, value = list wards

            Parameters:
                mode_write: True if write to file else False
                    
            Returns:
                dic_combine_level (dictionary): dictionary combine_level
    '''    
    # Read vn_units from file
    vn_units = pd.read_csv("json/data_vn_tinh_huyen.csv")
    
    vn_units['city'] = vn_units.apply(lambda row: row['city_prefix'] + ' ' + row['city_val'] if ((pd.notnull(row['city_prefix'])) and (pd.notnull(row['city_val']))) else None,axis=1)
    vn_units['district'] = vn_units.apply(lambda row: row['district_prefix'] + ' ' + row['district_val'] if ((pd.notnull(row['district_prefix'])) and (pd.notnull(row['district_val']))) else None,axis=1)
    vn_units['ward'] = vn_units.apply(lambda row: row['ward_prefix'] + ' ' + row['ward_val'] if ((pd.notnull(row['ward_prefix'])) and (pd.notnull(row['ward_val']))) else None,axis=1)
    
    vn_units = vn_units[['city','district','ward']]
    # Create dictionary
    dic_combine_level = df_to_nested_dic(vn_units,['city','district'])
    # Write dictionary
    if (write_mode == True):
        with open('json/DIC_COMBINE_LEVEL.json', 'w') as f:
            json.dump(dic_combine_level, f, ensure_ascii=False)
            
    return dic_combine_level


def main():
    # ARGUMENTS
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--dic_name", type=str, default="")
    parser.add_argument("-w","--write_mode", type=bool, default=False)
    args = parser.parse_args()

    name = args.dic_name
    mode = args.write_mode

    ls_name = ["tinh_huyen","tinh_duong",\
        "city_district_street","city_district_ward","combine_level",\
            "city_street","city_ward",\
            "district","street","ward"]

    if (name not in ls_name):
        parser.print_help(sys.stderr)
        print()
        print("error: dictionary name not in list")
        print(ls_name)
        sys.exit(1)
    
    # CREATE VN_TINH_HUYEN
    if (name == "tinh_huyen"):
        #Save vn_tinh_huyen
        save_file = 'json/data_vn_tinh_huyen.csv'
        vn_tinh_huyen = create_vn_tinh_huyen(save_file,mode)
        print("vn_tinh_huyen.head")
        print(vn_tinh_huyen.head())


    # CREATE VN_TINH_DUONG
    if (name == "tinh_duong"):
        # Save vn_tinh_duong
        street_folder = 'json/street_name/'
        save_file = 'json/data_vn_tinh_duong.csv'
        vn_tinh_duong = create_vn_tinh_duong(street_folder,save_file,mode)
        print("vn_tinh_duong.head")
        print(vn_tinh_duong.head())


    # CREATE DIC 3 LEVEL: DIC_CITY_DISTRICT_WARD, DIC_CITY_DISTRICT_STREET
    if (name == "city_district_ward" or name == "tinh_huyen"):
        dic_vn_tinh_huyen = create_dic_tinh_huyen(mode)
        print("dic_vn_tinh_huyen['thanh pho']['Hà Nội']['quan']['Ba Đình']['phuong']")
        print(dic_vn_tinh_huyen['thanh pho']['Hà Nội']['quan']['Ba Đình']['phuong'])
        print("dic_vn_tinh_huyen['thanh pho']['Hồ Chí Minh']['quan']['10']['phuong']")
        print(dic_vn_tinh_huyen['thanh pho']['Hồ Chí Minh']['quan']['10']['phuong'])
    if (name == "city_district_street" or name == "tinh_duong"):
        dic_vn_tinh_duong = create_dic_tinh_duong(mode)
        print("dic_vn_tinh_duong['thanh pho']['Hà Nội']['quan']['Ba Đình']['duong']")
        print(dic_vn_tinh_duong['thanh pho']['Hà Nội']['quan']['Ba Đình']['duong'])
        print("dic_vn_tinh_duong['thanh pho']['Hồ Chí Minh']['quan']['10']['duong']")
        print(dic_vn_tinh_duong['thanh pho']['Hồ Chí Minh']['quan']['10']['duong'])


    # CREATE DIC 2 LEVEL: DIC_CITY_WARD, DIC_CITY_STREET
    if (name == "city_ward" or name == "city_district_ward" or name == "tinh_huyen"):
        dic_city_ward = create_dic_city_ward(mode)
        print("dic_city_ward['thanh pho']['Hồ Chí Minh']['phuong']")
        print(dic_city_ward['thanh pho']['Hồ Chí Minh']['phuong'])
    if (name == "city_street" or name == "city_district_street" or name == "tinh_duong"):
        dic_city_street = create_dic_city_street(mode)
        print("dic_city_street['thanh pho']['Hồ Chí Minh']['quoc lo']")
        print(dic_city_street['thanh pho']['Hồ Chí Minh']['quoc lo'])


    # CREATE DIC 1 LEVEL: DIC_STREET, DIC_WARD, DIC_DISTRICT, DIC_CITY
    if (name == "city" or name == "tinh_huyen"):
        dic_city = create_dic_distinct("city",mode)
        print("dic_city['thanh pho']")
        print(dic_city['thanh pho'])
    if (name == "district" or name == "tinh_huyen"):
        dic_district = create_dic_distinct("district",mode)
        print("dic_district['quan']")
        print(dic_district['quan'])
    if (name == "ward" or name == "tinh_huyen"):
        dic_ward = create_dic_distinct("ward",mode)
        print("dic_ward['phuong']")
        print(dic_ward['phuong'])
    if (name == "street" or name == "tinh_duong"):
        dic_street = create_dic_distinct("street",mode)
        print("dic_street['quoc lo']")
        print(dic_street['quoc lo'])

    
    # CREATE DIC_COMBINE_LEVEL
    if (name == "combine_level" or name == "tinh_huyen"):
        dic_combine_level = create_dic_combine(mode)
        print("dic_combine_level")
        print(dic_combine_level)

    
if __name__ == "__main__":
    main()


