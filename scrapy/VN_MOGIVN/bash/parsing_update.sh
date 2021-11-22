#!/bin/bash
set -x
source ../common/Utils.sh

work_dir=$(pwd)

if [[ $1 != "" ]]; then
  d=$1
else
  echo "Parsing insert: Missed input"
fi

# Define
table_name="MOGIVN"
site_name="mogivn"
today=`date +"%Y-%m-%d"`
# 2020-11-20
folder="${work_dir}/${d}"
all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
update_sql_file="${delta_folder}/VO_ANNONCE_update.sql"

rm -rf "${update_sql_file}"

echo "CREATE UPDATE SQL FILE"

find ${all_folder} -type f -name "annonce_*.txt" -exec python3 ../real-estate-crawl/realestatevn/python-parser/real_estate_data_parser.py {} ../real-estate-crawl/realestatevn/configs/mogivn.yml \; > "${update_sql_file}"
