# Crawling

## 1. Objective 

- Download and parse data from **SOSANHNHA** site using bash script & awk.

## 2. How does it work ?  
**A Script structure described as below:**
-  download_site.sh : this is main script that calls other scripts
-  awk:
    - put_html_to_tab.awk: convert data from list mode pages to **extract.tab**
    - put_tab_to_db.awk: convert data from **extract.tab** to insert SQL script  
    - get_ads_details.awk: convert data from ads pages to update SQL script
    - decode_hex.awk: decrypt special characters from html file
    - get_list_category.awk: convert list category in sosanhnha main page to **category_list.temp**
-  bash:
    - parsing_insert.sh: run put_tab_to_db.awk to create **ads_insert.sql** for further import
    - parsing_update.sh: run get_ads_details.awk to create **ads_update.sql** for further import
-  python:
    - get_download_list.py: generate **download_list.temp** for list mode download
-  json: contain files which have id of the city and its districts
-  requirement.txt: contains all libraries with its version

### Step 0: Create following folders
-  ALL/: contains detail ads .html files.
-  DELTA/: 
    - ads_insert.sql: to insert the new ads to database
    - ads_update.sql: to update information about the new ads to database
    - extract_backup.tab: ads information getting from list pages
    - extract.tab (daily download): extract.tab after compare
    - category_list.temp: list of category and its id in sosannha. Example: `324	 Bán căn hộ chung cư`
    - download_list.temp: list of page url and its location code, every line include url and ads code (icat_iCit_iDis). Example: `https://sosanhnha.com/search?iCat=324&iCit=25&iDis=230	324-25-230`
    - status_ok: contains ``ok`` content to indicate that the program runs completely
- LIST_MODE/: contains list page .html files

###  Step 1: Download list pages and save .html files in LIST_MODE folder
-  There are some main problems when download from this site:
    - This site is encrypt number of page. For example: page 2 convert to page YM
    - This site is fake number of ads. For example: in this link `https://sosanhnha.com/search?iCat=324&iCit=2&iDis=3`, there are actual 3 ads but it can show 114,957 ads found
    - This site is limited **50** page of view. If total ads filter by the rules is larger than 50 pages, the 51th page will repeat the 50th. If the total number is smaller than 50 pages, it will display not found page
    - Some link ads detail in this site is not actual detail ads. Example: `https://sosanhnha.com/search?iCat=324&iCit=2&iDis=3`
-  Solution: find page download based on search link. Example: `https://sosanhnha.com/search?iCat=324&iCit=30&page=2`. To view city id, this URL can be refered: `https://sosanhnha.com/api/v2/locations?fields=name,id,type,dis_id&where=cit_id,ward_id+0,street_id+0,project_id+0`. List of district id in every city can be refered by using city_id. For example, list of district in Ho Chi Minh, which has city_id=30, is `https://sosanhnha.com/api/v2/locations?fields=name,id,type,dis_id&where=cit_id+30,ward_id+0,street_id+0,project_id+0`. Because of not define exact total ads, for large cities, including Ho Chi Minh, Ha Noi, Da Nang, Can Tho, Binh Duong, three levels of filter are used: iCat, iCit and iDis. With other cities, two levels of filter are used: iCat and iCit.
-  The script download_site.sh generate the **category_list.temp**, then the category list will be put to **get_download_list.py** to create **download_list.temp**. This download list will perform possible pages can be download in list mode. After that, the `download_list_mode` will begin and save all **(html)** files in LIST_MODE folder.

### Step 2: Download detail pages and save .html files in ALL folder
- Parsing the every file in LIST_MODE folder to create extract.tab
- Copy extract.tab to create extract_backup.tab
- If fully download, the script will generate list_need_to_download from full extract.tab. If daily download, the script will generate list_need_to_download from extract_update.tab, which created by comparing current extract.tab with its previous extract_backup.tab in the lastest folder.
- The `download_detail_mode` will use list_need_to_download to perform to download details pages and store **.html** files in ALL/ folder.

### Step 3: Parsing and insert data into the database
-  Parsing:  
    - Parsing list mode: for every line in extract.tab, the script bash/parsing_insert.sh will create **ads_insert.sql**
    - Parsing detail mode: for every html file in all folder, the script bash/parsing_update.sh will create **ads_update.sql**
-  Import: connect to mysql and import **ads_insert.sql** and **ads_update.sql** to the database 

## 3. How to run
**3.1/ Prerequisites**
- Libraries:
    - wget==3.2
- Install all libraries in requirements.txt: ``` pip3 install -r requirements.txt ```

**3.2/ How to run the script**

  ```
  * Options: 
     -x = debug
     -y = test mode
     -i = import SQL to database
     -r = Download Ads from LIST_MODE folder (don't re-download list pages)
     -d YYYYmmdd = date of download.
     -D = daily mode
  ```
    a) Test mode:    
        ./download_site.sh -zVN_SOSANHNHA -d{_date_store_} -x -y > log{_date_store_} 2>&1 &
        Example: ./download_site.sh -zVN_SOSANHNHA -d20200825 -x -y > log20200825 2>&1 &  

    b) Full mode:      
        ./download_site.sh -zVN_SOSANHNHA -d{_date_store_} -x > log{_date_store_} 2>&1 &   
        Example: we specific {_date_store_} is 20200825
        ./download_site.sh -zVN_SOSANHNHA -d20200825 -x > log20200825 2>&1 & 

    c) Daily mode:
        ./download_site.sh -zVN_SOSANHNHA -d{_date_store_} -x -D > log{_date_store_} 2>&1 &
        Example: ./download_site.sh -zVN_SOSANHNHA -d20200825 -x -D > log20200825 2>&1 &  
        
**Note:**
-   -x option must be call first others
-   If there is no {_date_store_}, {_date_store_} = today by default. Example: If today is 25/08/2020, if `./download_site.sh -zVN_SOSANHNHA -x > log20200825 2>&1 &` is run, folder will be 20200825
-   If there is no option -y, the script will run full mode by default
-   The script will parse data automatically or manually by calling `bash/ads_insert.sql {_date_store_}`  or `bash/ads_update.sql {_date_store_}`
-   If you import data into database, you will use -i options.      
-   If there is a test mode, only 4 districts and 4 pages in each district are created