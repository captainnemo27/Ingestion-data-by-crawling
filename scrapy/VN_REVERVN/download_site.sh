#!/bin/bash
#Include libraries
. ../Lib_Offy/list_useragent.sh

work_dir=`pwd`
lynx_ind=1
get_all_ind=1
mode_test=0
mode_import=0
delta_ind=0

while getopts :-ad:rhxt:yz:Di name
do
    case $name in

        a)  lynx_ind=0
        ((shift=shift+1))
        ;;

        d) 	date=$OPTARG
        ((shift=shift+1))
        ;;

        D) 	delta_ind=1
        ((shift=shift+1))
        ;;

        h)  echo -e "${usage}"
        ExitProcess 0
        ;;

        r)  get_all_ind=0
        ((shift=shift+1))
        ;;

        x)  set -x
        ((shift=shift+1))
        ;;

        y) mode_test=1
        ((shift=shift+1))
        ;;

        i) mode_import=1
        ((shift=shift+1))
        ;;

        z)  ((shift=shift+1))
        ;;

        *) echo "usage: $0 [-v] [-r]" >&2
        exit 1 ;;

    esac
done
shift ${shift}

#################################
# DEFINE FOLDER TO SAVE         #
#################################
if [ "${date}X" = "X" ]
then
    date=$(date +"%Y%m%d")
fi
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

if [ ${mode_test} -eq 1 ]; then
    echo "TESTING DOWNLOAD WITH 2 SITES"
		echo "1" > $folder/option_file.txt
else	
    echo "FULL DOWNLOAD"
		echo "0" > $folder/option_file.txt
fi   

#################################
# MAIN                          #
#################################
main(){
    #====================== DOWNLOAD_SITE =======================
    if [ ${lynx_ind} -eq 1 ] && [ ${get_all_ind} -eq 1 ]; then
	    python3 ${python_dir}/get_max_page_number.py $date
  	  cd python/download
	    scrapy crawl -a argument=$date download_site --logfile ${log_folder}/annonce_site.log
	    cd .. && cd ..			
    fi
    #============== CREATE LIST ID AND COMPARE DATA =============
    python3 ${python_dir}/create_listid.py $date
    # Run if the daily mode is enable
    if [ ${delta_ind} -eq 1 ]; then
      python3 ${python_dir}/compare_data.py $date		
    else
      cp $delta_folder/list_id.txt $delta_folder/list_new_id.txt
    fi
    #====================== DOWNLOAD_ADS  =======================
    if [ ${lynx_ind} -eq 1 ] || [ ${get_all_ind} -eq 0 ]; then
      cd python/download
      scrapy crawl -a argument=$date download_ads --logfile ${log_folder}/annonce_ads.log
      cd .. && cd ..
    fi
    #====================== PARSING DATA ========================
    #python3 ${python_dir}/put_html_into_delta.py $date
    ./parsing_insert.sh "$date"
    ./parsing_update.sh "$date"
    #====================== IMPORT DATABASE =====================
    if [ "${mode_import}" -eq 1 ]; then 
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