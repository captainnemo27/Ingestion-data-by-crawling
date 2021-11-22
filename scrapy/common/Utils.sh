#!/bin/bash 

############################################################
# THIS FILE CONTAINS COMMON FUNCTIONS FOR PROJECT AUTOBIZ  #
############################################################
work_dir=`pwd`;

#############################
# Standardized input text   #
#############################
#Example: <a>bcd</a><b>asd</b>
#Result:
#	<a>bcd</a>
#	<b>asd</b>
function standardized_data () {
  	data=$1 ;
	cat $data | awk '{ gsub("><",">\n<",$0); print $0; }' > ${work_dir}/tmp.txt.$$ ; #standardized input text 

	#remove multi break new line 
	awk NF ${work_dir}/tmp.txt.$$ > $data ;
	rm -rf ${work_dir}/tmp.txt.$$ ;

}

function standardized_all_files_in_folder () { 
	find $1/ -type f > ${work_dir}/list_html.tab.$$
	
	while read fn; do 
		standardized_data $fn
	done < ${work_dir}/list_html.tab.$$	
	rm -rf ${work_dir}/list_html.tab.$$
}


###############################################
# Remove all incompleted files HTML in folder #
# Parameters:				      #	
# + $1 : folder contains files HTML	      #	
###############################################
function remove_incompleted_files_html(){
	find $1/ -type f > ${work_dir}/list_html.tab.$$ 
	while read fn; do 
		grep -i "<\/html>" $fn
		if [ $? -ne 0 ]; then 
			rm -rf $fn		
		fi 
	done < ${work_dir}/list_html.tab.$$ 	
	rm -rf ${work_dir}/list_html.tab.$$
} 

###############################################
# Check incompleted files HTML 		      #	
# Parameters:				      #	
# + $1 : file need to check 		      #	
# Result:				      #
#	1: file is incompleted code	      # 
#	0: file is completed code 	      #	
###############################################
function check_incompleted_file_html(){
	grep -i "<\/html>" $1
	if [ $? -ne 0 ]; then 
		return 1;		
	fi 
	return 0;	
} 

#########################################
# Remove all empty files HTML in folder #
# Parameters:		      	        #	
# + $1 : folder contains files HTML     #	
#########################################
function remove_empty_files_html(){
	find $1/ -empty -type f -delete
} 


###############################################
# Remove duplicated lines in file	      #
# Parameters:				      #	
# + $1 : file need to remove duplicated lines #	
###############################################
#Example: 
#	a
#	a
#	b
#Result:
#	a
#	b
function remove_duplicated_lines(){
	TAB="	"
	data=$1;
	sort -u -k1,1 -t"${TAB}" $data > tmp.txt.$$;
	mv tmp.txt.$$ $data;
}

