#!/bin/bash
set -x
source ../common/Utils.sh

work_dir=$(pwd)

if [[ $1 != "" ]]; then
    d=$1
else
    echo "Parsing insert: Missed input"
fi

if [[ $2 != "" ]]; then
    tab_file=$2
else
    tab_file="${work_dir}/${d}/DELTA/extract.tab"
fi

# Define
#today=`date +%Y-%m-%d`
#today=`date +"%Y-%m-%d"`
# 2020-11-20
today="${d:0:4}-${d:4:2}-${d:6:2}"
table="_${d:0:4}_${d:4:2}"
# db_name="REAL_ESTATE_VN"
table_name="MOGIVN"
site_name="mogivn"
insert_file="${work_dir}/${d}/DELTA/VO_ANNONCE_insert.sql"
awk_dir="${work_dir}/awk"

main(){
    echo "BEGIN CREATE INSERT SQL"

    # sort tab file
    sort -u "${tab_file}" -o "${tab_file}"
    remove_duplicated_lines "${tab_file}"

    # project_tab_file="${work_dir}/extract.tab"
    # insert_tab_file="${work_dir}/${d}/DELTA/extract_insert.tab"
    # if [ -s "${project_tab_file}" ];then
    #     join -t "$(printf '\t')" "${tab_file}" "${project_tab_file}" -v 1 > "${insert_tab_file}"
    # else
    #     cp "${tab_file}" "${insert_tab_file}"
    # fi
    # cat "${insert_tab_file}" >> "${project_tab_file}"

    # Parsing
    awk -vsite=${site_name} -vcreated_day=$today -vtable="${table_name}" -f "${awk_dir}/list_tab.awk" -f "${awk_dir}/put_tab_into_db.awk" "${tab_file}" > "${insert_file}"

    echo "DONE!"
}
main
