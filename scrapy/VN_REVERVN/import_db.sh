#!/bin/bash
set -x

work_dir=$(pwd)
if [ "X${1}" = "X" ]
then
        date=$(date +"%Y%m%d")
else
        date=$1
fi

source ../common/db_config.sh "${date}"


insert_file="${work_dir}/${date}/DELTA/ads_insert.sql"
update_file="${work_dir}/${date}/DELTA/ads_update.sql"
mysql -h $DB_HOST -u $DB_USERNAME "$DB_NAME" < $insert_file
mysql -h $DB_HOST -u $DB_USERNAME "$DB_NAME" < $update_file