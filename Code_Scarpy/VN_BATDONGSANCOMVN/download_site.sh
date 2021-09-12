#!/usr/bin/env bash
#
# Perfom crawling and parsing data from tinbatdongsan.com

#Include libraries
source ../Lib_Offy/Utils.sh
source ../Lib_Offy/list_useragent.sh 
u_a=0

work_dir=$(pwd)
lib_dir="../Lib_Offy"

readonly DOMAIN="https://batdongsan.com.vn"
readonly MAX_LOOP=3          # Maximun number of trying re-download html file if failed
readonly SLEEP_SEC=0         # Sleep second between downloading html file
NB_PROCESSES=8              # Number of proocesses when apply multi-processes
TAB="	"
today=$(date +"%Y-%m-%d")

incr_useragent() {
	a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
        let "u_a=a % max_useragent"
		# let "ip=a % max_ip"
}


ExitProcess () {
	status=$1
	if [ ${status} -ne 0 ]
	then
		echo -e $usage
		echo -e $error
	fi
	rm ${work_dir}/*.$$ ${work_dir}/${d}/*.$$ > /dev/null 2>&1 
	exit ${status}
}

trap 'ExitProcess 1' SIGKILL SIGTERM SIGQUIT SIGINT

echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tDEBUT"

#################################
# PARSE OPTION                  #
#################################
#list options 
usage="download_site.sh\n\
\t-d [date] (default today)\n\
\t-p [nb processes] number of running process\n\
\t-x debug mode\n\
\t-a no download\n\
\t-y test mode ( download 2 single category and 2 pages of list pages for testing )\n\
\t-D Daily download ( previous day is yesterday )\n\
\t-i import SQL to database\n\
\t-r retrieve only, do not download the detailed adds\n\
\t-c update cache of download list\n\
\t-z site name\n\
\t-h help\n\
"

## Option parse
mode_download=1
get_all_ind=1
mode_test=0
mode_daily=0
mode_import=0
mode_update_cache=0

while getopts :axyDirhzc:d:p: name; do
  case $name in
    x)  set -x
        let "shift=shift+1"
    ;;

    a)  mode_download=0
        let "shift=shift+1"
    ;;

    y)  mode_test=1
        let "shift=shift+1"
    ;;

    d) 	d=$OPTARG
        let "shift=shift+1"
    ;;

    D) 	last_date=$(date -d "yesterday 13:00" '+%Y%m%d')
        mode_daily=1
        let "shift=shift+1"
    ;;

    i)  mode_import=1
        let "shift=shift+1"
    ;;

    r)  get_all_ind=0
		let "shift=shift+1"
		;;

    z) let "shift=shift+1"
    ;;

    c) mode_update_cache=1
        let "shift=shift+1"
    ;;

    p) 	# Check if positive integer and maximum 20 processes
        if [[ "${OPTARG}" =~ ^[0-9]+$ ]] && [[ "${OPTARG}" -gt 0 ]]; then
            if [[ "${OPTARG}" -lt 20 ]]; then
                NB_PROCESSES="${OPTARG}"
            else
                NB_PROCESSES=20
            fi
        fi
        let "shift=shift+1"
    ;;

    h)  echo -e ${usage}
        ExitProcess 0
	;;

    --) break 
	;;

  esac
done
shift ${shift}

# If the input day is not empty
if [[ -z "${d}" ]]; then
    d=$(date +"%Y%m%d")
    folder_name="${d}"
else
    folder_name="${d}"
fi

source ../common/db_config.sh "${d}"
# {{{ GLOBAL VARIABLES
#################################
# DEFINE FOLDER TO SAVE         #
#################################

readonly FOLDER="${work_dir}/${folder_name}"
readonly ALL_FOLDER="${FOLDER}/ALL"
readonly DELTA_FOLDER="${FOLDER}/DELTA"
readonly LIST_FOLDER="${FOLDER}/LIST_MODE"
readonly LOG_FOLDER="${FOLDER}/LOG"

readonly LINK_FILE="${work_dir}/cache/link.tab"
readonly TAB_FILE="${DELTA_FOLDER}/extract.tab"
readonly AWK_FOLDER="${work_dir}/awk"

readonly TABLE_NAME="BATDONGSANCOMVN"
readonly insert_file="${DELTA_FOLDER}/ads_insert.sql"
readonly update_file="${DELTA_FOLDER}/ads_update.sql"
readonly cookie_file="${FOLDER}/cookie.txt"

TOTAL_PAGE=1
# }}} end global variables

#######################################
# Custom curl to specific crawling site
# Globals:
#   None
# Arguments:
#   url link to download
#   location to save html file
#######################################
function download_tool {
    local url=$1
    local save_file=$2
    local proxy="172.16.1.11:3128"

    #node ../Lib_Offy/puppeteer-crawling/main.js url="${url}" proxy="http://172.16.1.11:3128" delay="1" saved_file="${save_file}"
    node ../Lib_Offy/puppeteer-crawling/batdongsancomvn.js url="${url}" proxy="${proxy}" delay="5" saved_file="${save_file}"
}

#######################################
# Hepler function to download web content
# Globals:
#   MAX_LOOP
# Arguments:
#   None
#######################################
function download_page {
    local loop=0
    local url=$1
    local output_file=$2

    while (( ${loop} < ${MAX_LOOP} )); do
        if [[ ! -f "${output_file}" ]] || [[ ! -s "${output_file}" ]]; then 
            incr_useragent
            download_tool "${url}" "${output_file}"

            if grep -i 'vui lòng nhập mã captcha' "${output_file}" 1> /dev/null; then
                rm -rf "${output_file}"
            elif ! grep -i "<\/html>" "${output_file}" 1> /dev/null; then
                rm -rf "${output_file}"
            else
                standardized_data "${output_file}"
                loop=${MAX_LOOP}
            fi

            (( loop = loop + 1 ))
        else
            loop=${MAX_LOOP}
        fi
    done
}

#######################################
# Download content in list mode with
# multiprocess
# Globals:
#   NB_PROCESSES
# Arguments:
#   None
#######################################
function download_each_listmode_multi {
    local base_url=$1
    local nb_pages=$2

    if [[ "${base_url}" == *"nha-dat-cho-thue"* ]]; then
        local name="rent"
    else
        local name="sale"
    fi


    if [[ "${nb_pages}" -lt "${NB_PROCESSES}" ]]; then
        local max_processes="${nb_pages}"
    else
        local max_processes="${NB_PROCESSES}"
    fi

    running_proccsess=()
    for ((i=1; i <= ${max_processes}; i++)) ;do
        running_proccsess+=(-2)
    done

    local page=1
    while [[ ${page} -le ${nb_pages} ]]; do
        local url="${base_url}/p${page}"
        local page_html_file="${LIST_FOLDER}/${name}-page-${TOTAL_PAGE}.html"

        if [[ -f "${page_html_file}" ]] && [[ -s "${page_html_file}" ]]; then
            echo "Skipping page-${TOTAL_PAGE}"

        else
            local is_asssign=0

            # infinite loop to assign the url download to child process
            while [[ "${is_asssign}" -eq 0 ]] ; do
                for i in "${!running_proccsess[@]}"; do

                    if kill -0 "${running_proccsess[$i]}" > /dev/null 2>&1; then
                        continue
                    fi

                    echo "Downloading page-${TOTAL_PAGE}"
                    download_page "${url}" "${page_html_file}" &
                    running_proccsess[$i]=$!
                    is_asssign=1
                    break
                done

                test "${is_asssign}" -eq 1 && break
                sleep 3

            done
        fi
        (( TOTAL_PAGE = TOTAL_PAGE + 1 ))
        (( page = page + 1 ))
    done

    wait "${running_proccsess[@]}"
    unset running_proccsess
}


function download_detail_ad {
    local extract_file=$1
    local max_processes="${NB_PROCESSES}"

    running_proccsess=()
    for ((i=1; i <= ${max_processes}; i++)) ;do
        running_proccsess+=(-2)
    done

    while read -a line; do
        local id_client="${line[0]}"
        local url="${line[1]}"
        local page_html_file="${ALL_FOLDER}/ads_${id_client}.txt"

        if [[ -f "${page_html_file}" ]] && [[ -s "${page_html_file}" ]]; then
            echo "[detail-mode] Skipping ads ${id_client}"
            continue
        elif [[ -z "${id_client}" ]]; then
            continue
        fi

        # infinite loop to assign the url download to child process
        echo "[detail-mode] Downloading ads ${id_client}"
        local is_asssign=0
        while [[ "${is_asssign}" -eq 0 ]]; do
            for i in "${!running_proccsess[@]}"; do

                if kill -0 "${running_proccsess[$i]}" > /dev/null 2>&1; then
                    continue
                fi

                download_page "${url}" "${page_html_file}" &
                running_proccsess[$i]=$!
                is_asssign=1
                break
            done

            # Early break loop instead of waiting 1 second
            test "${is_asssign}" -eq 1 && break
            sleep 3
        done

    done < "${extract_file}"

    wait "${running_proccsess[@]}"
    unset running_proccsess
}

#######################################
# Created need_download.tab
# Note: need_download.tab contains only
# the new ads's url for crawling daily
#
# Globals:
#   TAB_FILE
# Arguments:
#   None
#######################################
function create_need_download_tab {
    # Algorithm:
    #     - Find the extract.tab file of today to get id_client ("today")
    #     - Find the extract.tab file of most recent date to get id_client ("most_recent")
    #     - Get id_client, url that have in "today" but not in "most_recent" (join command -v option)
    #     - Save the result to "nead_download" file
    #     - If fully download mode, "nead_download" is same as "today"

    echo "[detail-mode] Starting create need_download.tab"

    local need_download_file=$1
    local today_extract="${TAB_FILE}"

    local most_recent_date=20200101 # Dummy small value

    # Get list of download date in working FOLDER (pwd)
    local previous_dates=($(find . -type f -name 'extract.tab' | awk 'BEGIN {FS="/"} {print $2}'))

    # Get most recent date
    for p in ${previous_dates[@]}; do
        if [[ "${most_recent_date}" -lt "${p}" ]] && [[ "${p}" -ne "${folder_name}" ]]; then
            most_recent_date=${p}
        fi
    done

    # If there is no recent date data FOLDER, start download full ads list
    # from today extract.tab
    if [[ "${most_recent_date}" -eq 20200101 ]]; then
        cp "${today_extract}" "${need_download_file}"
    else
        local most_recent_tab="${work_dir}/${most_recent_date}/DELTA/extract.tab"

        # Get id_clients that is not exist in most recent date data
        # id_client diff = id_client_today - id_client_most_recent_date
        join -t"${TAB}" -v1 "${today_extract}" "${most_recent_tab}" > "${need_download_file}"
    fi
}

#######################################
# Parsing data to insert to database
#
# Globals:
#   TABLE_NAME
#   AWK_FOLDER
# Arguments:
#   $1 Tab file to parsing
#   $2 Output file
#######################################
function parse_insert_queries {
    local tab_file=$1
    local output_file=$2

    if [[ -f "${tab_file}" ]]; then
        echo "create extract.tab...OK"

        awk -vtable=${TABLE_NAME} -vcreated_date="${today}" \
            -f ${AWK_FOLDER}/list_tab.awk \
            -f ${AWK_FOLDER}/put_tab_into_db.awk \
            "${tab_file}" > "${output_file}"
    fi
}

######################################################################
########################### Main #####################################
######################################################################

function main {
    echo "[mode] download.....${mode_download}"
    echo "[mode] daily.....${mode_daily}"
    echo "[mode] test.....${mode_test}"
    echo "[mode] import.....${mode_import}"
    echo "[mode] number of processes.....${NB_PROCESSES}"


    if [[ ${get_all_ind} -eq 1 ]]; then
        echo "Cleaning folder"
        echo "Creating the folders"
        echo $FOLDER
        echo $ALL_FOLDER
        echo $DELTA_FOLDER
        echo $LIST_FOLDER
        mkdir -p ${ALL_FOLDER} ${DELTA_FOLDER} ${LIST_FOLDER} ${LOG_FOLDER} "${work_dir}/cache"
    fi

    # check FOLDER create successful
    if [[ ! -d "${FOLDER}" ]]; then
        exit_process 1
    fi

    echo "[mode] update cache.....${mode_update_cache}"

    # =====================================================================
    # ==================== Download list mode =============================
    # =====================================================================

    # check retrieve data only (-r option)
    if [[ "${mode_download}" -eq 1 ]] && [[ ${get_all_ind} -eq 1 ]]; then

        # Create url link after filter location criteria
        echo "[get-link] Prepare url for list mode download...."

        categories[0]="nha-dat-ban"
        categories[1]="nha-dat-cho-thue"

        rm -rf "${LINK_FILE}"

        # Find all url of sale type and its number of pages
        for category in "${categories[@]}"; do
            local url="${DOMAIN}/${category}"
            local save_file="${LIST_FOLDER}/${category}.max"

            download_page "${url}" "${save_file}"
            nb_pages=$(awk -f "${lib_dir}/Utils.awk" -f ${AWK_FOLDER}/nb_pages.awk ${save_file})

            echo "${url}${TAB}${nb_pages}" >> "${LINK_FILE}"
        done

        remove_duplicated_lines "${LINK_FILE}"

        echo -e  "Date: $(date +"%Y-%m-%d %H:%M:%S")" > "${work_dir}/cache/status_ok"

        echo "[list-mode] Starting download list page..."

        # Download list mode for each sale type
        if [[ "${mode_test}" -ne 1 ]]; then
            while IFS="${TAB}" read -a arr; do
                local base_url="${arr[0]}"
                local nb_page="${arr[1]}"

                download_each_listmode_multi "${base_url}" "${nb_page}"
                wait
            done < "${LINK_FILE}"

        # Test mode
        else
            local base_url="${DOMAIN}/nha-dat-ban"
            local nb_page=2

            download_each_listmode_multi "${base_url}" "${nb_page}"
            wait
        fi

        rm -rf "${LIST_FOLDER}/*.max"
    fi

    # =====================================================================
    # ==================== Create extract tab =============================
    # =====================================================================

    if [[ "${get_all_ind}" -eq 1 ]]; then
        echo "Starting create extract.tab"
        
        find "${LIST_FOLDER}" -type f -name "*.html" -exec  awk -vcreated_date="${today}" -f ${lib_dir}/Utils.awk  -f ${AWK_FOLDER}/list_tab.awk  -f ${AWK_FOLDER}/put_html_into_tab.awk {} \; > "${TAB_FILE}"
        cp "${TAB_FILE}" "${TAB_FILE}.bk"
        remove_duplicated_lines "${TAB_FILE}"
    fi


    # =====================================================================
    # ==================== Download detail mode ===========================
    # =====================================================================

    local need_download_file="${DELTA_FOLDER}/need_download.tab"
    if [[ ${mode_download} -eq 1 ]] && [[ -f "${TAB_FILE}" ]]; then

        # Daily download
        if [[ ${mode_daily} -eq 1 ]]; then

            # Extract the only ads's url that is not downloaded before
            create_need_download_tab "${need_download_file}" 

        # Fully download
        else

            # Download all ads's url in today crawling
            cp "${TAB_FILE}" "${need_download_file}"
        fi

        download_detail_ad "${need_download_file}"
    fi

    # =====================================================================
    # ==================== Parsing data ===================================
    # =====================================================================
    echo "Staring parsing sql file"

    parse_insert_queries "${need_download_file}" "${insert_file}"
    ${work_dir}/parsing_update.sh "${folder_name}"

    # =====================================================================
    # ==================== Import data ====================================
    # =====================================================================
    echo "Staring import data to database"

    if [[ "${mode_import}" -eq 1 ]]; then
        ${work_dir}/import_db.sh "${folder_name}"
    fi

    # =====================================================================
    # ==================== Cleanup and done  ==============================
    # =====================================================================

    echo -e "\033[38;5;10m Finished \033[0m"
    echo -e  "$(date +"%Y-%m-%d %H:%M:%S")\tEND"

    echo "OK" > "${DELTA_FOLDER}/status_ok"
    echo -e  "Date: $(date +"%Y-%m-%d %H:%M:%S")" >> "${DELTA_FOLDER}/status_ok"

    ExitProcess 0

}

main "$@" | tee "${LOG_FOLDER}/log_$(date +"%H")"
