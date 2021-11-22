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
update_file="${DELTA_FOLDER}/ads_update.sql"


find "${ALL_FOLDER}" -type f -exec python3 ../real-estate-crawl/realestatevn/python-parser/real_estate_data_parser.py {} ../real-estate-crawl/realestatevn/configs/revervn.yml \; > "${update_file}"

echo "DONE!"