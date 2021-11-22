#!/bin/bash
#Include libraries
. ../common/list_useragent.sh
. ../common/Utils.sh


#Declare variable
work_dir=`pwd`
u_a=0
incr_useragent() {
	a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
        let "u_a=a % max_useragent"
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
# FUNCTION  CHECK MAX PROCESS   
#-Parameters:					
# $1: number of max process				
#################################
function check_max_process(){
    # Parameter input
    local _process_max=$1

    while [ "${#list_process_pids[@]}" -gt "${_process_max}" ]; do
        for i in ${!list_process_pids[@]} ; do # loop key in list_process_pids
        
            # The pid is gone
            if ! ps -p "${list_process_pids[${i}]}" > /dev/null ; then
                unset "list_process_pids[${i}]" # Remove the pid out of the list_process_pids
            fi
        done
        if [ "${#list_process_pids[@]}" -lt "${_process_max}" ]; then
            break
        fi
        sleep 1
    done
}

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
	local ip_address=$3

	local max_loop=5
	local loop=1

	while [ $loop -lt $max_loop ]; do
		incr_useragent
		curl -sSL -x $ip_address -q "$url" -b $cookie_file -c $cookie_file -A "${USERAGENT_ARR[$u_a]}" -H 'Referer: '$url -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.9,vi;q=0.8' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'Connection: keep-alive' -H 'Cache-Control: max-age=0' -H 'Upgrade-Insecure-Requests: 1' --retry 5 --retry-max-time 90 --max-time 120 --compressed -o $html_file
		exit_code_curl=$?
		grep -q -i "</html>" $html_file
		exit_code_grep=$?
		
		if [ $exit_code_curl -eq 0 -a $exit_code_grep -eq 0 ]; then
			echo "Download: ${url}  -> OK"
			let "loop=max_loop"
		else
			let "loop=loop + 1"
			echo "Download error, try to download again. Loop:$loop"
			rm -f $html_file
			sleep 2s
		fi
		rm -f $cookie_file
	done
}

