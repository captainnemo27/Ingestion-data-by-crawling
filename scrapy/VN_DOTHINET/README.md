# Crawling

## 1. Objective 

- Download and parse data from **dothi.net** site using bash script & awk

## 2. Workflow
    
###  2.1.  Create folder to save
        
   -   ALL: folder save all Ads file.
   -   DELTA: folder save 2 file sql important ( insert.sql-insert new ads to database and update.sql-update ads information ) and some project *.tab file.
   -   LIST_MODE: folder save list pages.
   -   TAB: folder save extract tab of single category list pages.
   -   LOG: folder save log when download site.
   
###  2.2. Download list pages and store its to LIST_MODE folder 

- When downloading single category of list page finish, to extract it by using put_html_into_tab, store list ads to **.tab** file in TAB folder. 
- When downloading all category finish,  will have full Ads **.tab** file in DELTA folder. 

###  2.3. Download all Ads

- Read project .tab file in DELTA folder and download all Ads from it. 

## 3. How to run
    
- The script is run from the directory by:
  
  ```
  * Options: 
     -x = debug  
     -y = test 
     -d YYYYmmdd = date of download.
  * Help:
      ./download_site.sh -h
  ```
### Example of download strategies
        
-   Normal FULL download:
      
      ``` ./download -zVN_DOTHINET -d{_date_store_} -x ```
    
- Daily download ( previous day is yesterday ):
    
     ```./download -zVN_DOTHINET -d{_date_store_} -x -D```
     
```
- In order to save time of download , the strategy is the following :
1. we perform a FULL download in LIST mode
2. we compare the data with the previous download (day before)
3. we ONLY download in DETAIL mode the ads which are either new (ID_CLIENT not seen the previous day) or modified (same ID_CLIENT with some changes)
```
    
- Testing download ( download 2 single category and 2 pages of list pages for testing )
     
    ``` ./download -zVN_DOTHINET -d{_date_store_} -x -y ```
    
- Download Ads from project .tab only ( don't download list pages ):
    
     ```./download -zVN_DOTHINET -d{_date_store_} -x -r```
    
- Parsing only ( don't download anything just parse ):
    
    ```./download -zVN_DOTHINET -d{_date_store_} -x -a```



