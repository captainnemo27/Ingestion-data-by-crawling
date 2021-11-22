# Crawling

## 1. Objective 

- Download and parse data from **HOMEDY** site using bash script & awk.

## 2. How does it work ?  
**A Script structure described as below:**
-  download_site.sh : this is main script that calls other scripts
-  awk:
    - put_html_to_tab.awk: convert data from list mode pages to **extract.tab**
    - put_tab_to_db.awk: convert data from **extract.tab** to insert SQL script  
    - get_ads_details.awk: convert data from ads pages to update SQL script
    - decode_hex.awk: decrypt special characters from html file
    - get_list_page.awk: generate list of possible page can download
-  bash:
    - parsing_insert.sh: run put_tab_to_db.awk to create **ads_insert.sql** for further import
    - parsing_update.sh: run get_ads_details.awk to create **ads_update.sql** for further import

### Step 0: Create following folders
-  ALL/: contains detail ads .html files.
-  DELTA/: 
    - ads_insert.sql: to insert the new ads to database
    - ads_update.sql: to update information about the new ads to database
    - extract.tab: ads information getting from list pages
    - extract_update.tab (daily download): extract.tab after compare
    - download_list.temp: list of possible page can download, every line includes url, number of ads and type. Example: `https://homedy.com/cho-thue-nha-dat-lam-dong	10 lam-dong cho-thue-nha-dat`
    - status_ok: contains ``ok`` content to indicate that the program runs completely
- LIST_MODE/: contains list page .html files
- TEMP/: 
    - .*html: list of page to get location
    - ban-nha-dat_country_extract.tab: list city for sale: number of ads, link, name and type
    - ban-nha-dat_city_extract.tab: list district for sale: number of ads, link, name and type
    - cho-thue-nha-dat_country_extract.tab: list city for lease: number of ads, link, name and type
    - cho-thue-nha-dat_city_extract.tab: list district for lease: number of ads, link, name and type

###  Step 1: Download list pages and save .html files in LIST_MODE folder
-  The main problems when download from this site is limited **200** page of view. 
-  Solution: find page download based on location. If total ads number of a city is larger than 3600, go to its districts to download. That makes sure the total ads number of a location is always smaller than 3600.
-  The main script download_site.sh calls `download_list_mode` begin and save all html files in LIST_MODE folder.

### Step 2: Download detail pages and save .html files in ALL folder
- Parsing the every file in LIST_MODE folder to create extract.tab
- If fully download, the script will generate list_need_to_download from full extract.tab. If daily download, the script will generate list_need_to_download from extract_update.tab, which created by comparing current extract.tab with its previous extract.tab in the lastest folder.
- The `download_detail_mode` will use list_need_to_download to perform to download details pages and store html files in ALL/ folder.

### Step 3: Parsing and insert data into the database
-  Parsing:  
    - Parsing list mode: for every line in extract.tab, the script bash/parsing_insert.sh will create **ads_insert.sql**
    - Parsing detail mode: for every html file in all folder, the script bash/parsing_update.sh will create **ads_update.sql**
-  Import: connect to mysql and import **ads_insert.sql** and **ads_update.sql** to the database 

## 3. How to run
**3.1/ Prerequisites**
- Libraries:
    - pandas==1.1.2
    - Unidecode==1.1.1
    - requests==2.25.1
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
        ./download_site.sh -zVN_HOMEDY -d{_date_store_} -x -y > log{_date_store_} 2>&1 &
        Example: ./download_site.sh -zVN_HOMEDY -d20200825 -x -y > log20200825 2>&1 &  

    b) Full mode:      
        ./download_site.sh -zVN_HOMEDY -d{_date_store_} -x > log{_date_store_} 2>&1 &   
        Example: we specific {_date_store_} is 20200825
        ./download_site.sh -zVN_HOMEDY -d20200825 -x > log20200825 2>&1 & 

    c) Daily mode:
        ./download_site.sh -zVN_HOMEDY -d{_date_store_} -x -D > log{_date_store_} 2>&1 &
        Example: ./download_site.sh -zVN_HOMEDY -d20200825 -x -D > log20200825 2>&1 &  
        
**Note:**
-   -x option must be call first others
-   If there is no {_date_store_}, {_date_store_} = today by default. Example: If today is 25/08/2020, if `./download_site.sh -zVN_HOMEDY -x > log20200825 2>&1 &` is run, folder will be 20200825
-   If there is no option -y, the script will run full mode by default
-   The script will parse data automatically or manually by calling `bash/ads_insert.sql {_date_store_}`  or `bash/ads_update.sql {_date_store_}`
-   If you import data into database, you will use -i options.      
-   If there is a test mode, only 2 districts and 2 pages in each district are created