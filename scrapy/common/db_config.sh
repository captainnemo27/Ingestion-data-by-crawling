#!/bin/bash

# the first argument is the date format YYYYmmdd
if [ "X${1}" = "X" ]
then
        d=$(date +"%Y%m%d")
else
        d=$1
fi
DB_HOST="172.16.0.167"
DB_HOST_227="172.16.0.227"

# From 08/2021, change to use DB monthly
if [[ $d > 2021-07-31 ]]; then
    DB_NAME="VN_REAL_RAW_${d:0:4}_${d:4:2}"
    DB_CLEAN_NAME="VN_REAL_CLEAN_${d:0:4}_${d:4:2}"
else
    DB_NAME="REAL_ESTATE_VN"
    DB_CLEAN_NAME="VN_REAL"
fi
DB_USERNAME="openreal"
BACKUP_DIR="/home/itdev/backup_autobiz_data/DAILY"

if [ ! -s ~/.my.cnf ];then
   cp ../common/.my.cnf ~/	
fi

echo "Finished Database configuration"
