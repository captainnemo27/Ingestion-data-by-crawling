# Crawling
1. **Objective**: Download and parse data from MOGIVN using bash script & awk
2. **Workflow**
    *  **Step 1:** Create folder to save:
        -   ALL: folder save all Ads file.
        -   DELTA: folder save 2 file sql important ( insert.sql-insert new ads to database and update.sql-update ads information ) and some project *.tab file.
        -   LIST_MODE: folder save list pages.
        -   TAB: folder save extract tab of single category list pages.
        -   LOG: folder save log when download site.
    *  **Step 2:** Download list pages and store its to LIST_MODE folder. When dowload single category of list page finish, extract it by using put_html_into_tab, store list ads to .tab file in TAB folder. When download all category finish, we will have full project .tab file in DELTA folder. 
    *  **Step 3:** Read project .tab file in DELTA folder and download all Ads from it.
3. **How to run**
    * **Normal download:**
        ./download_site.sh -zVN_MOGIVN -d{_date_store_} -x
    * **Download new Ads from previous day ( check if Ads exist in last previous day, dont down it ):**
        ./download_site.sh -zVN_MOGIVN -d{_date_store_} -D{_previous_day_} -x
    * **Daily download ( previous day is yesterday ):**
        ./download_site.sh -zVN_MOGIVN -d{_date_store_} -x -l
    * **Testing download ( download 2 single category and 2 pages of list pages for testing ) - Can try with all way running above:**
        ./download_site.sh -zVN_MOGIVN -d{_date_store_} -y

    * **Download Ads from project .tab only ( don't download list pages ):**
        ./download_site.sh -zVN_MOGIVN -d{_date_store_} -x -r
    * **Parsing only ( don't download anything just parse ):**
        ./download_site.sh -zVN_MOGIVN -d{_date_store_} -x -a
4. **Team**
5. **License**

