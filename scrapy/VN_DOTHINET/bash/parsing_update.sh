#!/bin/bash
set -x
source ../common/Utils.sh

work_dir=$(pwd)

if [[ $1 != "" ]]; then
  d=$1
else
  echo "Parsing insert: Missed input"
fi

if [[ $2 != "" ]]; then
    tab_file=$2
else
    tab_file="${work_dir}/${d}/DELTA/extract.tab"
fi
today=`date +"%Y-%m-%d"`
# Define
db_name="REAL_ESTATE_VN"
table_name="DOTHINET"
site_name="dothinet"
folder="${work_dir}/${d}"
all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
tab_file="${delta_folder}/extract.tab"
update_sql_file="${delta_folder}/VO_ANNONCE_update.sql"
awk_dir="${work_dir}/awk"

rm -rf "${update_sql_file}"

echo "CREATE UPDATE SQL FILE"

find ${all_folder} -type f -name "annonce_*.txt" -exec python3 ../real-estate-crawl/realestatevn/python-parser/real_estate_data_parser.py {} ../real-estate-crawl/realestatevn/configs/dothinet.yml \; > "${update_sql_file}"
