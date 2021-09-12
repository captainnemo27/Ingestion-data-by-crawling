#!/usr/bin/env bash
#
#Include libraries
source ../common/db_config.sh
source ../Lib_Offy/Utils.sh


work_dir=$(pwd)
lib_dir="../Lib_Offy"
TAB="	"
today=$(date +"%Y-%m-%d")
d="20200101"
if [ $1 != "" ]; then
   d=$1
 else
   echo "Parsing update: Missed input"
   exit 1
fi
#######################################
# Parsing data to update data
#
# Globals:
#   TABLE_NAME
#   AWK_FOLDER
#   ALL_FOLDER
# Arguments:
#   date folder
#######################################
folder_name="${d}"
FOLDER="${work_dir}/${folder_name}"
ALL_FOLDER="${FOLDER}/ALL"
DELTA_FOLDER="${FOLDER}/DELTA"
AWK_FOLDER="${work_dir}/awk"
TABLE_NAME="BATDONGSANCOMVN"
update_file="${DELTA_FOLDER}/ads_update.sql"


if [ -s "${update_file}" ]; then
    rm -f "${update_file}"
fi

standardized_all_files_in_folder ${ALL_FOLDER}

while read line; do
    ads="${line}"
    id_client=$(basename "${ads}")
    id_client="${id_client//[^0-9]/}"

    echo "== parsing update: $(basename ${id_client})"
    awk -vid_client="${id_client}" \
        -vcreated_date="${today}" \
        -vtable=${TABLE_NAME} \
        -f ${lib_dir}/Utils.awk \
        -f ${AWK_FOLDER}/all_html.awk \
        "${ads}" >> "${update_file}"
done < <(find "${ALL_FOLDER}" -type f)

echo "DONE"