###################################
# Find avaible strom proxy	      #
# Return: index					  #	
###################################
function findAliveIP(){
	local result=0;
	local count=1; # note number failures  
	local condition=1;

	until [ 0 -eq 1 ]
	do
		a=$(od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g')
    ((id_proxies=a % max_proxy))

    # If number failures is 3 times => use main proxy with id_proxies, having 0 value 
    ((condition=count%3))

    if [ ${condition} -eq 0 ]; then
      id_proxies=0; # index of main proxy 
    fi
		
    result=$(wget -e use_proxy=yes -e https_proxy="${PROXY_ARR[$id_proxies]}" -nv --no-check-certificate --timeout=5 --tries=1 --waitretry=1 -qO- https://geoip.hmageo.com/json | awk 'BEGIN{value=0} /"country_name":/{ value=1; } END{ print value;}')
		
    if [ ${#result} -ne 0 ]
		then
			if [ "${result}" -eq 1 ];then
				#echo "get id:$id_proxies"
				return $id_proxies;
			fi
		fi

    # Increase number failures  
		((count++))
	done
}

##############################
# Find a good residential IP #
##############################
function findResidentialIP(){

    max_proxy=${#PROXY_ARR[@]}

	until [ 0 -eq 1 ]
	do

		a=$(od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g')
		((id_proxies=a % max_proxy))
		
		result=$(wget -e use_proxy=yes -e https_proxy="${PROXY_ARR[$id_proxies]}" -nv --no-check-certificate --timeout=3 --tries=1 --waitretry=1 -qO- https://geoip.hmageo.com/json | awk 'BEGIN{value=0} /"country_name":/{ value=1; } END{ print value;}')
			
		if [ ${#result} -ne 0 ]
		then
			if [ "${result}" -eq 1 ];then
				return $id_proxies;
			fi
		fi
	done
}

#####################################################
# Find missed records in extract.tab 				#
# Compare with file .sql			 				#
# Return data to a file	: follow fileTab content	#
# Param 1: fileTab									#
# Param 2: fileSql									#
# Param 3: fileSave									#
#####################################################
function findMissRecords(){
	local fileTab=$1
	local fileSql=$2
	local fileSave=$3
	if [ ${#fileTab} -eq 0 -o ${#fileSql} -eq 0 -o ${#fileSave} -eq 0 ]; then
		echo "Missed params!"
	else
		# Check existence of fileSave. If it exists, remove it first.
		if [ -f "$fileSave" ]; then
			rm -f $fileSave
		fi
		# Read line by line fileTab and get the column 1 for idClient.
		while read -r line; do
			FS='\t' read -r -a array <<< "$line"
			idClient="${array[0]}"
			# Check existence of idClient in the fileSql
			grep -q "${idClient}" $fileSql
			if [ $? -eq 1 ]; then
				( IFS=$'\t'; echo "${array[*]}" ) >> $fileSave
			fi
		done < $fileTab
	fi
}

#########################################################################################
# DESCRIPTION: Use this function to compare extract tab between now and last month.		#
# PARAMETER:																			#
#	+	$1 Date download site.															#
# NOTE: 																				#
#	+	extract.tab site should be in this uri (workDir/<date>/extract.tab)			#
#	+	folder ALL store all detail site file with this uri (workDir/<date>/ALL/*.html)#
#########################################################################################
function compareExtractTab(){
	# Load parameter
	local dateNow=$1
	local dateLast=$2

	# Define Variable
	## Get workplace dir
	local workDir=`pwd`
	
	## Define dir of extract tab
	local extractTabDateNow="${workDir}/${dateNow}/DELTA/extract.tab"
	local extractTabDateLast="${workDir}/${dateLast}/DELTA/extract.tab"

	## Define new tab 
	local repeatedIdExtractTab="${workDir}/${dateNow}/repeated_id_extract.tab"
	local differentIdExtractTab="${workDir}/${dateNow}/different_id_extract.tab"
	
	## Compare 1 collumn
	#################################################
	####TAB 1:										#
	#		A	https://abc.com	...					#
	#		B	https://bcd.com	...					#
	#		C	https://vmn.com	...					#
	#		F	https://opm.com	...					#
	####TAB 2:										#
	#		A	https://abc.com	...					#
	#		B	https://bcd.com	...					#
	#		D	https://ioc.com	...					#
	#################################################
	####TAB	3 ( repeated ):							#
	#		A	https://abc.com ...					#
	#		B	https://bcd.com	...					#
	#################################################
	####TAB	4 ( defferent ):						#
	#		C	https://vmn.com	...					#
	#		F	https://opm.com	...					#
	#################################################
	local temp_file="./temp.$$"
	sort "${extractTabDateNow}" > "${temp_file}"
	cat "${temp_file}" > "${extractTabDateNow}"
	sort "${extractTabDateLast}" > "${temp_file}"
	cat "${temp_file}" > "${extractTabDateLast}"

	join -t "$(printf '\t')" "${extractTabDateNow}" "${extractTabDateLast}" -v 1 > "${differentIdExtractTab}"
	sort "${differentIdExtractTab}" > "${temp_file}"
	cat "${temp_file}" > "${differentIdExtractTab}"

	join -t "$(printf '\t')" "${extractTabDateNow}" "${differentIdExtractTab}" -v 1 > "${repeatedIdExtractTab}"
	sort "${repeatedIdExtractTab}" > "${temp_file}"
	cat "${temp_file}" > "${repeatedIdExtractTab}"

	## Define dir of ALL folder
	local allFolderDateNow="${workDir}/${dateNow}/ALL/"
	local allFolderDateLast="${workDir}/${dateLast}/ALL/"

	local temp_name_now
	local temp_name_last
	while read -r line; do
		# Back up line
		temp="${line}"

		FS='\t' read -r -a array <<<"$line"
		clientId="${array[0]}"
		file="annonce_${clientId}.*"
		temp_name_now=`find "${allFolderDateNow}" -name "${file}"`
		if [ ! -s "${temp_name_now}" ];then
			temp_name_last=`find "${allFolderDateLast}" -name "${file}"`
			if [ ! -s "${temp_name_last}" ];then
				## Old file from folder ALL dateLast not exist - Maybe broken when downloading dateLast
				## Copy back to differentTab for download that file again
				echo "${temp}" >> "${differentIdExtractTab}"
			else
				## Copy file from folder ALL dateLast to folder ALL dateNow
				cp -v "${temp_name_last}" "${allFolderDateNow}"
			fi
		fi
	done <"${repeatedIdExtractTab}"

	sort "${differentIdExtractTab}" > "${temp_file}"
	cat "${temp_file}" > "${differentIdExtractTab}"
	join -t "$(printf '\t')" "${repeatedIdExtractTab}" "${differentIdExtractTab}" -v 1 > "${temp_file}"
	sort "${temp_file}" > "${repeatedIdExtractTab}"

	## Rename differentTab to extract.tab
	mv "${extractTabDateNow}" "${workDir}/${dateNow}/extract.tab.bk"
	mv "${differentIdExtractTab}" "${extractTabDateNow}" 
	rm "${temp_file}"
}