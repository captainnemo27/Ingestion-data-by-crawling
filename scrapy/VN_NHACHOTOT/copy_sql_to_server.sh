#!/bin/bash
set -x

work_dir=$(pwd)

if [[ $1 != "" ]]; then
    d=$1
else
    echo "Parsing insert: Missed input"
fi

user_name="itdev"
host="172.16.0.167"

table_name="NHACHOTOT"
database="REAL_ESTATE_VN"

date=$(date +%Y%m%d)
# date=20200812

insert_file="${work_dir}/${date}/DELTA/VO_ANNONCE_insert.sql"

server_folder="~/SQL/${table_name}/${date}"
server_insert_file="${server_folder}/VO_ANNONCE_insert.sql"
server_insert_file_log="${server_folder}/log_insert"

echo $insert_file
echo $server_folder
main(){
    # Access to server by using key and create folder to save sql file
    ssh -i ../common/offy-oreal-key-rsa "${user_name}"@"${host}" "mkdir -p ~/SQL/${table_name} && mkdir -p ${server_folder} && exit"

    # Tranfer file to server
    scp -i ../common/offy-oreal-key-rsa "${insert_file}" "${user_name}"@"${host}":"${server_insert_file}"

    # Import SQL to DATABASE
    ssh -i ../common/offy-oreal-key-rsa "${user_name}"@"${host}" "\
    mysql -uroot -p123456789 ${database} < ${server_insert_file} && \
    exit"
}
main