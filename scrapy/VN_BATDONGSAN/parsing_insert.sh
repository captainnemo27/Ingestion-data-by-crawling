#!/usr/bin/env bash
#
# Perfom crawling and parsing data from batdongsan.vn

#Include libraries
source ../common/db_config.sh
source ../Lib_Offy/Utils.sh

work_dir=$(pwd)
lib_dir="../Lib_Offy"
TAB="	"

today=$(date +"%Y-%m-%d")
d="20200101"
if [ $1 != "" ]; then
   d=$1
 else
   echo "Parsing update: Missed input"
   exit 1
fi

folder_name="${d}"
FOLDER="${work_dir}/${folder_name}"
DELTA_FOLDER="${FOLDER}/DELTA"
AWK_FOLDER="${work_dir}/awk"
LIST_FOLDER="${FOLDER}/LIST_MODE"
TABLE_NAME="BATDONGSAN"
insert_file="${DELTA_FOLDER}/ads_insert.sql"
TAB_FILE="${DELTA_FOLDER}/extract.tab"


function create_extract_tab {
    if [ -s "${TAB_FILE}" ]; then
        rm -f "${TAB_FILE}"
    fi
    while read line; do
        page_html="${line}"
        echo "== parsing insert: $(basename ${page_html})"

        sale_type="SALE"
        if [[ "${page_html}" == *"rent"* ]]; then
            sale_type="RENT"
        fi

        awk -vcreated_day=$today -vsale_type="${sale_type}" \
            -f ${lib_dir}/Utils.awk \
            -f ${AWK_FOLDER}/list_tab.awk \
            -f ${AWK_FOLDER}/put_html_into_tab.awk \
            "${page_html}" >> "${TAB_FILE}.$$"

    done < <(find "${LIST_FOLDER}" -type f -name '*.html')

    # sort unique to remove double lines
    sort -u -k1,1 -t"${TAB}" "${TAB_FILE}.$$" -o "${TAB_FILE}"
    rm -rf "${TAB_FILE}.$$"
}

create_extract_tab

awk -vtable=${TABLE_NAME} -vcreated_day="${today}" \
            -f ${AWK_FOLDER}/list_tab.awk \
            -f ${AWK_FOLDER}/put_tab_into_db.awk \
            "${TAB_FILE}" > "${insert_file}"


echo "DONE!"