#################################
# FUNCTION DOWNLOAD LIST MODE
#-Description: Crawling multi pages from list mode url with multiprocess  
#-Parameters:					
# $1: number of max process		
#################################
function download_list_mode(){
	# Parameter input
    local _process_max=$1
    # Declare some local variables
    local page_param="p"
    
	domain="https://propzy.vn"
	
	category_url=${domain}
	category[1]="mua/nha/hcm"
	category[2]="mua/can-ho/hcm"
	category[3]="mua/dat-nen/hcm"
	category[4]="mua/dat-nen-du-an/hcm"
	category[5]="thue/nha/hcm"
	category[6]="thue/can-ho/hcm"

	name_category[1]="mua-nha-hcm"
	name_category[2]="mua-can-ho-hcm"
	name_category[3]="mua-dat-nen-hcm"
	name_category[4]="mua-dat-nen-du-an-hcm"
	name_category[5]="thue-nha-hcm"
	name_category[6]="thue-can-ho-hcm"

    ##############################

	# If list_process_pids is local check Maxprocess will error b/c function cant change value of this array
    list_process_pids=()

   	# Start download list mode
	for k in ${!category[@]};do
        local stop_download[$k]=0
        local current_list_page=0

		# Take max page
		local max_page=0
		local max_page_url=${category_url}/${category[${k}]}
		# Local max_page_file: mua-nha-hcm.html
		local max_page_file=${list_folder}/${name_category[${k}]}.html

		download ${max_page_url} $max_page_file "172.16.1.11:3128"

		if [ -s $max_page_file ]; then
			standardized_data $max_page_file
			max_page=$(awk -f "${awk_dir}/get_max_page.awk" -f ../common/Utils.awk "${max_page_file}")
			rm -f $max_page_file
		fi

        while [ ${stop_download[$k]} -ne 1 ]; do
            let "current_list_page=current_list_page + 1"
			# Url: https://propzy.vn/mua/nha/hcm/p2
            local url=${category_url}/${category[${k}]}/${page_param}${current_list_page}
            # Local file: mua-nha-hcm-1.html
            local html_file=${list_folder}/${name_category[${k}]}-${page_param}${current_list_page}.html

			# Check max process or not
            check_max_process ${_process_max}

			# Download file list mode
			if [ ! -s "${html_file}" ]; then
				download "$url" "$html_file" "172.16.1.11:3128" &
				# Take the pid and put it in the array
				list_process_pids+=($!)
			fi

			# Conditional for stoping
			if [ ${current_list_page} -ge "${max_page}" ]; then
				stop_download[$k]=1
			fi

            if [ $mode_test -eq 1 -a $current_list_page -eq 1 ]; then
                stop_download[$k]=1
            fi
        done
		# waiting all processes to complete
        wait "${list_process_pids[@]}"
        
    done
	# Empty an array
    unset list_process_pids
	standardized_all_files_in_folder "${list_folder}"
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

    # If list_process_pids is local check Maxprocess will error b/c function cant change value of this array
    list_process_pids=()

	while read -r line; do
        FS='\t' read -r -a array <<< "$line"
        url="${array[0]}"
		file="${array[1]}"

		# Check max process or not
		check_max_process ${_process_max}

		if [ ! -s "${file}" ]; then
            # Take the pid and put it in the array
			download "${url}" "${file}" "172.16.1.11:3128" &
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
folder=${work_dir}/${folder_name}

all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
list_folder="${folder}/LIST_MODE"

awk_dir="${work_dir}/awk"
bash_dir="${work_dir}/bash"

insert_file="${delta_folder}/ads_insert.sql"
update_file="${delta_folder}/ads_update.sql"
tab_file="${folder}/DELTA/extract.tab"
cookie_file="${folder}/cookie.txt"

#################################
# DEFINE MAX PROCESS TO RUN     #
#################################
process_max=15
list_process_pids=()


#################################
# MAIN                          #
#################################
main(){
	#Create above folders
	echo "Starting to create the folders."
	mkdir -p $folder $all_folder $delta_folder $list_folder
	
	# Download list mode
	if [ ${get_all_ind} -eq 1 ]; then
		#Remove DELTA if exist
		if [ -d "${delta_folder}" ]; then
			rm -rf "${delta_folder}"
			mkdir "${delta_folder}"
		fi

		echo "Starting to download list."
		download_list_mode ${process_max}

		# Create tab file from html file in LIST_MODE
		for file_name in ${list_folder}/*.html; do
			cat $file_name | awk -v domain=$domain -f ${awk_dir}/put_html_to_tab.awk -f ../common/Utils.awk >> ${tab_file}
		done

		if [ -s "$tab_file" ]; then
			### Sort and remove duplicate line tab_file ###
			echo "Sorting and removing duplicate line $tab_file"
			sort -u "${tab_file}" -o "${tab_file}"
    		remove_duplicated_lines "${tab_file}"
		fi
	fi

	# Download detail mode
	if [ -s $tab_file ]; then
		list_need_to_download=${delta_folder}/list_need_to_download.temp

		last_folders=$(find "${work_dir}"/*/DELTA -type f ! -size 0 -name 'extract.tab' | awk '/\/[1-9][0-9]{3}[01][0-9][0-3][0-9]\//{split($0, ar, "'"${work_dir}"'/"); split(ar[2], ar, "/"); print ar[1]}')
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
			tab_last="${work_dir}/${last_folder}/DELTA/extract.tab"
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
					file_ads=${all_folder}/${ads_type}-${ads_id}.html
					echo "$ads_url	$file_ads $ads_id" >> $list_need_to_download
				fi
			done < $update_tab_file

			echo "Download detail mode."
			download_detail_mode $list_need_to_download ${process_max}
			rm -f $list_need_to_download

			# Transfer extract_update.tab to extract.tab and extract.tab to extract_backup.tab
			echo "Back up extract.tab"
			backup_tab_file="${folder}/DELTA/extract_backup.tab"
			cp $tab_file $backup_tab_file
			mv $update_tab_file $tab_file

		# Fully Download
		else
			echo "Fully download is starting"
			while read -r line; do
				FS='\t' read -r -a array <<< "$line"
				ads_id="${array[0]}"
				ads_type="${array[2]}"
				ads_url="${array[1]}"
				if [ ${#ads_id} -ne 0 -a ${#ads_type} -ne 0 -a ${#ads_url} -ne 0 ]; then
					file_ads=${all_folder}/${ads_type}-${ads_id}.html
					echo "$ads_url	$file_ads $ads_id" >> $list_need_to_download
				fi
			done < $tab_file

			echo "Download detail mode."
			download_detail_mode $list_need_to_download ${process_max}
			rm -f $list_need_to_download
		fi
	fi

	# Parsing data
	${bash_dir}/parsing_insert.sh "$d" 
	${bash_dir}/parsing_update.sh "$d" 

	# Run if daily mode is enabled
	if [ $mode_daily -eq 1 -a -n "${last_folder}" ]; then
		echo "Convert extract.tab again"
		mv $tab_file $update_tab_file
		mv $backup_tab_file $tab_file
	fi

	# Import data
	if [ "${mode_import}" -eq 1 ];then 
		${bash_dir}/import_db.sh "${folder_name}"	
    fi

	echo "Finished!"
	echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tEND"

	echo "ok" > "${delta_folder}/status_ok"
}
main