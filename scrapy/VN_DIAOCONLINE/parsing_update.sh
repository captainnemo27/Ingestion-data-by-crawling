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
update_file="${DELTA_FOLDER}/ads_update.sql"


if [ -s "${update_file}" ]; then
    rm -f "${update_file}"
fi

find "${ALL_FOLDER}" -type f -name 'ads_*.txt' -exec python3 ../real-estate-crawl/realestatevn/python-parser/real_estate_data_parser.py {} ../real-estate-crawl/realestatevn/configs/diaoconline.yml \; > "${update_file}"

echo "DONE!"