#!/bin/bash
. ../common/list_useragent.sh
. ../common/Utils.sh
. ../common/db_config.sh

if [ $1 != "" ]; then
  d=$1
else
  echo "Parsing update: Missed input"
fi

#Declare variable
created_date=$(date +"%Y-%m-%d")
work_dir=`pwd`
folder=${work_dir}/${d}
awk_dir="${work_dir}/awk"
all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
update_folder="${folder}/UPDATE"
update_file=${delta_folder}/ads_update.sql
tab_file="${folder}/DELTA/extract.tab"

mkdir -p $update_folder

#Define MYSQL
database="REAL_ESTATE_VN"
table_name="PROPZYVN"

echo "Parsing detail mode"

# Remove database file if exist
if [ -s "$update_file" ]; then
	rm "$update_file"
fi

for file_name in ${all_folder}/*.html; do
	ads_id=$(echo "$file_name" | awk '{gsub(".html","",$0); split($0,ar,"ALL/"); split(ar[2],arr,"-"); print arr[length(arr)]}')
  if [ ! -s "${update_folder}/ads_update_"$ads_id".sql" ]; then
    cat $file_name | awk -vtable="${table_name}" -vid=${ads_id} -vDATE=${created_date} -f ../common/Utils.awk -f ${awk_dir}/get_ads_details.awk > "${update_folder}/ads_update_"$ads_id".sql"
  fi
done

printf '%s\0' ${update_folder}/*.sql | xargs -0 cat > $update_file

if [ -d "${update_folder}" ]; then
    rm -rf "${update_folder}"
fi

echo "done!"



