#!/usr/bin/env bash


#######################################
# Parsing ads html and create sql file 
# to update
#
# Globals:
#   ALL_FOLDER
# Arguments:
#   date folder
#######################################

work_dir=$(pwd)

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


find "${ALL_FOLDER}" -type f -exec python3 ../real-estate-crawl/realestatevn/python-parser/revervn_insert.py {} ../real-estate-crawl/realestatevn/configs/revervn.yml \; > "${insert_file}"

echo "DONE!"