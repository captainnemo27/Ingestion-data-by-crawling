#!/bin/bash
source ./utils/utils.sh
# set -x

#################################
# IMPORT TEMPLATE               #
#################################
template

#################################
# PARSE OPTION                  #
#################################
## usage / mode d'emploi du script
usage="download_site.sh\n\
\t-a no download - just process what's in the directory\n\
\t-d [date] (default today)\n\
\t-h help\n\
\t-D Download Ads dont have in previous date \n\
\t-i Dont push sql to DB \n\
\t-r retrieve only, do not download the detailed adds\n\
\t-x debug mode - verbose ligne par ligne\n\
\t-y mode TEST telecharge 2 pages seulement \n\
\t-z nom du site - optionnel juste utile pour savoir ce qui tourne lorsqu'on fait \"ps\" \n\
"
## Option parse
lynx_ind=1
get_all_ind=1
mode_test=0
mode_import=0
delta_ind=0
today=`date +"%Y-%m-%d"`
TAB=" "

while getopts :-ad:rhxt:yz:Di name
do
    case $name in

        a)  lynx_ind=0
        ((shift=shift+1))
        ;;

        d) 	d=$OPTARG
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

# verification si on a mis un argument non attendu
if [ $# -ne 0 ]
then
        error="Bad arguments, $@"
        ExitProcess 1
fi

# si la date n'est pas indiquee on met la date du jour par defaut
if [ "${d}X" = "X" ]
then
    d=$(date +"%Y%m%d")
fi

source ../common/db_config.sh "${d}"

#################################
# FUNCTION                      #
#################################

# Download List Mode -max_process
function download_list_mode(){    
    local _processMax=$1

    # Define
    local category_index=0
    local sub_category_index=0
    local sub_sub_category_index=0
    local k_flag=0
    local stop_down_list=()
    local page_list_current=0
    local url
    local file_download
    local loop_to_get_max_page
    local category_url="https://mogi.vn/"
    
    
    local list_process_pids=()
    
    # Remove Tab file if exist
    if [ -f "${tab_file}" ]; then
        rm -f "${tab_file}"
    fi

    # sub_sub_category - third floor
    mua_nha=("mua-nha-mat-tien-pho" "mua-nha-biet-thu-lien-ke" "mua-duong-noi-bo" "mua-nha-hem-ngo")
    mua_can_ho=("mua-can-ho-chung-cu" "mua-can-ho-tap-the-cu-xa" "mua-can-ho-penthouse" "mua-can-ho-dich-vu" "mua-can-ho-officetel")
    mua_dat=("mua-dat-tho-cu" "mua-dat-nen-du-an" "mua-dat-nong-nghiep" "mua-dat-kho-xuong")
    mua_mat_bang_cua_hang_shop=("mua-mat-bang-cua-hang-shop-quan-an-nha-hang" "mua-mat-bang-cua-hang-shop-cafe-do-uong" \
        "mua-mat-bang-cua-hang-shop-thoi-trang-my-pham-thuoc" "mua-mat-bang-cua-hang-shop-spa-tiem-toc-nail" \
        "mua-cua-hang-shop-shophouse" "mua-mat-bang-cua-hang-shop-nhieu-muc-dich")

    thue_nha=("thue-nha-mat-tien-pho" "thue-nha-biet-thu-lien-ke" "thue-duong-noi-bo" "thue-nha-hem-ngo")
    thue_can_ho=("thue-can-ho-chung-cu" "thue-can-ho-tap-the-cu-xa" "thue-can-ho-penthouse" "thue-can-ho-dich-vu" "thue-can-ho-officetel")
    thue_phong_tro_nha_tro=("thue-phong-tro-khu-nha-tro" "thue-phong-tro-loi-di-rieng" "thue-phong-tro-o-chung-chu" "thue-phong-tro-o-ghep")
    thue_van_phong=("thue-van-phong-toa-nha-cao-oc" "thue-van-phong-tt-thuong-mai" \
        "thue-van-phong-ao-tron-goi" "thue-van-phong-nha-rieng-can-ho" "thue-van-phong-officetel")
    thue_mat_bang_cua_hang_shop=("thue-mat-bang-cua-hang-shop-quan-an-nha-hang" "thue-mat-bang-cua-hang-shop-cafe-do-uong" \
        "thue-mat-bang-cua-hang-shop-thoi-trang-my-pham-thuoc" "thue-mat-bang-cua-hang-shop-spa-tiem-toc-nail" \
        "thue-cua-hang-shop-shophouse" "thue-mat-bang-cua-hang-shop-nhieu-muc-dich")
    thue_nha_xuong_kho_bai_dat=("thue-nha-xuong" "thue-nha-kho" "thue-bai-de-xe" "thue-dat-trong")

    # sub_category - second floor
    mua=(mua_nha mua_can_ho mua_dat mua_mat_bang_cua_hang_shop)
    thue=(thue_nha thue_can_ho thue_phong_tro_nha_tro thue_van_phong thue_mat_bang_cua_hang_shop thue_nha_xuong_kho_bai_dat)

    # category - first floor
    category=(mua thue)

    if [ ${mode_test} -eq 1 ];then
        mua_nha=("mua-nha-mat-tien-pho" "mua-nha-biet-thu-lien-ke")
        mua_can_ho=("mua-can-ho-chung-cu" "mua-can-ho-tap-the-cu-xa")

        thue_nha=("thue-nha-mat-tien-pho" "thue-nha-biet-thu-lien-ke")
        thue_can_ho=("thue-can-ho-chung-cu" "thue-can-ho-tap-the-cu-xa")

        mua=(mua_nha mua_can_ho)
        thue=(thue_nha thue_can_ho)

        category=(mua thue)
    fi

    declare -n sub_category sub_sub_category
    # Read category - first floor
    for sub_category in "${category[@]}"; do
        # # Read parameter of first floor
        # echo "${category[$category_index]}"
        sub_category_index=0

        # Read sub_category - second floor
        for sub_sub_category in "${sub_category[@]}"; do
            # # Read parameter of second floor
            # echo "${sub_category[$sub_category_index]}"
            
            # Read sub_sub_categoy - third floor
            for sub_sub_category_index in ${!sub_sub_category[@]}; do
                # # Read parameter of third floor
                # echo ${sub_sub_category[$sub_sub_category_index]}

                stop_down_list[$sub_sub_category_index]=0
                page_list_current=1
                # Make list folder model
                list_folder_model="${list_folder}/${category[$category_index]}/${sub_category[$sub_category_index]}"
                list_tab_folder="${tab_folder}/${category[$category_index]}/${sub_category[$sub_category_index]}"
                

                mkdir -p "$list_folder_model" "$list_tab_folder" 

                # Url:https://mogi.vn/thue-nha-xuong?cp=1
                url="${category_url}${sub_sub_category[$sub_sub_category_index]}?cp=${page_list_current}"

                # file: page-mua-can-ho-1.html
                file_download="${list_folder_model}/page-${sub_sub_category[$sub_sub_category_index]}-${page_list_current}.html"
                
                # Take max page
                max_page=0
                loop_to_get_max_page=0
                while [ ${loop_to_get_max_page} -lt 20 ] && [ ${max_page} -eq 0 ]; do
                    if [ ! -s "${file_download}" ]; then
                    download "${url}" "${file_download}" 
                    fi
                    temp_max_page=$(awk -f ../common/Utils.awk -f "${awk_dir}/get_max_page.awk" "${file_download}")
                    if [ ${temp_max_page} -gt 0 ]; then
                        max_page=${temp_max_page}
                    else
                    ((loop_to_get_max_page++))
                    fi
                done
                


                # If cant get max page skip for another category
                if [ ${max_page} -eq 0 ];then
                    stop_down_list[$sub_sub_category_index]=1
                fi

                # Start download list mode
                while [ ${stop_down_list[$sub_sub_category_index]} -ne 1 ]; do
                    ((page_list_current=page_list_current+1))
                    
                    # Url:https://mogi.vn/thue-nha-xuong?cp=1
                    url="${category_url}${sub_sub_category[$sub_sub_category_index]}?cp=${page_list_current}"

                    # file: page-mua-can-ho-1.html
                    file_download="${list_folder_model}/page-${sub_sub_category[$sub_sub_category_index]}-${page_list_current}.html"
                    
                    # Check max process or not
                    while [ "${#list_process_pids[@]}" -gt "${_processMax}" ]; do
                        for i in ${!list_process_pids[@]} ; do # loop key in list_process_pids
                        
                            # Check the pid done or not
                            # if ! kill -0 "${list_process_pids[${i}]}" ; then 

                            # The pid is gone
                            if ! ps -p "${list_process_pids[${i}]}" > /dev/null ; then
                                unset "list_process_pids[${i}]" # Remove the pid out of the list_process_pids
                            fi
                        done
                        if [ "${#list_process_pids[@]}" -lt "${_processMax}" ]; then
                            break
                        fi
                        sleep 2s
                    done

                    # Download file list mode
                    download_the_file_in_list_mode "${url}" "${file_download}"  &

                    # Take the pid and put it in the array
                    list_process_pids+=($!)
                    # Conditional for stoping
                    if [ ${page_list_current} -ge "${max_page}" ]; then
                        stop_down_list[$sub_sub_category_index]=1
                    fi
                    # If test mode
                    if [ ${mode_test} -eq 1 ] && [ ${page_list_current} -eq 2 ]; then
                        stop_down_list[$sub_sub_category_index]=1
                    fi
                done
                # waiting all processes to complete
                wait "${list_process_pids[@]}"

                # Parse all files in model folder.
                find "${list_folder_model}" -name page-${sub_sub_category[$sub_sub_category_index]}\*.html -exec awk -vmodel="${sub_sub_category[$sub_sub_category_index]}" -vtype="${category[$category_index]}" -vcreated_day="$today" -f ../common/Utils.awk -f "${awk_dir}/list_tab.awk" -f "${awk_dir}/put_html_into_tab.awk" {} \; >>  "${list_tab_folder}/${sub_sub_category[$sub_sub_category_index]}"
                # Put model extract tab to the main extract tab
                cat "${list_tab_folder}/${sub_sub_category[$sub_sub_category_index]}" >> "${tab_file}"
            done
            ((sub_category_index=sub_category_index+1))

        done
        ((category_index=category_index+1))
    done

    # # waiting all processes to complete
    wait "${list_process_pids[@]}"
    # Empty an array
    unset list_process_pids
}

# Function to download file for List Mode
function download_the_file_in_list_mode(){
    # Download file with the mark
    if [ ! -s "${2}" ]; then
        download "${1}" "${2}" "${3}" "$4"
    fi
    # Download the file with the default mark
    if [ ! -s "${2}" ]; then
        download "${1}" "${2}" "${3}"
    fi
}

#################################
# DEFINE FOLDER TO SAVE         #
#################################
folder="${work_dir}/${d}"
tab_file="${folder}/DELTA/extract.tab"
tab_folder="${folder}/TAB"
all_folder="${folder}/ALL"
delta_folder="${folder}/DELTA"
list_folder="${folder}/LIST_MODE"
cookie_file="${folder}/cookie.txt"
config_file="${work_dir}/configs"
awk_dir="${work_dir}/awk"
bash_dir="${work_dir}/bash"
site_name="VN_MOGIVN"
#################################
# DEFINE MAX PROCESS TO RUN     #
#################################
processMax=5

#################################
# MAIN                          #
#################################
main(){
    # on cree le dossier avec la date
    mkdir -p "${all_folder}" "${delta_folder}" "${list_folder}" "${tab_folder}"
    if [ ${lynx_ind} -eq 1 ] && [ ${get_all_ind} -eq 1 ]; then
        # Download list mode
        download_list_mode ${processMax}
        # Backup tab file
        cp "${tab_file}" "${tab_file}.bk"
        # Remove duplicated tab file
        remove_duplicated_lines "${tab_file}"
    fi

        # Run if the daily mode is enable
    if [ ${delta_ind} -eq 1 ]; then
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
        downloadDetailMode ${tab_file} ${processMax}   
    fi

    # #######################
    # Invoke parsing data   #
    # #######################

    ${bash_dir}/parsing_insert.sh "${d}" "${tab_file}"
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


    if [ "${mode_import}" -eq 1 ];then 
        ${bash_dir}/import_db.sh "${d}"
    fi
    
    echo "ok" > "${work_dir}/${d}/DELTA/status_ok"
    echo "Finished!"
    echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tEND"  
}
main