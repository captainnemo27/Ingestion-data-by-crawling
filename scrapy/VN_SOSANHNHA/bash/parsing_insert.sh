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
delta_folder="${folder}/DELTA"
insert_file=${delta_folder}/ads_insert.sql
tab_file="${folder}/DELTA/extract.tab"

#Define MYSQL
database="REAL_ESTATE_VN"
table_name="SOSANHNHA"

touch $insert_file

if [ -s $tab_file ]; then
	echo "Parsing list mode"
	# Remove database file if exist
	if [ -s "$insert_file" ]; then
		rm "$insert_file"
	fi

	awk -v table="${table_name}" -vDATE=${created_date} -f ../common/Utils.awk -f ${awk_dir}/put_tab_to_db.awk $tab_file > $insert_file
fi

echo "done!"



