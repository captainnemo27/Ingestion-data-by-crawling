#!/bin/bash

#################################
# IMPORT                        #
#################################
source ../common/Utils.sh
source ../common/list_useragent.sh

#################################
# FUNCTION                      #
#################################
function custom_sleep (){
    a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
    let "second=(a+3)%5" 
    sleep ${second}
}

# Find available user agent and proxy for download
function incr_ip() {
	a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
    ((u_a=a%max_useragent))
    id_proxies=10
    # To get the primary IP address of the local machine on Linux
    PROXY_ARR[$id_proxies]=$(hostname -I | cut -d' ' -f1)
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
function check_process(){
       # Will have the same kind of problem with processes freezing when downloading with jsdom.
       # This process will kill all phantomjs processes which takes long time to run. 
       # $ ps h -o etime,pid,args | grep phantomjs
       #  00:37  139849 /bin/bash ./test.sh nameps=phantomjs
       # pid is on 2nd col.

      ps h -o etime,pid,args | grep phantomjs | awk -F\: '{nb=split($NF,ar_2," "); pid=ar_2[2]; if($1>2){print "kill -9 "pid }}' > ${work_dir}/${d}/kill.eval
      nb=`wc -l ${work_dir}/${d}/kill.eval | awk '{print $1}'`
      if [ ${nb} -gt 0 ];  then
         . ${work_dir}/${d}/kill.eval
      fi
}
function download_phantomjs() {
  local link=$1
  local file=$2
  local check_element=$3
  local loop=0
  local max_loop=5

#   standard_html(){
#     temp_data=$(< "${file}" awk '{ gsub(/></,">\n<",$0); print $0; }')
#     # The good pattern is gsub(/>[\s\t]*</,">\n<",$0)
#     #remove multi break new line
#     echo "${temp_data}" | awk NF > "${file}"
#   }
  echo "Downloading file:  ${file}"
  while [ ${loop} -lt ${max_loop} ];do
    incr_ip
    proxy=""
    # // phantomjs main.js "172.16.1.11:3128" "https://dothi.net/ban-nha-biet-thu-lien-ke-xa-me-tri/ban-biet-thu-mat-ho-10ha-vinhomes-green-bay-cam-ket-gia-chinh-xac-va-tot-nhat-85-ty-0902962999-pr13339818.htm"
    phantomjs ../Lib_Offy/phantomjs-crawling/main.js "$proxy"  "$link" "$file" "${USERAGENT_ARR[$u_a]}" 
    if grep -i -q "</html>" "${file}"; then
        # If string is not empty
        if [ -n "${check_element}" ]; then
            if grep -i -q "${check_element}" "${file}"; then
                #standard_html
                return 0
            fi
        else
            #standard_html
            return 0
        fi
    fi
    rm -f "${file}"
    custom_sleep
    ((loop++))
  done
  return 1
}
function download_html() {
  local link=$1
  local file=$2
  local check_element=$3
  local loop=0
  local max_loop=5

#   standard_html(){
#     temp_data=$(< "${file}" awk '{ gsub(/></,">\n<",$0); print $0; }')
#     # The good pattern is gsub(/>[\s\t]*</,">\n<",$0)
#     #remove multi break new line
#     echo "${temp_data}" | awk NF > "${file}"
#   }
  echo "Downloading file:  ${file}"
  while [ ${loop} -lt ${max_loop} ];do
    incr_ip
    #  Download Compressed File By Sending gzip Headers and Uncompress by using gzip
    wget --bind-address="${PROXY_ARR[$id_proxies]}" -nv --max-redirect=0 --timeout=60 --tries=5 --waitretry=1 -U"${USERAGENT_ARR[$u_a]}" --random-wait --keep-session-cookies --save-cookies=${work_dir}/${d}/cookies.$$ -q -O- --header="Accept-Encoding: gzip" "${link}" | gzip -cdf > "${file}"
    if grep -i -q "<\/html>" "${file}"; then
        # If string is not empty
        if [ -n "${check_element}" ]; then
            if grep -i -q "${check_element}" "${file}"; then
                #standard_html
                return 0
            fi
        else
            #standard_html
            return 0
        fi
    fi
    rm -f "${file}"
    custom_sleep
    ((loop++))
  done
  return 1
}
function download_sub(){
    if [ ! -s "${2}" ]; then
        download_html "${1}" "${2}" "${3}"
    fi
    if [ ! -s "${2}" ]; then
        download_html "${1}" "${2}"
    fi
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
