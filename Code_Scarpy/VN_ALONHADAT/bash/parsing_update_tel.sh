#!/bin/bash
. ../common/list_useragent.sh
. ../common/Utils.sh
. ../common/db_config.sh

if [ $1 != "" ]; then
  d=$1
else
  echo "Parsing update: Missed input"
  exit 1
fi

#Declare variable
created_date=`date +"%Y-%m-%d"`
work_dir=`pwd`
folder=${work_dir}/${d}
awk_dir="${work_dir}/awk"
all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
tel_folder="${all_folder}/TEL"
update_tel_folder="${folder}/UPDATE_TEL"
update_file_tel="${delta_folder}/tel_ads_update.sql"
tel_list_need_to_download="${delta_folder}/list_id_tel.txt"
tab_file="${folder}/DELTA/extract.tab"

mkdir -p $update_tel_folder

#Define MYSQL
database="REAL_ESTATE_VN"
table_name="ALONHADAT"

echo "Parsing detail mode telephone"

# Remove database file if exist
if [ -s "$update_file_tel" ]; then
	rm "$update_file_tel"
fi

if [ -s "$tel_list_need_to_download" ]; then
  while read -r line; do
    FS='\t' read -r -a array <<< "$line"
    ads_id="${array[0]}"
    ads_url="${array[1]}"
    dealer_id=$(echo "$ads_url" | awk '{gsub(".html","",$0); split($0,ar,"nha-moi-gioi/"); print ar[2]}')
    
    file_ads_tel=${tel_folder}/${dealer_id}.html
    
    if [ -s "$file_ads_tel" ]; then
      cat $file_ads_tel | awk -vtable="${table_name}" -vADS_ID=${ads_id} -vDATE=${created_date} -f ../common/Utils.awk -f ${awk_dir}/get_ads_tel.awk > "${update_tel_folder}/tel_ads_update_"$ads_id".sql"
    fi
  done < ${tel_list_need_to_download}
else
  for file_name in ${tel_folder}/*.html; do
    ads_id=$(echo "$file_name" | awk '{gsub(".html","",$0); split($0,ar,"TEL/"); print ar[2]}')
    if [ ! -s "${update_tel_folder}/tel_ads_update_"$ads_id".sql" ]; then
      cat $file_name | awk -vtable="${table_name}" -vADS_ID=${ads_id} -vDATE=${created_date} -f ../common/Utils.awk -f ${awk_dir}/get_ads_tel.awk > "${update_tel_folder}/tel_ads_update_"$ads_id".sql"
    fi
  done
fi

printf '%s\0' ${update_tel_folder}/*.sql | xargs -0 cat > $update_file_tel

if [ -d "${update_tel_folder}" ]; then
    rm -rf "${update_tel_folder}"
fi

echo "done!"



