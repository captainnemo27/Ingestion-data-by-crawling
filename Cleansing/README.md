# Data Cleaning

## 1. Objectives 

- Cleaning data from each table in database using python.
- Fields should be cleaned: ```"ADS_DATE",'LAND_TYPE','LEGAL_STATUS','PRO_DIRECTION',
    	'CITY','DISTRICT','WARD','STREET',"FULL_ADDRESS","LAT","LON",
         'USED_SURFACE','SURFACE','SURFACE_UNIT','PRICE','PRICE_UNIT',
         'PRO_LENGTH','PRO_WIDTH','ALLEY_ACCESS', 'FRONTAGE','NB_ROOMS','NB_FLOORS','BEDROOM','BATHROOM','DEALER_TEL','DEALER_EMAIL','DEALER_JOINED_DATE',
            'ADS_DATE_ORIGINAL','DATE_ORIGINAL','PRICE_ORIGINAL','SURFACE_ORIGINAL'```

## 2. Script structure  
- config: store config files
	- config_.py: store common config
	- site_config.py: host, name, password and dics for each sites 
- libs: store library files
	-  or_utils.py: contains common functions
- json: store dictionary files 
	- street_name: list of streets in districts in cities of Vietnam crawling from [github](https://github.com/thien0291/vietnam_dataset.git) 
	- `Data Cleaning - vn tinh-huyen.csv`: data from offical website
	- `vn_tinh_huyen.csv`: vn_tinh_huyen generated from `Data Cleaning - vn tinh-huyen.csv`
	- `vn_tinh_duong.csv`: vn_tinh_duong generated from street_name
	- `dic_CITY.json`, `dic_DISTRICT.json`, `dic_WARD.json`, `dic_STREET.json`: dic unique city, district, ward, street with key = prefix and value = list cities or districts or wards or streets. Example: {thanhpho: ['Hồ Chí Minh','Hà Nội'], tinh: ['Ninh Bình','Cà Mau']}
	- `dic_CITY_WARD`,`dic_CITY_STREET`: dic wards or streets in cities, with key1 = 'thanhpho', key2 = 'Hồ Chí Minh', key3 = 'phuong', value = list ward. Example: data['thanhpho']['Hồ Chí Minh']['phuong']
	- `dic_CITY_DISTRICT_WARD`, `dic_CITY_DISTRICT_STREET`: dic wards or streets in districts, districts in cities, with with key1 = 'thanhpho', key2 = 'Hà Nội', key3 = 'quan', key4 = 'ba dinh', key5 = 'phuong' and value = list ward or list streets. Example: data["thanhpho"]["Hà Nội"]["quan"]["Ba Đình"]["phuong"] 
	- `dic_combine_level`: dic wards or streets in districts, districts in cities in unidecode format, with key1 = 'thanh pho ho chi minh', key2 = 'quan 3'
-  clean_site.py: the script used for cleaning each site
-  create_dic.py: create neccessary dictionaries for split address
-  pre_visualize.py: the script for checking after crawling or cleansing each site
-  data_backup.py: the script backup records cleaned to backup table
-  requirements.txt: contains all libraries with versions

## 3. Cleaning Workflow 
1. Update `PRO_FLAG` 0 -> 5
2. Set chunk = 1000
3. Clean fields (*)
4. Insert data into table `CLEAN_SITENAME` table
5. Loop from step 2,3,4 until read all `SITENAME` table
6. Insert `CLEAN_SITENAME` table into `REAL_CLEAN_SITENAME`
7. Update `PRO_FLAG` 5 -> 12

**Note**
- Clean fields based on rules defined in [sheet table](https://docs.google.com/spreadsheets/d/1cz-1qhT-2Vu1MliCuWH4Wxz2Oy-yLJ1G4YP6u_49NME/edit?ts=5f5f3cec#gid=0)
- Two IDs in diffeent websites could be the same and one ID in the specific website but different `CREATED_DATE` can be repeated. Solving this problem by setting `REAL_CLEAN_SITENAME` keys include `ID_CLIENT`, `SITE` and `CREATED_DATE` 
- All processes have been interagted automatically in Jenkins


## 4. How to run
### 4.1/ Prerequisites

**Docker Environment**
- docker: pyspark==3.0.1

- Activate environment: 
	- $ docker exec -it -u 0 oreal-spark /bin/bash

**Local Environment**

- virtualenv==20.4.7

- Activate environment: 
	- $ virtualenv mypython
	- $ source mypython/bin/activate

**Libraries**
- List libraries and their versions:
	- mysql-connector-python==8.0.21
	- pandas==1.1.2
	- SQLAlchemy==1.3.19
	- Unidecode==1.1.1
	- geopy==2.0.0
	- PyMySQL==0.10.1
	- mysql.connector==2.2.9
	- cryptography==3.1.1
	- prettytable==2.0.0
	- tqdm==4.56.0
	- tabulate==0.8.9
	- findspark==1.4.2

- Install all libraries in requirements.txt: 
	- $ pip3 install -r requirements.txt


### 4.2/ How to run the script clean_site.py

**Options** 
```-s``` = site name
```-t``` = test mode, default = False: if True, gen first 4000 records
```-pf``` = pro flag, default = 5: if test mode True, gen with pro_flag, else pro_flag = 5
```-i``` = index, default = 0 if test mode True, gen with index, else index = 0

**Test mode**    
	
- Running script:
	- $ python3 clean_site.py -s sitename -t test_mode -pf pro_flag -i index
	
- Example: 
	- $ python3 clean_site.py -s alonhadat -t True -pf 5 -i 170000 

**Full mode**      
	
- Running script:
	- $ python3 clean_site.py -s sitename
	
- Example: 
	- $ python3 clean_site.py -s alonhadat   

**Note**
- Site name must in list sites: ```"dothinet","batdongsancomvn","diaoconline","homedy","mogivn",
    "nhachotot","nhadatcafeland","propzyvn","revervn",
    "sosanhnha","tinbatdongsan","batdongsan","youhomes","alonhadat","rongbay"```
- Pro flag must in list ```0,5,12```

### 4.3/ How to run the script pre_visualize.py

**Options** 
```-s``` = site: site name
```-t``` = date: table. Ex: VN_REAL_RAW_2021_08
```-f``` = from date %Y%m%d: created date from date. Ex: 20210401
```-e``` = end date %Y%m%d: created date end date. Ex: 20210401

**Check crawl mode**    
- Running script:
	- $ python3 pre_visualize -s sitename -t table
- Example: visualize crawl table VN_REAL_RAW_2021_08/ALONHADAT
	- $ python3 pre_visualize -s alonhadat -t VN_REAL_RAW_2021_08


**Check crawl mode from date to date**    
- Running script:
	- $ python3 pre_visualize -s sitename -t table -f from_date -e to_date
- Example: visualize crawl table VN_REAL_RAW_2021_08/ALONHADAT from 10/08/2021 to 15/08/2021
	- $ python3 pre_visualize -s alonhadat -t VN_REAL_RAW_2021_08 -f 20210810 -e 20210815

**Note**
- Site name must in list sites: ```"dothinet","batdongsancomvn","diaoconline","homedy","mogivn",
    "nhachotot","nhadatcafeland","propzyvn","revervn",
        "sosanhnha","tinbatdongsan","batdongsan","youhomes","alonhadat","rongbay"```

### 4.4/ How to run the script transfer_data.py

**Options** 
```-s``` = site name
```-f``` = from date %Y%m%d: created date from date. Ex: 20210401
```-e``` = end date %Y%m%d: created date end date. Ex: 20210401
```-t``` = test mode, default = False: if True, convert all test cleansing table to REAL_CLEAN_ALL
```-u``` = city name, with prefix. Ex: Tỉnh Khánh Hòa

**Test mode**    
	
- Running script:
	- $ python3 transfer_data.py -u city_name -t True
	
- Example: 
	- $ python3 transfer_data.py -u 'Tỉnh Khánh Hòa' -t True

**Full mode**      
	
- Running script:
	- $ $ python3 transfer_data.py -u city_name
	
- Example: 
	- $ python3 transfer_data.py -u 'Tỉnh Khánh Hòa'  

**Full mode with date**      
	
- Running script:
	- $ $ python3 transfer_data.py -u city_name -f from_date -e end_date
	
- Example: 
	- $ python3 transfer_data.py -u 'Tỉnh Khánh Hòa' -f 20210601 -e 20210701 

**Site mode**    
	
- Running script:
	- $ python3 transfer_data.py -s site_name -f from_date -e end_date
	
- Example: 
	- $ python3 transfer_data.py -s alonhadat -f 20210601 -e 20210701

**Note**
- Site name must in list sites: ```"dothinet","batdongsancomvn","diaoconline","homedy","mogivn",
    "nhachotot","nhadatcafeland","propzyvn","revervn",
    "sosanhnha","tinbatdongsan","batdongsan","youhomes","alonhadat","rongbay"```

### 4.5/ How to run the script create_dic.py

**Options** 
```-d``` = dic name
```-w``` = write mode, default = False. If write = True, write file

**Full Mode**    
	
- Running script:
	- $ python3 create_dic.py -d
	
- Example: 
	- $ python3 create_dic.py -d city_dictrist_ward   

**Note**
- Dic name must in list dictionaries: ```""tinh_huyen","tinh_duong", "city_district_street","city_district_ward","combine_level", "city_street","city_ward","district","street","ward"```
