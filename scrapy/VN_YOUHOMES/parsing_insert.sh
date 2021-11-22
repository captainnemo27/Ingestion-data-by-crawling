#!/usr/bin/env bash
#

work_dir=$(pwd)


#######################################
# Parsing data to update data
#
# Globals:
#   TABLE_NAME
#   AWK_FOLDER
#   ALL_FOLDER
# Arguments:
#   $1 date folder
#######################################
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
ALL_FOLDER="${FOLDER}/ALL"
DELTA_FOLDER="${FOLDER}/DELTA"
insert_file="${DELTA_FOLDER}/ads_insert.sql"

if [ -s "${insert_file}" ]; then
    rm -f "${insert_file}"
fi

find "${ALL_FOLDER}" -type f -name '*.html' -exec python3 ../real-estate-crawl/realestatevn/python-parser/youhomes_insert.py {} ../real-estate-crawl/realestatevn/configs/youhomes.yml \; > "${insert_file}"

echo "DONE!"