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


mysql -h $DB_HOST -u $DB_USERNAME "$DB_NAME" < $insert_file
mysql -h $DB_HOST -u $DB_USERNAME "$DB_NAME" < $update_file

echo "Finished Importing DB!"

