#!/usr/bin/env bash
#
# Perfom crawling and parsing data from tinbatdongsan.com

#Include libraries

source ../Lib_Offy/Utils.sh
source ../Lib_Offy/list_useragent.sh 
source ../common/list_proxies.sh
# . /usr/local/bin/list_ip.sh
u_a=0

work_dir=$(pwd)
lib_dir="../Lib_Offy"

readonly DOMAIN="https://rongbay.com"
readonly MAX_LOOP=5          # Maximun number of trying re-download html file if failed
readonly SLEEP_SEC=0         # Sleep second between downloading html file
NB_PROCESSES=5              # Number of proocesses when apply multi-processes
TAB="	"
today=$(date +"%Y-%m-%d")
year=$(date +"%Y")
incr_useragent() {
	a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
    let "u_a=a % max_useragent"
    # findAliveIP
    # id_proxies=$? 
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

readonly TABLE_NAME="RONGBAY"
readonly insert_file="${DELTA_FOLDER}/ads_insert.sql"
readonly update_file="${DELTA_FOLDER}/ads_update.sql"
readonly cookie_file="${FOLDER}/cookie.txt"

TOTAL_PAGE=1
# }}} end global variables


# {{{ USER-DEFINED FUNCTIONS
function custom_standardized_data {
    local html_file=$1

    sed -i -e "s/\r//g" "${html_file}"
    awk -f "${lib_dir}/standardized_input.awk"  "${html_file}" > "${html_file}.$$"
    awk NF "${html_file}.$$" > "${html_file}.final"
    rm -rf "${html_file}.$$"
    mv "${html_file}.final" "${html_file}"
}

#######################################
# Custom curl to specific crawling site
# Globals:
#   None
# Arguments:
#   url link to download
#   location to save html file
#######################################
function custom_curl {
    local url=$1
    local save_file=$2
    incr_useragent
 #	proxy="${PROXY_ARR[$id_proxies]}"

    curl -sSL "${url}" \
        -A "${USERAGENT_ARR[$u_a]}" -b "${cookie_file}" \
        -c "${cookie_file}" \
        -H 'referer:' "https://www.google.com/" \
        -H 'accept-encoding: gzip, deflate, br' \
        -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
        -H 'accept: */*' \
        -H 'x-requested-with: XMLHttpRequest' \
        --retry 5  --compressed -o "${save_file}"
}

#######################################
# Hepler function to download web content
# Globals:
#   MAX_LOOP
#   SLEEP_SEC
# Arguments:
#   None
#######################################
function download_page {
    local loop=0
    local url=$1
    local output_file=$2

    while (( ${loop} < ${MAX_LOOP} )); do
        if [[ ! -f "${output_file}" ]] || [[ ! -s "${output_file}" ]]; then 
            custom_curl "${url}" "${output_file}"

            if grep -i "<\/html>" "${output_file}" 1> /dev/null; then
                custom_standardized_data "${output_file}"
                loop=${MAX_LOOP}
            else
                rm -rf "${output_file}"
                (( loop = loop + 1 ))
            fi

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
        local url="${base_url/.html/-trang${page}.html}"

        if [[ "${url}"  == *"Mua-Ban"* ]]; then
            local page_html_file="${LIST_FOLDER}/sale-page-${TOTAL_PAGE}.html"
        else
            local page_html_file="${LIST_FOLDER}/rent-page-${TOTAL_PAGE}.html"
        fi

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
                sleep 1

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
            sleep 1
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

        awk -vtable=${TABLE_NAME} \
            -f ${AWK_FOLDER}/liste_tab.awk \
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
        #rm -rf "${LOG_FOLDER}"

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

        url_sale_types[0]="Cho-thue-nha-c272"
        url_sale_types[1]="Mua-Ban-nha-dat-c15"
        url_sale_types[2]="Cho-thue-van-phong-c296"

        cities[0]="Ha-Noi";                    city_codes[0]=$(seq 68 95)
        cities[1]="TP-HCM";                    city_codes[1]=$(seq 96 120)
        cities[2]="Hai-Phong";                 city_codes[2]=$(seq 121 135)
        cities[3]="Da-Nang";                   city_codes[3]=$(seq 136 143)
        cities[4]="Binh-Duong";                city_codes[4]=$(seq 144 150)
        cities[5]="Khanh-Hoa";                 city_codes[5]=""
        cities[6]="Quang-Nam";                 city_codes[6]=""
        cities[7]="Quang-Ninh";                city_codes[7]=""
        cities[8]="Thua-Thien-Hue";            city_codes[8]=""
        cities[9]="Bac-Ninh";                  city_codes[9]=""
        cities[11]="Thanh-Hoa";                city_codes[11]=""
        cities[12]="Can-Tho";                  city_codes[12]=""
        cities[13]="Ba-Ria-Vung-Tau";          city_codes[13]=""
        cities[14]="Dong-Nai";                 city_codes[14]=""
        cities[15]="Long-An";                  city_codes[15]=""
        cities[16]="Cac-tinh-mien-bac-khac";   city_codes[16]=""
        cities[17]="Cac-tinh-mien-trung-khac"; city_codes[17]=""
        cities[18]="Cac-tinh-mien-trung-khac"; city_codes[18]=""

        # Download list mode of each city
        if [[ "${mode_test}" -ne 1 ]]; then
            rm -rf "${LINK_FILE}"

            for url_sale_type in "${url_sale_types[@]}"; do
                for i in "${!cities[@]}"; do
                    city="${cities[$i]}"
                    mkdir -p "${LIST_FOLDER}/${city}"

                    if [[ -n "${city_codes[$i]}" ]]; then
                        for city_code in ${city_codes[$i]}; do
                            #local url="${DOMAIN}/${city}/Mua-Ban-nha-dat-c15.html?md=${city_code}"
                            local url="${DOMAIN}/${city}/${url_sale_type}.html?md=${city_code}"

                            if [[ "${url_sale_type}" == *"Mua-ban"* ]]; then
                                local save_file="${LIST_FOLDER}/${city}/sale_${city_code}.max"
                            else
                                local save_file="${LIST_FOLDER}/${city}/rent_${city_code}.max"
                            fi

                            download_page "${url}" "${save_file}" && custom_standardized_data "${save_file}"
                            nb_page=$(awk -f "${lib_dir}/Utils.awk" -f ${AWK_FOLDER}/nb_pages.awk ${save_file})

                            echo "${url}${TAB}${nb_page}" >> "${LINK_FILE}"
                        done
                    else
                        local url="${DOMAIN}/${city}/Mua-Ban-nha-dat-c15.html"
                        local save_file="${LIST_FOLDER}/${city}/pages.max"
                        download_page "${url}" "${save_file}" && custom_standardized_data "${save_file}"
                        nb_page=$(awk -f "${lib_dir}/Utils.awk" -f ${AWK_FOLDER}/nb_pages.awk ${save_file})

                        echo "${url}${TAB}${nb_page}" >> "${LINK_FILE}"
                    fi
                done
            done

            remove_duplicated_lines "${LINK_FILE}"
            while IFS="${TAB}" read -a arr; do
                local base_url="${arr[0]}"
                local nb_page="${arr[1]}"

                echo "[list-mode] Starting download list page..."

                if [[ "${nb_page}" -gt 0 ]]; then
                    download_each_listmode_multi "${base_url}" "${nb_page}"
                fi

                wait
            done < "${LINK_FILE}"

        # Test mode
        else
            local base_url="https://rongbay.com/Ha-Noi/Mua-Ban-nha-dat-c15.html"
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
        rm -rf "${TAB_FILE}"

        while read line; do
            local page_html="${line}"
            echo "== parsing extract.tab: $(basename ${page_html})"

            local sale_type="SALE"
            if [[ "${page_html}" == *"rent"* ]]; then
                sale_type="RENT"
            fi

            awk -vcreated_day="${today}" -vyear="${year}" -vsale_type="${sale_type}" \
                -f ${lib_dir}/Utils.awk \
                -f ${AWK_FOLDER}/liste_tab.awk \
                -f ${AWK_FOLDER}/put_html_into_tab.awk \
                "${page_html}" >> "${TAB_FILE}"
        done < <(find "${LIST_FOLDER}" -type f -name '*.html')

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

main "$@"
