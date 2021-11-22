#!/usr/bin/env bash
#
#Include libraries
source ../common/db_config.sh
source ../Lib_Offy/Utils.sh


work_dir=$(pwd)
d="20200101"
if [ $1 != "" ]; then
   d=$1
 else
   echo "Parsing update: Missed input"
   exit 1
fi
#######################################
# Parsing data to update data
#
# Globals:
#   TABLE_NAME
#   ALL_FOLDER
# Arguments:
#   date folder
#######################################
folder_name="${d}"
FOLDER="${work_dir}/${folder_name}"
ALL_FOLDER="${FOLDER}/ALL"
DELTA_FOLDER="${FOLDER}/DELTA"
AWK_FOLDER="${work_dir}/awk"
update_file="${DELTA_FOLDER}/ads_update.sql"


find ${ALL_FOLDER} -type f -name "ads*.txt" -exec python3 ../real-estate-crawl/realestatevn/python-parser/real_estate_data_parser.py {} ../real-estate-crawl/realestatevn/configs/batdongsancomvn.yml \; > "${update_file}"
echo "DONE"