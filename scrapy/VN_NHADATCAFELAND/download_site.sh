#!/bin/bash
#Include libraries
. ../common/list_useragent.sh
. ../common/list_proxies.sh
. ../common/Utils.sh

#Declare variable
work_dir=`pwd`
u_a=0
incr_useragent() {
	a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
	let "u_a=a % max_useragent"
	#findAliveIP
    id_proxies=1
    echo "${PROXY_ARR[$id_proxies]}" 

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
# $3: ip_address
#################################
function download(){
	local url=$1
	local html_file=$2

	local max_loop=5
	local loop=1

	while [ $loop -lt $max_loop ]; do
		incr_useragent
		curl -sSL -x "${PROXY_ARR[$id_proxies]}"  -q "$url" -b $cookie_file -c $cookie_file -A "${USERAGENT_ARR[$u_a]}" -H 'Referer: '$url -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,vi;q=0.8' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' --retry 5 --retry-max-time 90 --max-time 120 --compressed -o $html_file
		exit_code_curl=$?
		grep -q -i "</html>" $html_file
		exit_code_grep=$?
		
		if [ $exit_code_curl -eq 0 -a $exit_code_grep -eq 0 ]; then
			echo "Download: ${url}  -> OK"
			let "loop=max_loop"
		else
			let "loop=loop + 1"
			echo "Download error, try to download again. Loop:$loop"
			sleep 2s
		fi
	done
}

#################################
# DEFINE FOLDER TO SAVE         #
#################################
today=`date +"%Y-%m-%d"`
#Define some folders
folder=${work_dir}/${folder_name}

all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
list_folder="${folder}/LIST_MODE"
temp_folder="${folder}/TEMP"

awk_dir="${work_dir}/awk"
bash_dir="${work_dir}/bash"

insert_file=${delta_folder}/ads_insert.sql
update_file=${delta_folder}/ads_update.sql
tab_file="${folder}/DELTA/extract.tab"
cookie_file="${folder}/cookie.txt"
download_list="${delta_folder}/download_list.temp"

log_folder="${folder}/LOG"
python_dir="${work_dir}/python"

#################################
# MAIN                          #
#################################
main(){
	################################ if in download mode ########################
	#Create above folders
	echo "Starting to create the folders."
	mkdir -p $folder $all_folder $delta_folder $list_folder $log_folder $temp_folder

	echo $d > $folder/date.txt
	case "$mode_test" in
        0)
            echo "FULL DOWNLOAD"
            echo "0" > $folder_name/option_file.txt
        ;;
        1)
            echo "TESTING DOWNLOAD WITH 2 SITES"
            echo "1" > $folder_name/option_file.txt
        ;;
	esac  

	domain="https://nhadat.cafeland.vn"

	category_url=${domain}
	category[1]="nha-dat-ban"
	category[2]="cho-thue"

	# # #============DOWNLOAD SITE ========================
	if [ ${get_all_ind} -eq 1 ]; then
		#Remove DELTA if exist
		if [ -d "${delta_folder}" ]; then
			rm -rf "${delta_folder}"
			mkdir "${delta_folder}"
		fi

		# Generate download list
		for k in ${!category[@]};do
			local list_page_url=${category_url}/${category[${k}]}
			local list_page_file="${temp_folder}/${category[${k}]}.html"
			local country="${temp_folder}/${category[${k}]}_country_extract.tab"
			local city="${temp_folder}/${category[${k}]}_city_extract.tab"
			local district="${temp_folder}/${category[${k}]}_district_extract.tab"

			if [ ! -s "$list_page_file" ]; then
				download "${list_page_url}" "$list_page_file" 
			fi

			if [ -s $list_page_file ]; then
				standardized_data $list_page_file
				awk -f "${awk_dir}/get_list_city.awk" -f ../common/Utils.awk "${list_page_file}" >> $country
			fi

			count_country=0
			while read -r line; do
				let "count_country=count_country + 1"
				if [ $mode_test -eq 1 -a $count_country -eq 2 ]; then
					break
				fi
				FS='\t' read -r -a array <<< "$line"
				number="${array[0]}"
				link="${array[1]}"
				location="${array[2]}"
				type="${array[3]}"
				file_temp=${temp_folder}/${type}-${location}.html

				if [ ! -s "$file_temp" ]; then
					download "${link}" "$file_temp" 
				fi

				if [ -s $file_temp ]; then
					standardized_data $file_temp
					awk -f "${awk_dir}/get_list_city.awk" -f ../common/Utils.awk "${file_temp}" >> $city
				fi
			done < $country

			count_city=0
			while read -r line; do
				let "count_city=count_city + 1"
				if [ $mode_test -eq 1 -a $count_city -eq 2 ]; then
					break
				fi
				FS='\t' read -r -a array <<< "$line"
				number="${array[0]}"
				link="${array[1]}"
				location="${array[2]}"
				type="${array[3]}"
				file_temp=${temp_folder}/${type}-${location}.html

				if [ ! -s "$file_temp" ]; then
					download "${link}" "$file_temp" 
				fi

				if [ -s $file_temp ]; then
					standardized_data $file_temp
					awk -f "${awk_dir}/get_list_ward.awk" -f ../common/Utils.awk "${file_temp}" >> $district
				fi
			done < $city

			count_district=0
			while read -r line; do
				let "count_district=count_district + 1"
				if [ $mode_test -eq 1 -a $count_district -eq 2 ]; then
					break
				fi
				FS='\t' read -r -a array <<< "$line"
				number="${array[0]}"
				link="${array[1]}"
				location="${array[2]}"
				type="${array[3]}"
				echo "$link	$number $location $type" >> $download_list
			done < $district
		done

		if [ -f "$folder_name/max_page_number.txt" ]; then
		    rm "$folder_name/max_page_number.txt"
		fi

		while read -r line; do
			FS='\t' read -r -a array <<< "$line"
			
			link="${array[0]}"
			number="${array[1]}"
			location="${array[2]}"
			type="${array[3]}"
			
			if [ $mode_test -eq 1 ]; then
				echo "2" $link >> $folder_name/max_page_number.txt
			else
				ads_page=26
				page=$((number / ads_page))
				max_page=$((page + 1))
				echo $max_page $link >> $folder_name/max_page_number.txt
			fi
		done < $download_list
		
		echo "Starting to download list."
		cd python/download
		scrapy crawl download_site -a argument=$d --logfile ${log_folder}/scrapy_site.log
		cd .. && cd ..
		standardized_all_files_in_folder "${list_folder}"

		# Create tab file from html file in LIST_MODE
		for file_name in ${list_folder}/*.html; do
			cat $file_name | awk -f ${awk_dir}/put_html_to_tab.awk -f ../common/Utils.awk >> ${tab_file}
		done

		### Sort and remove duplicate line tab_file ###
		if [ -s "$tab_file" ]; then
			echo "Sorting and removing duplicate line $tab_file"
			sort -u "${tab_file}" -o "${tab_file}"
    		remove_duplicated_lines "${tab_file}"
		fi
	fi

	# Backup extract.tab to extract_backup.tab
	echo "Back up extract.tab"
	backup_tab_file="${folder}/DELTA/extract_backup.tab"
	cp $tab_file $backup_tab_file

	######################## Download detail mode #######################
	if [ -s $tab_file ]; then
		list_need_to_download=${delta_folder}/list_id.txt
		# /home/itdev/backup_autobiz_data/DAILY/VN_NHADATCAFELAND/	
		last_folders=$(find "${BACKUP_DIR}/VN_NHADATCAFELAND"/*/DELTA -type f ! -size 0 -name 'extract_backup.tab' | awk '/\/[1-9][0-9]{3}[01][0-9][0-3][0-9]\//{split($0, ar, "'"${BACKUP_DIR}/VN_NHADATCAFELAND"'/"); split(ar[2], ar, "/"); print ar[1]}')
        last_folder=""
        for fn in ${last_folders}; do	
            if [ "${fn}" != "${d}" ]; then
                last_folder="${fn}"
            else
                 break
            fi
        done
		
		# Daily Download
		if [ $mode_daily -eq 1 -a -n "${last_folder}" ]; then
			echo "Daily download is starting"
			## Define dir of extract tab
			tab_last="${BACKUP_DIR}/VN_NHADATCAFELAND/${last_folder}/DELTA/extract_backup.tab"
			update_tab_file="${folder}/DELTA/extract_update.tab"

			# Pre sort
			sort -u -k1,1 -t"${TAB}" "${tab_last}" -o "${tab_last}"
			sort -u -k1,1 -t"${TAB}" "${tab_file}" -o "${tab_file}"
			# Do comparing the tab_file
			join -t"${TAB}" -v2 "${tab_last}" "${tab_file}" > "${update_tab_file}"; 

			# Generate list need to download
			while read -r line; do
				FS='\t' read -r -a array <<< "$line"
				ads_id="${array[0]}"
				ads_url="${array[1]}"
				ads_type="${array[2]}"
				if [ ${#ads_id} -ne 0 -a ${#ads_type} -ne 0 -a ${#ads_url} -ne 0 ]; then
					echo "$ads_id $ads_url" >> $list_need_to_download
				fi
			done < $update_tab_file

			echo "Download detail mode."
			cd python/download
			scrapy crawl download_ads -a argument=$d --logfile ${log_folder}/scrapy_ads.log
			cd .. && cd ..
			rm -f $list_need_to_download

			# Transfer remove extract.tab and convert extract_update.tab to extract_.tab for further parsing
			echo "Convert to extract_update.tab to extract.tab"
			rm -f $tab_file
			mv $update_tab_file $tab_file
		
		# Fully Download
		else
			echo "Fully download is starting"
			while read -r line; do
				FS='\t' read -r -a array <<< "$line"
				ads_id="${array[0]}"
				ads_url="${array[1]}"
				ads_type="${array[2]}"
				if [ ${#ads_id} -ne 0 -a ${#ads_type} -ne 0 -a ${#ads_url} -ne 0 ]; then
					echo "$ads_id $ads_url" >> $list_need_to_download
				fi
			done < $tab_file
			
			echo "Download detail mode."
			cd python/download
			scrapy crawl download_ads -a argument=$d --logfile ${log_folder}/scrapy_ads.log
			cd .. && cd ..
			rm -f $list_need_to_download
		fi
	fi

	# Parsing data
	${bash_dir}/parsing_insert.sh "$d" 
	${bash_dir}/parsing_update.sh "$d" 

	# Import database
	if [ "${mode_import}" -eq 1 ];then 
       ${bash_dir}/import_db.sh "${folder_name}"
    fi

	# Delete TEMP FOLDER
	# if [ -d "${temp_folder}" ]; then
    #     rm -rf "${temp_folder}"
    # fi

	echo "Finished!"
	echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tEND"

	echo "ok" > "${delta_folder}/status_ok"
}
main