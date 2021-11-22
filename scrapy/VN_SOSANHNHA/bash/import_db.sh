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

mysql -h $DB_HOST_227 -u $DB_USERNAME "$DB_NAME" --binary-mode -o < $insert_file
mysql -h $DB_HOST_227 -u $DB_USERNAME "$DB_NAME" --binary-mode -o < $update_file

echo "Finished Importing DB!"

