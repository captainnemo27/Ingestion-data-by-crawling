#!/bin/bash

#Include other functions
source ./bash/utils.sh

#################################
# IMPORT TEMPLATE               #
#################################
template

#################################
# PARSE OPTION                  #
#################################
# usage / mode d'emploi du script
usage="download_site.sh\n\
\t-a no download - just process what's in the directory\n\
\t-d [date] (default today)\n\
\t-D daily mode\n\
\t-h help\n\
\t-r retrieve only, do not download the detailed adds\n\
\t-x debug mode - verbose ligne par ligne\n\
\t-y mode TEST telecharge 2 pages seulement \n\
\t-i import to database \n\
\t-z nom du site - optionnel juste utile pour savoir ce qui tourne lorsqu'on fait \"ps\" \n\
"
TAB=" "
lynx_ind=1
get_all_ind=1
mode_test=0
delta_ind=0
import_db=0
site="VN_DOTHINET"
today=`date +"%Y-%m-%d"`

while getopts :-aDd:hrxt:yiz: name
do
  case $name in

    a)  lynx_ind=0
    ((shift=shift+1))
	;;

    d) d=$OPTARG
    ((shift=shift+1))
	;;
    D)  delta_ind=1
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
    i) import_db=1
    ((shift=shift+1))
	;;

    z)  ((shift=shift+1))
	;;

    *) echo "usage: $0 [-v] [-r]" >&2
    exit 1 ;;

  esac
done
shift ${shift}

# If the input day is empty : mean is download daily
if [ "${d}X" = "X" ]
then
	d=`date +"%Y%m%d"`
fi

folder_name="${d}"
source ../common/db_config.sh "${d}"
#Define some folders
folder="${work_dir}/${folder_name}"
tab_file="${folder}/DELTA/extract.tab"
tab_folder="${folder}/TAB"
all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
list_folder="${folder}/LIST_MODE"
cookie_file="${folder}/cookie.txt"
awk_dir="${work_dir}/awk"
bash_dir="${work_dir}/bash"

##################################################
# Define all download functions                  #
##################################################
function check_max_process(){
    # Make downloading async
    local process_max=$1
    while [ "${#list_process_pids[@]}" -gt "${process_max}" ]; do
      for i in "${!list_process_pids[@]}" ; do # loop key in listProcessPids
          # Check the pid done or not
        if ! kill -0 "${list_process_pids[${i}]}" # The pid is gone
        then
            unset "list_process_pids[${i}]" # Remove the pid out of the listProcessPids
        fi
      done
      if [ "${#list_process_pids[@]}" -lt "${process_max}" ]; then
        break
      fi
      sleep 1
    done
}

