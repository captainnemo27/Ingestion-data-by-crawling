#!/bin/bash

#################################
# IMPORT                        #
#################################
source ../common/Utils.sh
source ../common/list_proxies.sh
source ../common/list_useragent.sh

#################################
# FUNCTION                      #
#################################

function standardized_data () { 
    local data=$1 ;
    local temp="${data}_temp"
	cat "${data}" | awk '{ gsub(/>[ ]*</,">\n<",$0); print $0; }' | awk NF > "${temp}" ; #standardized input text 
	cat "${temp}" > "${data}"
    rm -rf ${temp} ;
}

# Find available user agent and proxy for download
function incrIp() {
	a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
    ((u_a=a % max_useragent))
    # findAliveIP
    # id_proxies=$? 
    #id_proxies=10  
    #PROXY_ARR[$id_proxies]="172.16.1.11:3128"
}

# Sortie finale - Exit
function ExitProcess () {
	status=$1
	if [ "${status}" -ne 0 ]
	then
		echo -e "${usage}"
		echo -e "${error}"
	fi
	rm "${work_dir}/"*.$$ "${work_dir}/${d}/"*.$$ > /dev/null 2>&1
	exit "${status}"
}

# Download -url -file_name -element_to_check_success
function download() {
    # Parameter input
    local link=$1
    local file=$2
    local check_element=$3
    

    local loop=0;local max_loop=3

    while [ ${loop} -lt ${max_loop} ];do
        incrIp
        #proxy="172.16.1.11:3128"
        proxy="${PROXY_ARR[$id_proxies]}"

        ############################################
        # CHANGE DOWNLOAD FUNCTION                 #
        ############################################
        wget -nv  --tries=5 --waitretry=1 -U"${USERAGENT_ARR[$u_a]}" --random-wait -q -O- --header="Content-Type: text/html; charset=UTF-8" --header="Accept-Encoding: gzip" "${link}" | gzip -cdf > "${file}"
        
        local status_of_checking=1
        if grep -q "/html" "${file}";then
            status_of_checking=0
        else
            status_of_checking=1
        fi  
        
        # If string is not empty
        if [ ${status_of_checking} -eq 0 ] && [ -n "${check_element}" ]; then
            if grep -q "${check_element}" "${file}";then
                status_of_checking=0
            else
                status_of_checking=1
            fi
        fi
        
        ((loop=loop+1))
        if [ ${status_of_checking} -ne 0 ]; then # empty text
            rm -f "${file}"
        else
            standardized_data "${file}"
            loop=${max_loop}
        fi
    done
}

# Download Detail -tab_file -max_process
## Tab_file shape:
#################################
## ID_CLIENT_1  SRC_LINK_1  ... #
## ID_CLIENT_2  SRC_LINK_2  ... #
#################################
function downloadDetailMode(){
    # Parameter input
    local tab_file=$1
    local _processMax=$2
    local file=""
    local list_process_pids=()
    
    while read -r line;do
        FS='\t' read -r -a array <<< "$line"
        client_id="${array[0]}"
        src_link="${array[1]}"
        src_link=$(echo "${src_link}" | iconv -c -f utf-8 -t ascii)

        if [ ${#client_id} -eq 0 ] || [ ${#src_link} -eq 0 ];then
            continue; # there are not id_client or url
        fi

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

        file="${all_folder}/annonce_${client_id}.txt"
                        
        if [ ! -s "${file}" ]; then
            # Take the pid and put it in the array
            download "${src_link}" "${file}"  &
            list_process_pids+=($!)
        fi

    done < "${tab_file}"
    # waiting all processes to complete
    wait "${list_process_pids[@]}"
    # Empty an array
    unset list_process_pids
}

#################################
# TEMPLATE                      #
#################################
template(){
    # CONFIG
    # export LANG=C.UTF-8
    trap 'ExitProcess 1' SIGTERM SIGQUIT SIGINT
    echo -e "$(date +"%Y-%m-%d %H:%M:%S")\tDEBUT"

    # DEFINE
    ## Variable often use 
    work_dir=$(pwd)
    ip=0;u_a=0
    id_proxies=0;
}