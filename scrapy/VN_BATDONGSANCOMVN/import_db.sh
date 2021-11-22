#!/bin/bash
set -x

work_dir=$(pwd)

if [ "X${1}" = "X" ]
then
        d=$(date +"%Y%m%d")
else
        d=$1
fi

source ../common/db_config.sh "${d}"

insert_file="${work_dir}/${d}/DELTA/ads_insert.sql"
update_file="${work_dir}/${d}/DELTA/ads_update.sql"
# From 08/2021, change to use server 227
if [[ $d > 2021-07-31 ]]; then
  DB_HOST_IMPORT=$DB_HOST_227
else
  DB_HOST_IMPORT=$DB_HOST    
fi

mysql -h $DB_HOST_IMPORT -u $DB_USERNAME "$DB_NAME" < $insert_file
mysql -h $DB_HOST_IMPORT -u $DB_USERNAME "$DB_NAME" < $update_file

echo "Finished Importing DB!"

