#!/bin/bash
#Include libraries
. ../Lib_Offy/list_useragent.sh

work_dir=`pwd`
date=$(date +%Y%m%d)
mode_debug=0
mode_test=0
download_site=0
insert_db=0
while getopts ":xyrid:" opt; do
  case ${opt} in
    d )
      d="$OPTARG"
      if [ "${d}" = "-x" ]; then
        mode_debug=1
      fi
      if [ "${d}" = "-y" ]; then
        mode_test=1
      fi
	  if [ "${d}" = "-r" ]; then
        download_site=1
      fi
	  if [ "${d}" = "-i" ]; then
        insert_db=1
      fi
      if [ "${d}" != "-x" ] && [ "${d}" != "-y" ] && [ "${d}" != "-r" ] && [ "${d}" != "-i" ] ; then
        date=$d
      fi
      ;;
    x )
      mode_debug=1
      ;;
    y )
      mode_test=1
      ;;
    r )
      download_site=1
      ;;
    i )
      insert_db=1
      ;;
    \? )
      echo "Invalid Option: -$OPTARG" 1>&2
    #   exit 1
      ;;  
  esac
done       


#################################
# DEFINE FOLDER TO SAVE         #
#################################
folder="${work_dir}/${date}"
log_folder="${folder}/LOG"
all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
list_folder="${folder}/LIST_MODE"
python_dir="${work_dir}/python"
spider_dir="${work_dir}/python/download_site/download_site/spiders"
sale_folder="${list_folder}/mua"
lease_folder="${list_folder}/thue"

mkdir -p "${folder}" "${all_folder}" "${delta_folder}" "${list_folder}" "${log_folder}" "${sale_folder}" "${lease_folder}"


#################################
# CREATE DATE.TXT AND           #
# OPTION_FILE.TXT               #
#################################

echo $date > $folder/date.txt

if [ "${mode_debug}" = 1 ]; then
  set -x
fi

case "$mode_test" in
        0)
            echo "FULL DOWNLOAD"
            echo "0" > $folder/option_file.txt
        ;;
        1)
            echo "TESTING DOWNLOAD WITH 2 SITES"
            echo "1" > $folder/option_file.txt
        ;;
esac  
    
#################################
# MAIN                          #
#################################
main(){
    #====================== DOWNLOAD_SITE =======================
    if [ "${download_site}" = 0 ]; then
	python3 ${python_dir}/get_max_page_number.py $date 
  	cd python/download
	scrapy crawl -a argument=$date download_site --logfile ${log_folder}/annonce_site.log
	cd .. && cd ..			
    fi
    #============== CREATE LIST ID AND COMPARE DATA =============
    python3 ${python_dir}/create_listid.py $date
    python3 ${python_dir}/compare_data.py $date		
    #====================== DOWNLOAD_ADS  =======================
    # cd python/download
    # scrapy crawl -a argument=$date download_ads --logfile ${log_folder}/annonce_ads.log
    # cd .. && cd ..
    #====================== PARSING DATA ========================
    python3 ${python_dir}/put_json_into_delta.py $date
    #====================== IMPORT DATABASE =====================
    if [ "${insert_db}" = 1 ]; then
    	./import_db.sh "$date"
    fi
    echo "DONE COMPLETE PROGRAM"
    touch $delta_folder/status_ok.txt
    if [ -s $delta_folder/list_id.txt ]; then
	echo "ok" > $delta_folder/status_ok.txt
    else        
	echo "fail" > $delta_folder/status_ok.txt
    fi
}
main 2>&1 | tee -a ${log_folder}/annonce.log