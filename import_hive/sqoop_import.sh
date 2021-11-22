#!/bin/bash

work_dir=$(pwd)

month=$1
function download_page {
  table_list=$1
  MAX_LOOP=4
  year=2021
  while FS='\t' read -r -a array; do
    table="${array[0]}"
    db="${array[1]}"
#    echo ${db} ${table} #_CLEAN_${year}_${month}
    sqoop import --connect jdbc:mysql://${db}/VN_REAL_CLEAN_${year}_${month} \
    --username root \
    --password 123456789 \
    --table ${table} \
    -m 1 --hive-import \
    --create-hive-table \
    --hive-table CLEAN_${year}_${month}.${table}_${year}_${month} \
    --target-dir /user/hive/warehouse/CLEAN/${table}_${year}_${month} \
    --fields-terminated-by "\t" \
    --map-column-hive DATE_ORIGINAL=date \
    --map-column-hive CREATED_DATE=date \
    --map-column-hive ADS_DATE=date 
    echo 'DONE FOR DATABASE: ' CLEAN_${year}_${month} '|  TABLE: ' ${table}_${year}_${month}

done < "${table_list}"
}
TAB_FILE="${work_dir}/table_clean.tab"
download_page ${TAB_FILE}
echo '====================== DONE =========================='