function get_district() {

   mkdir -p ${folder}/LOCATION 
   while read -r line;do
      FS='\t' read -r -a array <<< "$line"
      city_code="${array[0]}"
      city_name="${array[1]}"
      list_dist=()
      
      if [ ${#city_code} -eq 0 ] || [ ${#city_name} -eq 0 ]; then
          continue
      fi
      if [ ${city_code} == "SG" ];then
        city_name="tp-hcm"
      fi
      # Get district
      url="https://dothi.net/Handler/SearchHandler.ashx?module=GetDistrict&cityCode=${city_code}"
      district_json="${folder}/LOCATION/district_${city_code}.json"
      flag_city=""
      if [ ${city_code} != "SG" ] && [ ${city_code} != "HN" ]
      then
          flag_city=${city_code}
      fi

      if [ ! -s ${district_json} ]; then
          incr_ip
          wget --bind-address="${PROXY_ARR[$id_proxies]}" -nv  --timeout=60 --tries=5 --waitretry=1 -U"${USERAGENT_ARR[$u_a]}" --random-wait --keep-session-cookies --save-cookies=${work_dir}/${d}/cookies.$$ -q -O- --header="Accept-Encoding: gzip" "${url}" | gzip -cdf > "${district_json}"
      fi
      python ${work_dir}/get_list_from_json.py ${district_json} ${flag_city} >> ${work_dir}/locations.tab
            
  done < ${work_dir}/cities.tab  

}
function download_list_mode_by_locations(){
    # Declare some local variables
    local page_param="p"
    categories=(sale rent)
    land_type=()
    local district_name
    local k_n
    local land
    ##############################

    if [ ! -s ${work_dir}/locations.tab ]; then
      get_district
    fi

    # # shellcheck disable=SC2068
    for key in "${!categories[@]}"; do
	      k_n=${categories[$key]}
        if [ ${k_n} == "sale" ];then
            land_type=(ban-can-ho-chung-cu ban-nha-rieng ban-nha-biet-thu-lien-ke ban-nha-mat-pho ban-dat-nen-du-an ban-dat ban-trang-trai-khu-nghi-duong ban-kho-nha-xuong ban-loai-bat-dong-san-khac)
        else
            land_type=(cho-thue-can-ho-chung-cu cho-thue-nha-rieng cho-thue-nha-mat-pho cho-thue-nha-tro-phong-tro cho-thue-van-phong cho-thue-cua-hang-ki-ot cho-thue-kho-nha-xuong-dat cho-thue-loai-bat-dong-san-khac)
        fi
        
        for i in "${!land_type[@]}"; do
            cat_folder="${1}/${k_n}"
            mkdir -p ${cat_folder}
            land=${land_type[$i]}

            while read -r line;do
                FS='\t' read -r -a array <<< "$line"
                district_name="${array[0]}"
                page_current=1
                stop_down=0

                if  [ ${#district_name} -eq 0  ]; then
                  continue
                fi
                # Dowload first page  
                url="${2}/${land}-${district_name}/${page_param}${page_current}.htm"
                # Local file: nha-dat-cho-thue-p1.html
                html_file="${cat_folder}/page-${land}-${district_name}-${page_param}${page_current}.html"  
                download_sub  "$url" "$html_file" "listProductSearch"
                if [ -s $html_file ]; then
                        grep -q -i "ContentPlaceHolder1_ProductSearchResult1_pnlNotFound" "$html_file"
                        if [ $? -eq 0 ]; then
                            stop_down=1
                        fi
                fi  
                while [ ${stop_down} -ne 1 ]; do
                    let "page_current=page_current + 1"
                    # Url: https://dothi.net/nha-dat-cho-thue-tp-hcm/p1.htm
                    url="${2}/${land}-${district_name}/${page_param}${page_current}.htm"
                    # Local file: nha-dat-cho-thue-p1.html
                    html_file="${cat_folder}/page-${land}-${district_name}-${page_param}${page_current}.html"

                    download_sub  "$url" "$html_file" "saveProductDetail" 
                    if [ -s $html_file ]; then
                        grep -q -i "pnlNotFound" "$html_file" 
                        no_ads=$?
                        
                        grep -q -i "saveProductDetail" "$html_file"
                        if [ $? -ne 0 -o $no_ads -eq 0 ]; then
                            break
                        fi
                    fi  
                    if [ $mode_test -eq 1 -a $page_current -eq 2 -o $page_current -gt 101 ]; then
                      stop_down=1
                    fi  
                   
                done
                
  	        done < ${work_dir}/locations.tab
      done # Land type
     
    done # categories  
    # remove all draft files
    rm -rf ${work_dir}/${d}/cookies.*   
}
function download_list_mode(){
    # Declare some local variables
    local page_param="p"
    categories=(sale rent)
    local process_max=6
    land_type=()
    local k_n
    local land
    ##############################

    if [ ! -s ${work_dir}/locations.tab ]; then
      get_district
    fi

    # Remove Tab file if exist
    if [ -f "${3}" ]; then
        rm -f "${3}"
    fi

    # # shellcheck disable=SC2068
    for key in "${!categories[@]}"; do
	      k_n=${categories[$key]}
        if [ ${k_n} == "sale" ];then
            land_type=(ban-can-ho-chung-cu ban-nha-rieng ban-nha-biet-thu-lien-ke ban-nha-mat-pho ban-dat-nen-du-an ban-dat ban-trang-trai-khu-nghi-duong ban-kho-nha-xuong ban-loai-bat-dong-san-khac)
        else
            land_type=(cho-thue-can-ho-chung-cu cho-thue-nha-rieng cho-thue-nha-mat-pho cho-thue-nha-tro-phong-tro cho-thue-van-phong cho-thue-cua-hang-ki-ot cho-thue-kho-nha-xuong-dat cho-thue-loai-bat-dong-san-khac)
        fi
        
        for i in "${!land_type[@]}"; do
            cat_folder="${1}/${k_n}"
            mkdir -p ${cat_folder}
            land=${land_type[$i]}

            page_current=0
            stop_down=0

            while [ ${stop_down} -ne 1 ]; do
                let "page_current=page_current + 1"
                # Url: https://dothi.net/nha-dat-cho-thue-tp-hcm/p1.htm
                url="${2}/${land}/${page_param}${page_current}.htm"
                # Local file: nha-dat-cho-thue-p1.html
                html_file="${cat_folder}/page-${land}-${page_param}${page_current}.html"
                check_max_process $process_max
                # Conditional for stopping
                let "last_page=page_current - 1"	
                last_file="${cat_folder}/page-${land}-${page_param}${last_page}.html"
                if [ -s $last_file ]; then
                    grep -q -i "pnlNotFound" "$last_file" 
                    no_ads=$?
                    
                    grep -q -i "saveProductDetail" "$last_file"
                    if [ $? -ne 0 -o $no_ads -eq 0 ]; then
                        break
                    fi
                fi  

                
                download_sub  "$url" "$html_file" "saveProductDetail" &
                list_process_pids+=($!)
                
                if [ $mode_test -eq 1 -a $page_current -eq 2 -o $page_current -gt 101 ]; then
                  stop_down=1
                fi  
                
            done       
    
      done # Land type
      # Empty an array
      unset list_process_pids                  
         
      wait "${list_process_pids[@]}"

    done # categories

    # remove all draft files
    rm -rf ${work_dir}/${d}/cookies.*   
}


function download_detail_mode(){
    # Parameter input
    local tab_file=$1
    local process_max=10
    local file=""
    
    while read -r line;do
        FS='\t' read -r -a array <<< "$line"
        client_id="${array[0]}"
        src_link="${array[1]}"
        src_link=$(echo "${src_link}" | iconv -c -f utf-8 -t ascii)

        if [ ${#client_id} -eq 0 ] || [ ${#src_link} -eq 0 ];then
            continue; # there are not id_client or url
        fi

        file="${all_folder}/annonce_${client_id}.txt"
        # Check to kill phantomjs process which takes long time 
        check_process
        # Check full list process or not
        check_max_process $process_max

         # Take the pid and put it in the array
         if [ ! -s ${file} ]; then
            download_html "${src_link}" "${file}" &
          list_process_pids+=($!)
        fi
    done < "${tab_file}"
    # waiting all processes to complete
    wait "${list_process_pids[@]}"
    # Empty an array
    unset list_process_pids
}

#########################################################################
# MAIN FUNCTION
#########################################################################
list_process_pids=()
main(){

local domain="https://dothi.net"
local base_page_url="${domain}"
#Define MYSQL
local table_name="DOTHINET"
local site_name="dothinet"
mkdir -p "${all_folder}" "${delta_folder}" "${list_folder}"

if [ ${lynx_ind} -eq 1 ] && [ ${get_all_ind} -eq 1 ]; then
	echo "Starting to download list mode."
	download_list_mode ${list_folder} ${base_page_url} ${tab_file}
  download_list_mode_by_locations ${list_folder} ${base_page_url} ${tab_file}
  
  standardized_all_files_in_folder "${list_folder}"
  
  find "${list_folder}" -name "page-*.html" -exec awk -vcreated_day="${today}" -f "${awk_dir}/list_tab.awk" -f ../common/Utils.awk -f "${awk_dir}/put_html_into_tab.awk" {} \; >  "${tab_file}"
  cp "${tab_file}" "${tab_file}.bk"
  ### Sort and remove duplicate line fileTab ###
 	echo "Sorting and removing duplicate line ${tab_file}"
 	remove_duplicated_lines "${tab_file}"
fi


# Run if the daily mode is enable
 if [ ${delta_ind} -eq 1 ]; then
   last_folders=$(find "${BACKUP_DIR}/$site"/*/DELTA -type f ! -size 0 -name 'extract.tab' | awk '/\/[1-9][0-9]{3}[01][0-9][0-3][0-9]\//{split($0, ar, "'"${BACKUP_DIR}/$site"'/"); split(ar[2], ar, "/"); print ar[1]}')
   last_folder=""
   for fn in ${last_folders}; do	
   	if [ "${fn}" != "${d}" ]; then
       last_folder="${fn}"
     else
       break
     fi
   done
   # Create original tab file
   cp "${tab_file}" "${tab_file}.original"
   # If we have last_folder, we will need to compare the tab_file
   if [ -n "${last_folder}" ]; then
     # If last_folder is not the same with current date. Mean the script was not done.
     if [ "${last_folder}" != "${d}" ]; then
       last_folder="${BACKUP_DIR}/$site/${last_folder}"
       last_tab_file="${last_folder}/DELTA/extract.tab"
       # Pre sort
       sort -u -k1,1 -t"${TAB}" "${last_tab_file}" -o "${last_tab_file}"
       sort -u -k1,1 -t"${TAB}" "${tab_file}" -o "${tab_file}"
       # Do comparing the tab_file
       join -t"${TAB}" -v2 "${last_tab_file}" "${tab_file}" > "${tab_file}.temp"; rm -f "${tab_file}"; mv "${tab_file}.temp" "${tab_file}"
     fi
   fi
 fi



if [ ${lynx_ind} -eq 1 ] || [ ${get_all_ind} -eq 0 ]; then
  # Download via phantomjs
	  download_detail_mode ${tab_file}
  # Download via scrapy + splash
  #python3 "${work_dir}/start_crawler.py" "${d}"
  standardized_all_files_in_folder "${all_folder}"
fi





    # #######################
    # Invoke parsing data   #
    # #######################
${bash_dir}/parsing_insert.sh "${d}"
${bash_dir}/parsing_update.sh "${d}"


# Run if the daily mode is enable.
#
 if [ ${delta_ind} -eq 1 ]; then
   mv "${tab_file}" "${delta_folder}/extract_delta.tab"
   mv "${tab_file}.original" "${tab_file}"

   # If the status file is empty
   if [ ! -s "${delta_folder}/status" ]; then
     echo "1" > "${delta_folder}/status"
   else
     status=$(cat "${delta_folder}/status")
     ((status++))
     echo "${status}" > "${delta_folder}/status"
   fi
 fi


if [ $import_db -eq 1 ]; then
  ${bash_dir}/import_db.sh "${d}"
fi

echo "ok" > "${folder}/DELTA/status_ok"
echo "Finished!"
echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tEND"

ExitProcess 0
}
main
