#!/usr/bin/env bash
#
# Perfom crawling and parsing data from batdongsan.vn

#Include libraries
source ../Lib_Offy/Utils.sh
source ../Lib_Offy/list_useragent.sh 

work_dir=$(pwd)
lib_dir="../Lib_Offy"
readonly MAX_LOOP=2     # Maximun number of trying re-download html file if failed
readonly SLEEP_SEC=1    # Sleep second between downloading html file
readonly NB_PROCESSES=5 # Number of proocesses when apply multi-processes

## Option parse
mode_download=1
mode_test=0
mode_daily=0
mode_import=0
get_all_ind=1
TAB="	"
reset_ind=0

# . /usr/local/bin/list_ip.sh
u_a=0

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
\t-x debug mode\n\
\t-y test mode ( download 2 single category and 2 pages of list pages for testing )\n\
\t-d [date] (default today)\n\
\t-D Daily download ( previous day is yesterday )\n\
\t-i import SQL to database\n\
\t-r retrieve only, do not download the detailed adds\n\
\t-z site name\n\
\t-h help\n\
"

#while getopts :-aDd:i:I:m:M:rRt:T:hxyz: name
while getopts :xyDirhz:d: name; do
  case $name in

    x)  set -x
        mode_daily=1
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

    h)  echo -e ${usage}
        ExitProcess 0
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

# If the input day is not empty
if [[ -z "${d}" ]]; then
    d=$(date +"%Y%m%d")
    folder_name="${d}"
else
    folder_name="${d}"
fi

unset nb_pages_max
if (( ${mode_test} == 1 )); then
    nb_pages_max=2
fi

# {{{ GLOBAL VARIABLES

#################################
# DEFINE FOLDER TO SAVE         #
#################################
today=$(date +"%Y-%m-%d")
source ../common/db_config.sh "${folder_name}"


readonly FOLDER="${work_dir}/${folder_name}"
readonly ALL_FOLDER="${FOLDER}/ALL"
readonly DELTA_FOLDER="${FOLDER}/DELTA"
readonly LIST_FOLDER="${FOLDER}/LIST_MODE"
readonly LOG_FOLDER="${FOLDER}/LOG"

readonly TAB_FILE="${DELTA_FOLDER}/extract.tab"
readonly AWK_FOLDER="${work_dir}/awk"

readonly TABLE_NAME="BATDONGSAN"
readonly insert_file=${DELTA_FOLDER}/ads_insert.sql
readonly update_file=${DELTA_FOLDER}/ads_update.sql
# }}} end global variables

# {{{ USER-DEFINED FUNCTIONS

