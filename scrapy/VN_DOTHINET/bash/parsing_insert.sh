#!/bin/bash
set -x
source ../common/Utils.sh

work_dir=$(pwd)

if [[ $1 != "" ]]; then
  folder=${work_dir}/$1
else
  echo "Parsing insert: Missed input"
fi

if [[ $2 != "" ]]; then
    tab_file=$2
else
    tab_file="${folder}/DELTA/extract.tab"
fi

# Define
today=`date +"%Y-%m-%d"`
db_name="REAL_ESTATE_VN"
table_name="DOTHINET"
site_name="dothinet"
awk_dir="${work_dir}/awk"

insert_file="${folder}/DELTA/VO_ANNONCE_insert.sql"

# Parsing
awk -vsite=${site_name} -vtable="${table_name}" -f "${awk_dir}/list_tab.awk" -f "${awk_dir}/put_tab_into_db.awk" "${tab_file}" > "${insert_file}"

echo "DONE!"
