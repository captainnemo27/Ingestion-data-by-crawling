#!/bin/bash
. ../common/list_useragent.sh
. ../common/Utils.sh
. ../common/db_config.sh

if [ $1 != "" ]; then
  d=$1
else
  echo "Parsing insert: Missed input"
  exit
fi

#Declare variable
created_date=`date +"%Y-%m-%d"`
work_dir=`pwd`
folder=${work_dir}/${d}
awk_dir="${work_dir}/awk"
all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
update_folder="${folder}/UPDATE"
update_file="${delta_folder}/ads_update.sql"
tab_file="${folder}/DELTA/extract.tab"

mkdir -p $update_folder

#Define MYSQL
table_name="SOSANHNHA"

echo "Parsing detail mode"

# Remove database file if exist
if [ -s "$update_file" ]; then
	rm "$update_file"
fi

find "${all_folder}" -type f -name "*.html" -exec awk -vtable="${table_name}" -vDATE=${created_date} -f ../common/Utils.awk -f ${awk_dir}/decode_hex.awk -f ${awk_dir}/get_ads_details.awk  {} \; > "${update_file}"


echo "done!"



