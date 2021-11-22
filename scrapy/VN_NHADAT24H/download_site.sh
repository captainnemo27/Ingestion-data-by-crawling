#!/bin/bash
. ../Lib_Offy/list_useragent.sh 
. ../Lib_Offy/list_openvpn.sh 
. ../Lib_Offy/Utils.sh 

# faire tourner l'IP et le USER_AGENT
incr_ip() {
	a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
        let "u_a=a % max_useragent"
}

clean_sql_files(){
	echo "cleaning data in sql files"
	sort ${work_dir}/${d}/${d}_${split}/DELTA/extract.tab > ${work_dir}/${d}/${d}_${split}/DELTA/extract_sorted.txt

	awk '{split($0, ar, "ID_CLIENT=\""); split(ar[2], arr, "\""); print arr[1]}' ${work_dir}/${d}/${d}_${split}/DELTA/update.sql > ${work_dir}/${d}/${d}_${split}/DELTA/id_update.txt
	sort ${work_dir}/${d}/${d}_${split}/DELTA/id_update.txt > ${work_dir}/${d}/${d}_${split}/DELTA/id_update_sorted.txt

	join -j 1 -t $'\t' ${work_dir}/${d}/${d}_${split}/DELTA/extract_sorted.txt ${work_dir}/${d}/${d}_${split}/DELTA/id_update_sorted.txt > ${work_dir}/${d}/${d}_${split}/DELTA/extract_temp.txt

	mv ${work_dir}/${d}/${d}_${split}/DELTA/extract_temp.txt ${work_dir}/${d}/${d}_${split}/DELTA/extract.tab

	rm ${work_dir}/${d}/${d}_${split}/DELTA/*.txt

	echo "done cleaning data in sql files"
}

# parse site
download_listmode() {
	url_site=$1;
	page=$2;
	split=$3

	if [ ! -s ${work_dir}/${d}/${d}_${split}/page-${page}.html ]
	then
		loop=0
		while [ ${loop} -lt ${max_loop} ]
		do
			test ${lynx_ind} -eq 1 && incr_ip
			test ${lynx_ind} -eq 1 && phantomjs --proxy=172.16.1.11:3128 injectme.js "${url_site}${page}" ${work_dir}/${d}/${d}_${split}/page-${page}.html
		
			# on verifie que la page a ete telechargee jusqu'au bout (presence du </html>)
			grep -i "</html>" ${work_dir}/${d}/${d}_${split}/page-${page}.html
			if [ $? -ne 0 ]; then
				rm -f ${work_dir}/${d}/${d}_${split}/page-${page}.html
				let "loop=loop+1"
			else
				# call function standardized_data in Lib_Offy/Utils.sh
				standardized_data ${work_dir}/${d}/${d}_${split}/page-${page}.html
				loop=${max_loop}
			fi
		done
	fi
}

download_detailmode_parsing() {
	mysql -u root -p123456789 REAL_ESTATE_VN -e "Select ID_CLIENT from NHADAT24H" > ${work_dir}/${d}/ID_CLIENT.txt

	find ${work_dir}/${d}/${d}_${split}/ -name page-\*.html -exec awk -vdate=${date} -vstart=${start} -vend=${end} -f liste_tab.awk -f ../Lib_Offy/Utils.awk -f ${work_dir}/put_html_into_tab.awk {} \; > ${work_dir}/${d}/${d}_${split}/extract.$$

	# on prepare le script de telechargement du mode detail
	# cree un fichier extract des annonces avec ID unique
	sort -u -k1,1 -t"${TAB}" ${work_dir}/${d}/${d}_${split}/extract.$$ > ${work_dir}/${d}/${d}_${split}/DELTA/extract.tab
	nb_processus=5;
	i=0;
	while read -r line
	do
		FS='\t' read -r -a array <<< "$line"
		id_client=${array[0]}
		src_link=${array[1]}

		if [ ${#id_client} -eq 0 -o ${#src_link} -eq 0 ];then
			continue; # there are not id_client or url 
		fi

		grep ${id_client} ${work_dir}/${d}/ID_CLIENT.txt
		if [ $? -eq 0 ]
		then 
			echo "duplicated : "${id_client} >> ${work_dir}/${d}/duplicated.txt
			grep -v ${id_client} ${work_dir}/${d}/${d}_${split}/DELTA/extract.tab > ${work_dir}/${d}/${d}_${split}/DELTA/extract_temp.tab
			mv ${work_dir}/${d}/${d}_${split}/DELTA/extract_temp.tab ${work_dir}/${d}/${d}_${split}/DELTA/extract.tab
			continue;
		fi

		if [ ${i} -gt ${nb_processus} ]; then
			# waiting all processes to complete
			wait ${VN_NHADAT24H_pid_wait_arr[@]}	
			# initialize number of process background
			for Id_client in ${annonces_wait_arr[@]}
			do
				standardized_data ${work_dir}/${d}/${d}_${split}/ALL/annonce_${Id_client}.txt
			done 
			i=0; 
		fi

		if [ ! -e ${work_dir}/${d}/${d}_${split}/ALL/annonce_${id_client}.txt -o ! -s ${work_dir}/${d}/${d}_${split}/ALL/annonce_${id_client}.txt ]; then
			
			test ${lynx_ind} -eq 1 && incr_ip

			test ${lynx_ind} -eq 1 &&  phantomjs --proxy=172.16.1.11:3128 injectme.js ${src_link} ${work_dir}/${d}/${d}_${split}/ALL/annonce_${id_client}.txt &

			VN_NHADAT24H_pid_wait_arr[$i]=$!
			annonces_wait_arr[$i]=${id_client}

			let "i=i+1"  #increase number of process background
		fi
	done < ${work_dir}/${d}/${d}_${split}/DELTA/extract.tab

	#call funtion remove_incompleted_files_html in ../Lib_Offy/Utils.sh
	remove_incompleted_files_html ${work_dir}/${d}/${d}_${split}/ALL

	DATE=`date +%Y-%m-%d`

	while read -r line
	do
		FS='\t' read -r -a array <<< "$line"
		id_client=${array[0]}

		if [ ! -s ${work_dir}/${d}/${d}_${split}/UPD/annonce_"$id_client".upd -a -s ${work_dir}/${d}/${d}_${split}/ALL/annonce_"$id_client".txt ]; then 
			awk   -f ../Lib_Offy/Utils.awk -vid=${id_client} -vtable=${table} -vDATE=${DATE} -f "${work_dir}/all_html.awk" ${work_dir}/${d}/${d}_${split}/ALL/annonce_"$id_client".txt > ${work_dir}/${d}/${d}_${split}/UPD/annonce_"$id_client".upd ;
		fi

	done < ${work_dir}/${d}/${d}_${split}/DELTA/extract.tab
		
	# cree le fichier des upDATE du mode detail
	find ${work_dir}/${d}/${d}_${split}/UPD/ -type f -exec cat {} \; > ${work_dir}/${d}/${d}_${split}/DELTA/update.sql

	#clean data
	clean_sql_files

	# cree le fichier SQL des insert du mode liste
	
	awk -vDATE=${DATE} -vtable=${table}  -f ../Lib_Offy/Utils.awk -f "${work_dir}/liste_tab.awk" -f "${work_dir}/put_tab_into_db.awk" ${work_dir}/${d}/${d}_${split}/DELTA/extract.tab > ${work_dir}/${d}/${d}_${split}/DELTA/insert.sql

	# import into database 
	mysql -u root -p123456789 --default-character-set=utf8 REAL_ESTATE_VN < ${work_dir}/${d}/${d}_${split}/DELTA/insert.sql
	mysql -u root -p123456789 --default-character-set=utf8 REAL_ESTATE_VN < ${work_dir}/${d}/${d}_${split}/DELTA/update.sql

	# call procedure in database
	mysql -u root -p123456789 REAL_ESTATE_VN -e 'call Clean_All_Ads ("NHADAT24H");'
}

# Sortie finale
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

#
# MAIN
# programme principal commence ici
#
trap 'ExitProcess 1' SIGKILL SIGTERM SIGQUIT SIGINT

echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tDEBUT"

# liste des USER-AGENT disponibles
# USERAGENT_ARR[1]="Mozilla/5.0 ..."
#. /usr/local/bin/list_useragent.sh
u_a=0

# liste des IP disponibles
# IP_ARR[1]="94.23.190...
#. /usr/local/bin/list_ip.sh
ip=0

# usage / mode d'emploi du script
usage="download_site.sh\n\
\t-a no download - just process what's in the directory\n\
\t-d [date] (default today)\n\
\t-h help\n\
\t-r retrieve only, do not download the detailed adds\n\
\t-x debug mode - verbose ligne par ligne\n\
\t-y mode TEST telecharge 2 pages seulement \n\
\t-z nom du site - optionnel juste utile pour savoir ce qui tourne lorsqu'on fait \"ps\" \n\
"

lynx_ind=1
get_all_ind=1
TAB="	"
nb_retrieve_per_page=20
nb_processus=9
mode_test=0
from_day_to_day=0
set -x

while getopts :-ad:rhxf:yt:z name
do
  case $name in
    
    a)  lynx_ind=0
	let "shift=shift+1"
	;;

    d) 	d=$OPTARG
	let "shift=shift+1"
	;;

    h)  echo -e ${usage}
	ExitProcess 0
	;;

    r)  get_all_ind=0
	let "shift=shift+1"
	;;

    x)  set -x
	let "shift=shift+1"
	;;

    y) 	mode_test=1
	let "shift=shift+1"
	;;
	
    f) 	from_day_to_day=1 && f=$OPTARG 
	let "shift=shift+1"
	;;

    t) 	from_day_to_day=1 && t=$OPTARG 
	let "shift=shift+1"
	;;

    z)  let "shift=shift+1"
	;;

    --) break 
	;;

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
	d=`date +"%Y%m%d"`
fi

table="NHADAT24H"
work_dir=`pwd`
split=1;
date="${d:0:4}"-"${d:4:2}"-"${d:6:2}"

start="${f:0:4}"-"${f:4:2}"-"${f:6:2}"
end="${t:0:4}"-"${t:4:2}"-"${t:6:2}"

# remove all old files
rm -rf ${work_dir}/${d}/UPD/

# on cree le dossier avec la date 
mkdir -p ${work_dir}/${d}/ALL ${work_dir}/${d}/UPD ${work_dir}/${d}/DELTA
mkdir -p ${work_dir}/${d}/${d}_${split}
max_loop=5;
if [ ! -s ${work_dir}/${d}/${d}_${split}/page-1.html ]
then
	loop=0
	
	while [ ${loop} -lt ${max_loop} ]
	do
		test ${lynx_ind} -eq 1 && incr_ip
		test ${lynx_ind} -eq 1 && phantomjs --proxy=172.16.1.11:3128 injectme.js "https://nhadat24h.net/ban-bat-dong-san-tphcm-mua-ban-nha-dat-tphcm-s409644/" ${work_dir}/${d}/${d}_${split}/page-1.html 

		# on verifie que la page a ete telechargee jusqu'au bout (presence du </html>)
		# si ca n'est pas le cas , on efface 
		grep -i "<\/html>" ${work_dir}/${d}/${d}_${split}/page-1.html
		if [ $? -ne 0 ]; then
			rm -f ${work_dir}/${d}/${d}_${split}/page-1.html
			let "loop=loop+1"
		else
			# call function standardized_data in Lib_Offy/Utils.sh
			standardized_data ${work_dir}/${d}/${d}_${split}/page-1.html
			# la page est OK - on sort du loop
			loop=${max_loop}
		fi
	done
fi
# on trouve le nombre d'annonces selon le site
# nb_annonces.awk genere un fichier avec la variable nb_pages
awk -f ${work_dir}/nb_annonces.awk ${work_dir}/${d}/${d}_${split}/page-1.html > ${work_dir}/${d}/nb_annonces.$$
. ${work_dir}/${d}/nb_annonces.$$

let "nb_pages=nb_annonces / nb_retrieve_per_page"
let "mod=nb_annonces % nb_retrieve_per_page"
if [ $mod -gt 0 ]
then
	let "nb_pages=nb_pages + 1"
fi

echo "nb_pages = "$nb_pages
if [ ${mode_test} -eq 1 ]
then
	nb_pages=2
fi

let "page=nb_pages"
count=1;

while [ $page -gt 0 ]
do 
	mkdir -p ${work_dir}/${d}/${d}_${split}/ALL ${work_dir}/${d}/${d}_${split}/UPD ${work_dir}/${d}/${d}_${split}/DELTA

	download_listmode "https://nhadat24h.net/ban-bat-dong-san-tphcm-mua-ban-nha-dat-tphcm-s409644/" $page $split

	let "page=page - 1"
	let "count=count + 1"

	if [ $count -eq 200 ]
	then
		echo "split = "$split
		download_detailmode_parsing

		count=1;
		let "split=split + 1"
	fi
	
done

download_detailmode_parsing

echo "OK" > ${work_dir}/${d}/status	
echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tFIN"
ExitProcess 0
