#!/bin/bash
#Include libraries
. ../common/list_useragent.sh
. ../common/Utils.sh


#Declare variable
work_dir=`pwd`
u_a=0
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
#################################
function download(){
	local url=$1
	local html_file=$2

	local max_loop=5
	local loop=1

	while [ $loop -lt $max_loop ]; do
		incr_useragent
		curl -sSL -q "$url" -b $cookie_file -c $cookie_file -A "${USERAGENT_ARR[$u_a]}" -H 'Referer: '$url -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,vi;q=0.8' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' --retry 5 --retry-max-time 90 --max-time 120 --compressed -o $html_file
		exit_code_curl=$?
		grep -q -i "</html>" $html_file
		exit_code_grep=$?
		
		if [ $exit_code_curl -eq 0 -a $exit_code_grep -eq 0 ]; then
			echo "Download: ${url}  -> OK"
			let "loop=max_loop"
		else
			let "loop=loop + 1"
			echo "Download error, try to download again. Loop:$loop"
			#sleep 2s
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
tel_folder="${all_folder}/TEL"

awk_dir="${work_dir}/awk"
bash_dir="${work_dir}/bash"

insert_file="${delta_folder}/ads_insert.sql"
update_file="${delta_folder}/ads_update.sql"
update_file_tel="${delta_folder}/tel_ads_update.sql"
tab_file="${folder}/DELTA/extract.tab"
tel_tab_file="${folder}/DELTA/tel_extract.tab"
cookie_file="${folder}/cookie.txt"
max_page_number="${folder}/max_page_number.txt"


log_folder="${folder}/LOG"
python_dir="${work_dir}/python"
sale_folder="${list_folder}/FOR_SALE"
lease_folder="${list_folder}/FOR_LEASE"


#################################
# MAIN                          #
#################################
main(){
	#Create above folders
	echo "Starting to create the folders."
	mkdir -p $folder $all_folder $delta_folder $list_folder $tel_folder $sale_folder $lease_folder $log_folder

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

	domain="https://alonhadat.com.vn"
	category_url=${domain}/"nha-dat"

	category[1]="can-ban"
	category[2]="cho-thue"

	for k in ${!category[@]};do
		if [ $mode_test -eq 1 ]; then
			echo "2" >> $folder_name/max_page_number.txt
		else 
			# Take max page
			local max_page=0
			local max_page_url=${category_url}/${category[${k}]}/"trang--100000.html"
			local max_page_file=${list_folder}/${category[${k}]}.html

			download ${max_page_url} $max_page_file

			if [ -s $max_page_file ]; then
				standardized_data $max_page_file
				max_page=$(awk -f "${awk_dir}/get_max_page.awk" -f ../common/Utils.awk "${max_page_file}")
				echo $max_page >> $folder_name/max_page_number.txt
			fi

		fi
	done

    # Download list mode
	if [ ${get_all_ind} -eq 1 ]; then
		# Remove DELTA if exist
		if [ -d "${delta_folder}" ]; then
			rm -rf "${delta_folder}"
			mkdir "${delta_folder}"
		fi

		echo "Starting to download list."
		cd python/download
		scrapy crawl download_site -a argument=$d --logfile ${log_folder}/scrapy_site.log
		cd .. && cd ..
		standardized_all_files_in_folder "${sale_folder}"
		standardized_all_files_in_folder "${lease_folder}"

		# Create tab file from html file in LIST_MODE
		for file_name in ${sale_folder}/*.html; do
			cat $file_name | awk -v domain=$domain -f ${awk_dir}/put_html_to_tab.awk -f ../common/Utils.awk >> ${tab_file}
		done

		for file_name in ${lease_folder}/*.html; do
			cat $file_name | awk -v domain=$domain -f ${awk_dir}/put_html_to_tab.awk -f ../common/Utils.awk >> ${tab_file}
		done

		# Sort and remove duplicate line tab file
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

	last_folders=$(find "${work_dir}"/*/DELTA -type f ! -size 0 -name 'extract_backup.tab' | awk '/\/[1-9][0-9]{3}[01][0-9][0-3][0-9]\//{split($0, ar, "'"${work_dir}"'/"); split(ar[2], ar, "/"); print ar[1]}')
	for fn in ${last_folders}; do	
		if [ "${fn}" != "${d}" ]; then
			last_folder="${fn}"
		else
				break
		fi
	done

	# Download detail mode
	if [ -s $tab_file ]; then
		list_need_to_download=${delta_folder}/list_id.txt

		# Daily Download
		if [ $mode_daily -eq 1 -a -n "${last_folder}" ]; then
			echo "Daily download is starting"
			## Define dir of extract tab
			tab_last="${work_dir}/${last_folder}/DELTA/extract_backup.tab"
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
				ads_type="${array[2]}"
				ads_url="${array[1]}"
				if [ ${#ads_id} -ne 0 -a ${#ads_type} -ne 0 -a ${#ads_url} -ne 0 ]; then
					echo "$ads_id $ads_url" >> $list_need_to_download
				fi
			done < $update_tab_file

			echo "Download detail mode."
			cd python/download
			scrapy crawl download_ads -a argument=$d --logfile ${log_folder}/scrapy_ads.log
			cd .. && cd ..
			standardized_all_files_in_folder "${all_folder}"
			#rm -f $list_need_to_download

		# Fully Download
		else
			echo "Fully download is starting"
			while read -r line; do
				FS='\t' read -r -a array <<< "$line"
				ads_id="${array[0]}"
				ads_type="${array[2]}"
				ads_url="${array[1]}"
				if [ ${#ads_id} -ne 0 -a ${#ads_type} -ne 0 -a ${#ads_url} -ne 0 ]; then
					echo "$ads_id $ads_url" >> $list_need_to_download
				fi
			done < $tab_file

			echo "Download detail mode."
			cd python/download
			scrapy crawl download_ads -a argument=$d --logfile ${log_folder}/scrapy_ads.log
			cd .. && cd ..
			standardized_all_files_in_folder "${all_folder}"
			#rm -f $list_need_to_download
		fi
	fi

	# Create tel tab file from html file in ALL folder
	for file_name in ${all_folder}/*.html; do
		ads_id=$(echo "$file_name" | awk '{gsub(".html","",$0); split($0,ar,"ALL/"); split(ar[2],arr,"-"); print arr[length(arr)]}')
		cat $file_name | awk -v id=$ads_id -f ${awk_dir}/put_detail_to_tab_tel.awk -f ../common/Utils.awk >> ${tel_tab_file}
	done

	# Download telephone
	if [ -s $tel_tab_file ]; then
		tel_list_need_to_download=${delta_folder}/list_id_tel.txt
		
		# Daily Download
		if [ $mode_daily -eq 1 -a -n "${last_folder}" ]; then
			echo "Daily telephone download is starting"
			repeated_id_extract_tab_file="${folder}/DELTA/repeated_id_extract.tab"

			#tel_tab_last="${work_dir}/${last_folder}/DELTA/tel_extract.tab"
			update_tel_tab_file="${folder}/DELTA/tel_extract_update.tab"

			sort -u -k1,1 -t"${TAB}" "${tab_last}" -o "${tab_last}"
			sort -u -k1,1 -t"${TAB}" "${tab_file}" -o "${tab_file}"

			join -t "$(printf '\t')" --nocheck-order -j1 "${tab_last}" "${tab_file}" -o 1.1 > "${repeated_id_extract_tab_file}";

			sort -u -k1,1 -t"${TAB}" "${repeated_id_extract_tab_file}" -o "${repeated_id_extract_tab_file}"
			sort -u -k1,1 -t"${TAB}" "${tel_tab_file}" -o "${tel_tab_file}"

			join -t"${TAB}" "${tel_tab_file}" "${repeated_id_extract_tab_file}" -v1 > "${update_tel_tab_file}"; 

			while read -r line; do
				FS='\t' read -r -a array <<< "$line"
				ads_id="${array[0]}"
				ads_url="${array[1]}"
				if [ ${#ads_id} -ne 0 -a ${#ads_url} -ne 0 ]; then
					echo "$ads_id $ads_url" >> ${tel_list_need_to_download}
				fi
			done < ${update_tel_tab_file}

			cd python/download
			scrapy crawl download_tel -a argument=$d --logfile ${log_folder}/scrapy_tel.log
			cd .. && cd ..
			standardized_all_files_in_folder "${tel_folder}"
			rm -f $repeated_id_extract_tab_file
			#rm -f $tel_list_need_to_download

			# Transfer remove extract.tab and convert extract_update.tab to extract_.tab for further parsing
			echo "Convert to extract_update.tab to extract.tab"
			rm -f $tab_file
			mv $update_tab_file $tab_file

		# Fully Download
		else
			echo "Fully telephone download is starting"
			while read -r line; do
				FS='\t' read -r -a array <<< "$line"
				ads_id="${array[0]}"
				ads_url="${array[1]}"
				if [ ${#ads_id} -ne 0 -a ${#ads_url} -ne 0 ]; then
					echo "$ads_id $ads_url" >> ${tel_list_need_to_download}
				fi
			done < ${tel_tab_file}

			cd python/download
			scrapy crawl download_tel -a argument=$d --logfile ${log_folder}/scrapy_tel.log
			cd .. && cd ..
			standardized_all_files_in_folder "${tel_folder}"
			#rm -f $tel_list_need_to_download
		fi

	fi
	
	# Parsing data
	${bash_dir}/parsing_insert.sh "$d" 
	${bash_dir}/parsing_update.sh "$d" 
	${bash_dir}/parsing_update_tel.sh "$d" 

	# Import data
	if [ "${mode_import}" -eq 1 ];then 
		${bash_dir}/import_db.sh "$d"
    fi

    echo "Finished!"
    echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tEND" 

	echo "ok" > "${delta_folder}/status_ok"
}
main