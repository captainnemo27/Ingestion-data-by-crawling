# Crawling TINBATDONGSAN (site tinbatdongsan.com)

## Objectives

Download and parse data from TINBATDONGSAN using bash script & awk

## Workflow

**Step 1:** Create folder to save:

    - ALL: folder save all Ads html file.
    - DELTA: folder save 2 file sql (ads_insert.sql and ads_update.sql)
    and extract.tab and need_download.tab file.
    - LIST_MODE: folder save html file of list page.
    - LOG: folder contain all log files.

**Step 2:** Download list pages and store its to LIST_MODE folder. When download
all category finish, we will have full project extract.tab file in DELTA folder.
Due to the page content get repeated if the page number > 101, we use the following
strategy crawling as below.

    - Strategy:
        1. Filter the each category by following criteria in order,
        [city -> district -> ward] one criteria each time
        2. After the filter, if page number N > 101, then go back to step 1 to
        process next criteria, else proceed.
        3. Perform step as in Logic section.

        * Note: Read function get_link for more technical info

    - Logic:
        1. Download first index-page html file
        2. Extract total number of index-pages N need to download,
        3. Download all index-pages html file (from page 1 to N) and store it
        in LIST_MODE folder
        3. Parsing the neccessary data from all page-index html file and save it
        to extract tab.

**Step 3:** Download detail pages by reading need_download.tab file in DELTA folder
and download all Ads from it.

    - Logic:
        1. Find the extract.tab of most recent download date.
        2. Compare extract.tab file of today and most recent date, to find the ads
        need to download (need_download_ads = nb_ads_today - nb_ads_most_recent_date)
        and store it in need_download.tab in DELTA folder
        3. From need_download.tab, download all the ads page and store its
        html file to ALL folder

**Step 4:** Parse the crawling data and save to ads_insert.sql (from extract.tab)
and ads_update.sql (from html file in ALL folder) and store in DELTA folder.

**Step 5:** Transfer sql file to server and import sql to database. When all
processes finish, status_ok file is created in DELTA folder to confirm that there is no error.

## How to run

**Fully download + Import:**
    ./download_site.sh -zVN_TINBATDONGSAN -d{_date_store_} -x -i > log{_date_store_} 2>&1 &

**Daily download + Import:**
    ./download_site.sh -zVN_TINBATDONGSAN -x -D -i > log{_date_store_} 2>&1 &

**Testing download ( download 2 each category and 2 pages of list pages)**
    ./download_site.sh -zVN_TINBATDONGSAN -d{_date_store_} -x -y -i > log{_date_store_} 2>&1 &

## Team

## License