#######################################
# Checking if site blocked IP
# Globals:
#   None
# Arguments:
#   url link to download
#   location to save html file
#######################################
function check_ddos {
    html_file=$1
    nb_lines_page=$(wc -l ${html_file} | awk '{ print $1 }')

    if (( ${nb_lines_page} == 1 )); then
        local url="http://www.batdongsan.vn/default.aspx?removedos=true"
        custom_curl "${url}" "/dev/null"

        return $(true)
    else
        return $(false)
    fi
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

    curl -L "${url}" \
        -A "${USERAGENT_ARR[$u_a]}" \
        -x http://172.16.1.11:3128 \
        -H 'accept-encoding: gzip, deflate, br' \
        -H 'accept-language: en-US,en;q=0.9' \
        -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' \
        -H 'accept: */*' \
        -H 'referer:' "${url}" \
        -H 'x-requested-with: XMLHttpRequest' \
        --retry 3 --retry-max-time 10 --max-time 20 --compressed \
        --output "${save_file}" 1> /dev/null

}



function download_list_mode {
    local domain="http://www.batdongsan.vn"
    local category_url="${domain}/giao-dich"


    while read -r line; do
        maxpage_url="${line}"
        maxpage_file="${LIST_FOLDER}/${TOTAL_PAGE_MAX}.max"

        loop=0
        while [[ ${loop} -lt ${MAX_LOOP} ]]; do

            # Determine total of index-pages that contains the ads page to crawl
            # Logic: Download the page-index 0, find the pagination section (tab) of page-index-0
            # to find number of index page of website

            if [[ ! -f "${maxpage_file}" ]] || [[ ! -s "${maxpage_file}" ]]; then 
                incr_useragent
                custom_curl "${maxpage_url}" "${maxpage_file}"
            fi

            grep -i "<\/html>" "${maxpage_file}" 1> /dev/null

            # Check whether html file is valid
            # If invalid, re-download html file
            if [[ $? -ne 0 ]] && check_ddos "${maxpage_file}"; then 
                rm -rf "${maxpage_file}"
                (( loop = loop + 1 ))
            else
                loop=${MAX_LOOP}

                awk -f "${lib_dir}/standardized_input.awk"  "${maxpage_file}" > "${maxpage_file}.$$"
                awk NF "${maxpage_file}.$$" > "${maxpage_file}.final"
                rm -rf "${maxpage_file}.$$"
                mv "${maxpage_file}.final" "${maxpage_file}"
            fi 
        done

        nb_pages=$(awk -f "${lib_dir}/Utils.awk" -f ${AWK_FOLDER}/nb_pages.awk ${maxpage_file})
        download_each_list_mode "${maxpage_url}" "${nb_pages}"
        ((TOTAL_PAGE_MAX = TOTAL_PAGE_MAX + 1))

    done < "${work_dir}/cache/link.tab"
}

#######################################
# Hepler function to download each categories
# in list mode
# store it in LIST_FOLDER
# Globals:
#   MAX_LOOP
#   SLEEP_SEC
# Arguments:
#   None
#######################################
function download_each_list_mode {
    local page_url=$1
    local nb_pages=$2

    if [[ ${page_url} == *"cho-thue-nha-dat"* ]]; then
        local name="rent"
    else
        local name="sale"
    fi

    local page=1
    while [[ ${page} -le ${nb_pages} ]]; do 

        local loop=0
        while (( ${loop} < ${MAX_LOOP} )); do
            page_html_file="${LIST_FOLDER}/${name}-page-${TOTAL_PAGE}.html"
            page_url="${page_url/.html/}"
            url="${page_url}/pageindex-${page}.html"

            if [[ ! -s "${page_html_file}" ]]; then 
                incr_useragent
                custom_curl "${url}" "${page_html_file}"

                awk -f "${lib_dir}/standardized_input.awk" "${page_html_file}" > "${page_html_file}.temp"
                awk NF "${page_html_file}.temp" > "${page_html_file}.final"
                mv "${page_html_file}.final" "${page_html_file}"
                rm -rf "${page_html_file}.temp"

                if check_ddos "${page_html_file}"; then 
                    rm -rf "${page_html_file}"
                    (( loop = loop + 1 ))
                else
                    loop=${MAX_LOOP}
                fi

            else
                loop=${MAX_LOOP}
            fi
        done

        (( page = page + 1 ))
        (( TOTAL_PAGE = TOTAL_PAGE + 1 ))
    done

}

#######################################
# Download each ads in detail mode
# Globals:
#   None
# Arguments:
#   None
#######################################
function download_ad {
    local intial_page=$1
    local step=$2
    shift 2

    local src_links=("$@")

    local page=${intial_page}
    local last_page="${#src_links[@]}"

    while [[ ${page} -lt ${last_page} ]]; do
        local src_link="${src_links[${page}]}"
        local page_file="${ALL_FOLDER}/ads_${page}.txt"

        if [[ ! -f "${page_file}" ]] || [[ ! -s "${page_file}" ]]; then
            incr_useragent 
            custom_curl "${src_link}" "${page_file}"

            awk -f ${lib_dir}/standardized_input.awk "${page_file}" > "${page_file}.temp"
            awk NF "${page_file}.temp" > "${page_file}"
            rm -rf "${page_file}.temp"


            # Check DDOS blocked from batdongsan.vn
            # When sites detect too many requests. It will send
            # link http://www.batdongsan.vn/default.aspx?removedos=true
            # to verify whether the robot
            if check_ddos "${page_file}"; then
                echo "== ads_${page}.txt...Re-download"
            else
                echo "== ads_${page}.txt...OK" 
                (( page = page + step ))
            fi

        else
            (( page = page + step ))
        fi

    done
}

function create_extract_tab {
    while read line; do
        page_html="${line}"
        echo "== parsing insert: $(basename ${page_html})"

        local sale_type="SALE"
        if [[ "${page_html}" == *"rent"* ]]; then
            sale_type="RENT"
        fi

        awk -vcreated_day=$today -vsale_type="${sale_type}" \
            -f ${lib_dir}/Utils.awk \
            -f ${AWK_FOLDER}/list_tab.awk \
            -f ${AWK_FOLDER}/put_html_into_tab.awk \
            "${page_html}" >> "${TAB_FILE}.$$"

    done < <(find "${LIST_FOLDER}" -type f -name '*.html')

    # sort unique to remove double lines
    sort -u -k1,1 -t"${TAB}" "${TAB_FILE}.$$" >> "${TAB_FILE}"
    rm -rf "${TAB_FILE}.$$"
}

function parse_insert_queries {
    local tab_file=$1

    if [[ -f "${tab_file}" ]]; then
        echo "create extract.tab...OK"

        awk -vtable=${TABLE_NAME} -vcreated_day="${today}" \
            -f ${AWK_FOLDER}/list_tab.awk \
            -f ${AWK_FOLDER}/put_tab_into_db.awk \
            "${tab_file}" > "${insert_file}"
    fi
}

######################################################################
########################### Main #####################################
######################################################################

function main {

    TOTAL_PAGE=1
    TOTAL_PAGE_MAX=1

    if [[ ${get_all_ind} -eq 1 ]]; then
        echo "Cleaning folder"
        #rm -rf "${LOG_FOLDER}"

        echo "Creating the folders"
        echo $FOLDER
        echo $ALL_FOLDER
        echo $DELTA_FOLDER
        echo $LIST_FOLDER
        mkdir -p ${ALL_FOLDER} ${DELTA_FOLDER} ${LIST_FOLDER} ${LOG_FOLDER}
    fi

    # check FOLDER create successful
    if [[ ! -d "${FOLDER}" ]]; then
        exit_process 1
    fi


    # ========== Download list mode ==========

    # check retrieve data only (-r option)
    if [[ "${mode_download}" -eq 1 ]] && [[ ${get_all_ind} -eq 1 ]]; then
        echo "Starting download list page..."
        download_list_mode
    fi

    # Create extract.tab file for parsing insert sql
    # and (detail) ads url
    rm -rf "${TAB_FILE}"

    echo "Starting create extract.tab and parse insert sql"
    create_extract_tab

    #========== Download detail mode ==========

    echo "Starting download the ads (detail)"

    local today_extract="${TAB_FILE}"
    local download_extract="${DELTA_FOLDER}/need_download.tab"

    # Download only if mode_detail mode is set
    if [[ ${mode_download} -eq 1 ]] && [[ ${get_all_ind} -eq 1 ]] && [[ -f "${TAB_FILE}" ]]; then

        # Mode daily
        # Algorithm:
        #     - Find the extract.tab file of today to get id_client ("today")
        #     - Find the extract.tab file of most recent date to get id_client ("most_recent")
        #     - Get id_client, url that have in "today" but not in "most_recent" (join command -v option)
        #     - Save the result to "download_extract" file
        #     - If fully download mode, "download_extract" is same as "today"
        if [[ ${mode_daily} -eq 1 ]]; then
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
                cp "${today_extract}" "${download_extract}"
            else
                local most_recent_tab="${work_dir}/${most_recent_date}/DELTA/extract.tab"

                # Get id_clients that is not exist in most recent date data
                # id_client diff = id_client_today - id_client_most_recent_date
                join -t"${TAB}" -v1 "${today_extract}" "${most_recent_tab}" > "${download_extract}"
            fi

        # Fully download
        else
            cp "${today_extract}" "${download_extract}"
        fi

        declare -a src_links

        # Get all ads links to run multi-process
        while read id_client src_link a b c de e f g; do
            src_links+=("${src_link}")
        done < "${download_extract}"

        process_list=()

        rm -rf "${LOG_FOLDER}/detailmode_proc.txt"
        for ((pro_i=0; pro_i < NB_PROCESSES; pro_i++)); do
            download_ad ${pro_i} ${NB_PROCESSES} "${src_links[@]}"  &
            process_list+=($!)
            echo "$!" >> "${LOG_FOLDER}/detailmode_proc.txt"
            sleep 1
        done

        wait "${process_list[@]}"
    fi

    #============== Parsing ads data
    echo "Staring parse update sql"
    parse_insert_queries "${download_extract}"
    ${work_dir}/parsing_update.sh "${folder_name}" 

    if [[ "${mode_import}" -eq 1 ]]; then
        ${work_dir}/import_db.sh "${folder_name}"
    fi

    echo -e "\033[38;5;10m Finished \033[0m"
    echo -e  "$(date +"%Y-%m-%d %H:%M:%S")\tEND"

    echo "OK" > "${DELTA_FOLDER}/status_ok"
    echo -e  "Date: $(date +"%Y-%m-%d %H:%M:%S")" >> "${DELTA_FOLDER}/status_ok"
    echo "Nb of ads: ${#src_links[@]}"  >> "${DELTA_FOLDER}/status_ok"

    ExitProcess 0

}

main "$@" | tee "${LOG_FOLDER}/log_$(date +"%H:%M")"

