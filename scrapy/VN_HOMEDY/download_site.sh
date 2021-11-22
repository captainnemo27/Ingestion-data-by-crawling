#!/bin/bash
#Include libraries
. ../common/list_useragent.sh
. ../common/Utils.sh
. ../common/list_proxies.sh

#Declare variable
work_dir=`pwd`
u_a=0
incr_useragent() {
	a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
    let "u_a=a % max_useragent"
	#findAliveIP
    #id_proxies=$? 
}
exit_process () {
	status=$1
	if [ ${status} -ne 0 ];then
		echo -e $usage
		echo -e $error
	fi
	rm ${work_dir}/*.$$ ${folder}/*.$$ > /dev/null 2>&1 
	exit ${status}
}

trap 'exit_process 1' SIGKILL SIGTERM SIGQUIT SIGINT

echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tDEBUT"

#################################
# PARSE OPTION                  #
#################################
#list options 
usage="download_site.sh\n\
\t-d [YYYYmmdd] date of download (default today)\n\
\t-D [YYYYmmdd] daily download ( previous day is yesterday )\n\
\t-h help\n\
\t-r download Ads from extract.tab only ( don't re-download list pages )\n\
\t-x debug mode\n\
\t-y test mode ( download 2 single category and 2 pages of list pages for testing )\n\
\t-i import SQL to database\n\
\t-z site name\n\
"

## Option parse
lynx_ind=1
mode_test=0
mode_daily=0
mode_import=0
get_all_ind=1
TAB="	"

while getopts :-d:Dhrxyiz name
do
  case $name in
    d) 	d=$OPTARG
		let "shift=shift+1"
		;;
	D) 	last_date=$(date -d "yesterday 13:00" '+%Y%m%d')
		mode_daily=1
        let "shift=shift+1"
        ;;
    h)  echo -e ${usage}
		exit_process 0
		;;
    r)  get_all_ind=0
		let "shift=shift+1"
		;;
    x)  set -x
		mode_daily=0
		let "shift=shift+1"
		;;
    y) 	mode_test=1
		let "shift=shift+1"
		;;
	i) mode_import=1
        let "shift=shift+1"
        ;;
    z)  let "shift=shift+1"
		;;
    	--) break 
		;;
  esac
done
shift ${shift} 

echo "Mode daily"
echo $mode_daily

echo "Mode test"
echo $mode_test 

# If the input day is empty : mean is download daily
if [ "${d}X" = "X" ]
then
	d=`date +"%Y%m%d"`
	# Define the folder name for downloading daily
	folder_name=$d
else
	folder_name=$d
fi
. ../common/db_config.sh "${d}"

#################################
# FUNCTION  DOWNLOAD
#-Description: Download an url and save to html file   
#-Parameters:					
# $1: url			
# $2: html_file
#################################
function download(){
	local url=$1
	local html_file=$2
	local element=$3

	local max_loop=3
	local loop=0

	while [ $loop -lt $max_loop ]; do
		incr_useragent
		proxy="${PROXY_ARR[$id_proxies]}"
		curl -sSL -q "$url" -b $cookie_file -c $cookie_file -A "${USERAGENT_ARR[$u_a]}" -H 'Referer: '$url -H 'Accept-Encoding: gzip, deflate, br'  -H 'Connection: keep-alive'  --retry 5 --compressed -o $html_file
		exit_code_curl=$?
	
		grep -q -i "${element}" "${html_file}"
		exit_code_grep=$?
		
		if [ $exit_code_curl -eq 0 -a $exit_code_grep -eq 0 ]; then
			echo "Download: ${url}  -> OK"
			let "loop=max_loop"
		else
			rm -f  "${html_file}"
			let "loop=loop + 1"
			echo "Download error, try to download again. Loop:$loop"
			sleep 1
		fi
	done
}

#################################
# FUNCTION DOWNLOAD LIST MODE
#-Description: Crawling multi pages from list mode url with multiprocess  
#-Parameters:					
# $1: number of max process		
#################################
function get_url() {
	local ward=1
	local nb_ads=0
	local cat_url=$1
	local page=$2
	local url=""
	
	url=$(awk '/"Url":/{
			split($0, arr, "\"Url\":\"")
			split(arr[2], arr, "\"")
			print arr[1]
	}' "${cat_url}")
	echo "Processing : ${url}"
	if [ ${#url} -eq 0 ]; then
		return 2
	fi

	if [ ! -s "${page}" ]; then
		download "https://homedy.com/${url}" "${page}"
	fi	
	if ! grep -q -i "class=\"relate-new\"" "${page}"; then
		return 2
	fi
	nb_ads=$(awk -f ${awk_dir}/nb_ads.awk "${page}")
	echo -e "Total ads: https://homedy.com/${url} \t ${nb_ads}"
	echo ${page} | grep -i -q "ward"
	ward=$?
	if [ ${#nb_ads} -eq 0 ]; then
		return 2
	fi
	# Limits 3600 ads in website
	if [  ${nb_ads} -lt 3600 -a ${nb_ads} -gt 0 -o  $ward -eq 0 ]; then
		echo -e "${url}\t${nb_ads}" >> "${folder}/list_url_download.tab"
		return 0
	else
		return 1
	fi
	
}
function create_list_category(){
	# list city url:  https://homedy.com/Common/CityAC
	# list district by city: https://homedy.com/Common/DistrictAC?CityId=2
	# list ward by district: https://homedy.com/Common/WardAC?DistrictId=72
	# list street by district: https://homedy.com/Common/StreetAC?districtId=62
	# list list_category_cho_thue url:  https://homedy.com/Common/CategoryAC?typeId=2
	# list list_category_mua_ban url:  https://homedy.com/Common/CategoryAC?typeId=1

	# Get Url: https://homedy.com/Search/GetUrl?SellType=1&CategoryId=62&CityId=2&DistrictId=72&WardId=11852
	# > "ban-nha-rieng-xa-da-phuoc-huyen-binh-chanh-tp-ho-chi-minh"
	# https://homedy.com/Search/GetUrl?SellType=2&CategoryId=62&WardId=11850

	# https://homedy.com/Search/GetUrl?SellType=1&CategoryId=62
	
	# 1st filter: category : if total of ads < 3,600 => OK
	# 2nd filter: category > City : if total of ads < 3,600 => OK
	# 3rd filter (more >3600):  category > City > District
	# 4th filter (more >3600):  category > City > District > Ward
	local sell_type=$1
	local cat_path=$2
	if [ ! -d "${cat_path}" ]; then
		mkdir -p "${cat_path}"
	fi
	
	########## 1st filter ############
	count_1=0
	while read -r line; do
		let "count_1=count_1 + 1"

		if [ $mode_test -eq 1 -a $count_1 -eq 2 ]; then
			break
		fi

		FS='\t' read -r -a array <<< "$line"
		local cat_id="${array[0]}"
		local cat_url="${cat_path}/url-${cat_id}.html"
		local cat_page="${cat_path}/${cat_id}_page-1.html"
		local check_nb_ads=0
		if [ ${#cat_id} -eq 0 ]; then
			continue
		fi
		if [ ! -s "${cat_url}" ]; then
			download "https://homedy.com/Search/GetUrl?SellType=${sell_type}&CategoryId=${cat_id}" "${cat_url}"
		fi
		get_url "${cat_url}" "${cat_page}"
		check_nb_ads=$?
		count_2=0
		province=63
		if [ $mode_test -eq 1 ]; then
			let "province=3"
		fi
		if [ ${check_nb_ads} -eq 1 ]; then
			for i in {1..63}
			do
				let "count_2=count_2 + 1"

				if [ $mode_test -eq 1 -a $count_2 -eq 2 ]; then
					break
				fi
				# 2nd filter : Category > City
				local city_cat_page="${cat_path}/${cat_id}_city_${i}_page-1.html"
				local city_cat_url="${cat_path}/url-${cat_id}_city_${i}.html"
				local stop_download=0
				local last_dist=""
				if [ ! -s "${city_cat_url}" ]; then
					download "https://homedy.com/Search/GetUrl?SellType=${sell_type}&CategoryId=${cat_id}&CityId=${i}" "${city_cat_url}"
				fi
				get_url "${city_cat_url}" "${city_cat_page}"
				check_nb_ads=$?
				count_3=0
				if [ ${check_nb_ads} -eq 1 ]; then
					# 3rd filter : Category > City > District
					while read -r line; do
						let "count_3=count_3 + 1"

						if [ $mode_test -eq 1 -a $count_3 -eq 2 ]; then
							break
						fi
						FS='\t' read -r -a array <<< "$line"
						city_id="${array[0]}"
						district_id="${array[1]}"
						ward_id="${array[2]}"
						if [ ${#district_id} -eq 0 -o ${#city_id} -eq 0 ]; then
							continue
						fi
						if [[ "$last_dist" != "$district_id" ]]; then
							echo "Check the last district: $last_dist"
							stop_download=0
						fi

						if [ $stop_download -eq 1  ]; then
							continue
						fi
						echo "List city: ${city_id}  ${district_id}  ${ward_id} "
						local dist_cat_page="${cat_path}/${cat_id}_dist_${district_id}_page-1.html"
						local dist_cat_url="${cat_path}/url-${cat_id}_dist_${district_id}.html"
						if [ ! -s "${dist_cat_url}" ]; then
							download "https://homedy.com/Search/GetUrl?SellType=${sell_type}&CategoryId=${cat_id}&DistrictId=${district_id}" "${dist_cat_url}"
						fi
						get_url "${dist_cat_url}" "${dist_cat_page}"
						check_nb_ads=$?
						if [ $check_nb_ads -eq 0 ]; then
							stop_download=1
							last_dist="${district_id}"
						fi

						if [ ${check_nb_ads} -eq 1 ]; then
							# 4th filter : Category > City > District > Ward
							local ward_cat_page="${cat_path}/${cat_id}_ward_${ward_id}_page-1.html"
							local ward_cat_url="${cat_path}/url-${cat_id}_ward_${ward_id}.html"
							if [ ${#ward_id} -eq 0 ]; then
								continue
							fi
							if [ ! -s "${ward_cat_url}" ]; then
								download "https://homedy.com/Search/GetUrl?SellType=${sell_type}&CategoryId=${cat_id}&WardId=${ward_id}" "${ward_cat_url}"
							fi
							get_url "${ward_cat_url}" "${ward_cat_page}"
						fi

					done < "${list_wards}/list_${i}_dist_ward.tab"
				fi
 				
			done
		fi
	done < "${work_dir}/list_category.tab"
}
function download_list_mode(){
	# Parameter input
    local _process_max=$1
    # Download download_list open first 
	###python3 $get_download_list

    ##############################
    local list_process_pids=()

	while read -r line; do
		FS='\t' read -r -a array <<< "$line"	
		local link="${array[0]}"
		local number="${array[1]}"
		echo -e "Processing: $link \t ${number}"
		if [ ${#link} -eq 0 -o ${#number} -eq 0 ]; then
			continue
		fi
		local ads_page=18
		local page=$((number / ads_page))
		local max_page=$((page + 1))
		if [ ${max_page} -gt 200 ]; then
			max_page=201
		fi
        local current_list_page=1
		echo "Max page : ${max_page}"
        while [ ${current_list_page} -lt ${max_page} ]; do
            let "current_list_page=current_list_page + 1"
			# Url:https://homedy.com/cho-thue-nha-dat-tp-ho-chi-minh/p2
            local url="https://homedy.com/${link}/p${current_list_page}"
			# Local file: cho-thue-nha-dat-tp-ho-chi-minh-p2.html
            local html_file="${list_folder}/${link}-page-${current_list_page}.html"

			# Check max process or not
            while [ ${#list_process_pids[@]} -gt ${_process_max} ]; do
                for i in ${!list_process_pids[@]} ; do # loop key in list_process_pids
                    # The pid is gone
                    if ! ps -p "${list_process_pids[${i}]}" > /dev/null ; then
                        unset "list_process_pids[${i}]" # Remove the pid out of the list_process_pids
                    fi
                done
				if [ ${#list_process_pids[@]} -lt ${_process_max} ]; then
					break
				fi
				sleep 2s
        	done

			# Download file list mode
			if [ ! -s "${html_file}" ]; then
				download "$url" "$html_file" "</html>" &
				# Take the pid and put it in the array
            	list_process_pids+=($!)
			fi 

            if [ $mode_test -eq 1 -a $current_list_page -eq 2 ]; then
				break
            fi
        done
    done < "${folder}/list_url_download.tab"
	# waiting all processes to complete
    wait "${list_process_pids[@]}"
        
	# Empty an array
    unset list_process_pids
	standardized_all_files_in_folder "${list_folder}"
}
function download_list(){
	if [ ! -s "${folder}/list_url_download.tab" ]; then
		create_list_category "1" "${list_folder}/ban"
		create_list_category "2" "${list_folder}/cho-thue"
		remove_duplicated_lines "${folder}/list_url_download.tab"
	fi
	download_list_mode $process_max
}
###################################
# FUNCTION DOWNLOAD DETAIL MODE
#-Description: Crawling ads page from detail mode url with multiprocess
#-Parameters:
# $1: list download
# $2: number of max process
###################################
function download_detail_mode(){
    # Parameter input
    local list_download=$1
    local _process_max=$2
    local list_process_pids=()

	while read -r line; do
        FS='\t' read -r -a array <<< "$line"
        local id="${array[0]}"
		local url="${array[1]}"
		local file_name="${all_folder}/ads_${id}.html"

		if [ ${#id} -eq 0 -o ${#url} -eq 0 ]; then
			continue
		fi

		if [ -s ${file_name} ]; then
			continue
		fi
		
		# Check max process or not
		while [ ${#list_process_pids[@]} -gt ${_process_max} ]; do
			for i in ${!list_process_pids[@]} ; do # loop key in list_process_pids
			
				# Check the pid done or not
				# if ! kill -0 "${list_process_pids[${i}]}" ; then 

				# The pid is gone
				if ! ps -p "${list_process_pids[${i}]}" > /dev/null ; then
					unset "list_process_pids[${i}]" # Remove the pid out of the list_process_pids
				fi
			done
			if [ ${#list_process_pids[@]} -lt ${_process_max} ]; then
				break
			fi
			sleep 2s
		done

		if [ ! -s "${file_name}" ]; then
            # Take the pid and put it in the array
			download "${url}" "${file_name}" "</html>" &
            list_process_pids+=($!)
        fi
        
    done < "${list_download}"
    # waiting all processes to complete
    wait "${list_process_pids[@]}"
    # Empty an array
    unset list_process_pids
	standardized_all_files_in_folder "${all_folder}"
}

#################################
# DEFINE FOLDER TO SAVE         #
#################################
today=`date +"%Y-%m-%d"`
#Define some folders
folder="${work_dir}/${folder_name}"
all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
list_folder="${folder}/LIST_MODE"

list_wards="${work_dir}/list_wards"
json_dir="${work_dir}/json"
python_dir="${work_dir}/python"
awk_dir="${work_dir}/awk"
bash_dir="${work_dir}/bash"

insert_file="${delta_folder}/ads_insert.sql"
update_file="${delta_folder}/ads_update.sql"
tab_file="${folder}/DELTA/extract.tab"
cookie_file="${folder}/cookie.txt"
get_download_list="${python_dir}/get_download_list.py"

#################################
# DEFINE MAX PROCESS TO RUN     #
#################################
process_max=15
site_name="VN_HOMEDY"
#################################
# MAIN                          #
#################################
main(){
	# Create above folders
	echo "Starting to create the folders."
	mkdir -p $folder $all_folder $delta_folder $list_folder
	if [ ${lynx_ind} -eq 1 ] && [ ${get_all_ind} -eq 1 ]; then
		echo "Starting to download list."
		download_list

		# Create tab file from html file in LIST_MODE
		find "${list_folder}" -type f -name "*page*.html" -exec awk -f ${awk_dir}/put_html_to_tab.awk -vDATE="${today}" -f ${awk_dir}/decode_hex.awk -f ../common/Utils.awk {} \; > "${tab_file}"
		# Sort and remove duplicate line tab_file ###
		if [ -s "$tab_file" ]; then
			echo "Sorting and removing duplicate line $tab_file"
			cp  "$tab_file"  "$tab_file.bk"
			remove_duplicated_lines "${tab_file}"
		fi
	fi
	# Run if the daily mode is enable
    if [ ${mode_daily} -eq 1 ]; then
	    echo "Check last extract.tab"
        last_folders=$(find "${BACKUP_DIR}/${site_name}"/*/DELTA -type f ! -size 0 -name 'extract.tab' | awk '/\/[1-9][0-9]{3}[01][0-9][0-3][0-9]\//{split($0, ar, "'"${BACKUP_DIR}/${site_name}"'/"); split(ar[2], ar, "/"); print ar[1]}')
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
                last_folder="${BACKUP_DIR}/${site_name}/${last_folder}"
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
        download_detail_mode ${tab_file} ${process_max}   
    fi

	# Parsing data
	${bash_dir}/parsing_insert.sh "${folder_name}" 
	${bash_dir}/parsing_update.sh "${folder_name}" 

    # Run if the daily mode is enable.
    if [ ${mode_daily} -eq 1 ]; then
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

	# Import database
	if [ "${mode_import}" -eq 1 ];then 
       ${work_dir}/import_db.sh "${folder_name}"
    fi
	echo "Finished!"
	echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tEND"
	echo "ok" > "${delta_folder}/status_ok"
}
main
