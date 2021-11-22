#!/bin/bash


. ../Lib_Offy/list_useragent.sh 
. ../Lib_Offy/list_openvpn.sh 
. ../Lib_Offy/Utils.sh 

# faire tourner l'IP et le USER_AGENT
incr_ip() {
	a=`od -vAn -N4 -tu4 < /dev/urandom | sed 's/ //g'`
        let "u_a=a % max_useragent"
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
nb_retrieve_per_page=30
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

table="DIAOCONLINE"
work_dir=`pwd`
date="${d:0:4}"-"${d:4:2}"-"${d:6:2}"

start="${f:0:4}"-"${f:4:2}"-"${f:6:2}"
end="${t:0:4}"-"${t:4:2}"-"${t:6:2}"

# remove all old files
rm -rf ${work_dir}/${d}/UPD/

# on cree le dossier avec la date 
mkdir -p ${work_dir}/${d}/ALL ${work_dir}/${d}/UPD ${work_dir}/${d}/DELTA


# nb max de tentative pour telecharger une page
max_loop=5

# on telecharge la premiere page
page=1
loop=0
while [ ${loop} -lt ${max_loop} ]
do
	# on loop tant que la page n'est pas telecharge proprement
	if [ ! -s ${work_dir}/${d}/page-1.html ]
	then
		test ${lynx_ind} -eq 1 && incr_ip
		test ${lynx_ind} -eq 1 && wget -c -nv --timeout=150 --tries=5 --waitretry=1 -U"${USERAGENT_ARR[$u_a]}"  --referer="http://diaoconline.vn/sieu-thi" --random-wait --keep-session-cookies --save-cookies=${work_dir}/${d}/cookies.$$ --load-cookies=${work_dir}/${d}/cookies.$$ "http://diaoconline.vn/sieu-thi" -O ${work_dir}/${d}/page-1.html


	fi
		
	# on verifie que la page a ete telechargee jusqu'au bout (presence du </html>)
	# si ca n'est pas le cas , on efface 
	grep -i "<\/html>" ${work_dir}/${d}/page-1.html
	if [ $? -ne 0 ]; then
		rm -f ${work_dir}/${d}/page-1.html
		let "loop=loop+1"
	else
		# la page est OK - on sort du loop
		loop=${max_loop}
	fi
done

# on trouve le nombre d'annonces selon le site
# nb_annonces.awk genere un fichier avec la variable nb_pages
awk -f ${work_dir}/nb_annonces.awk ${work_dir}/${d}/page-1.html > nb_pages.$$
. nb_pages.$$

			
if [ ${mode_test} -eq 1 ]
then
	nb_pages=2
fi

page=2
while [ ${page} -le ${nb_pages} ]
do
	loop=0
	while [ ${loop} -lt ${max_loop} ]
	do
		if [ ! -s ${work_dir}/${d}/page-${page}.html ]
		then
			test ${lynx_ind} -eq 1 && incr_ip
			#test ${lynx_ind} -eq 1 && curl -x http://172.16.1.11:3128 -L "http://diaoconline.vn/sieu-thi/${page}" -A "${USERAGENT_ARR[$u_a]}" -H "Content-type: text/plain; charset=utf-8" --retry 2 --retry-max-time 60 --max-time 90 -o ${work_dir}/${d}/page-${page}.html
			test ${lynx_ind} -eq 1 && wget -c -nv --timeout=150 --tries=5 --waitretry=1 -U"${USERAGENT_ARR[$u_a]}"  --referer="http://diaoconline.vn/sieu-thi" --random-wait --keep-session-cookies --save-cookies=${work_dir}/${d}/cookies.$$ --load-cookies=${work_dir}/${d}/cookies.$$ "http://diaoconline.vn/sieu-thi/${page}" -O ${work_dir}/${d}/page-${page}.html
		
		fi
		# on verifie que la page a ete telechargee jusqu'au bout (presence du </html>)
		grep -i "</html>" ${work_dir}/${d}/page-${page}.html
		if [ $? -ne 0 ]; then
			rm -f ${work_dir}/${d}/page-${page}.html
			let "loop=loop+1"
		else
			loop=${max_loop}
		fi
	done
	
	# check from day to day: will be used when download new sites
	if [ ${from_day_to_day} -eq 1 ]
	then
		awk -vdate=${date} -vstart=${start} -vend=${end} -f ../Lib_Offy/Utils.awk -f check_stop.awk ${work_dir}/${d}/page-${page}.html > check_id.$$
		. check_id.$$

		if [ $check_id ]
		then 
			break;
		fi
		
	fi
	let "page=page+1"
done # fin sur page 


find ${work_dir}/${d}/ -name page-\*.html -exec awk -vdate=${date} -vstart=${start} -vend=${end} -f liste_tab.awk -f ../Lib_Offy/Utils.awk -f ${work_dir}/put_html_into_tab.awk {} \; > ${work_dir}/${d}/extract.$$

# on prepare le script de telechargement du mode detail
# cree un fichier extract des annonces avec ID unique
sort -u -k1,1 -t"${TAB}" ${work_dir}/${d}/extract.$$ > ${work_dir}/${d}/DELTA/extract.tab

if [ ${lynx_ind} -eq 1 -a ${get_all_ind} -eq 1 ] 
then
	# nb de processus a faire tourner en parrallele
	max_nb_processus=7
	nb_lignes_total=`wc -l ${work_dir}/${d}/DELTA/extract.tab | awk '{print $1}'`
	let "tranche=(nb_lignes_total / max_nb_processus) + 1"
		
	# loop sur le nb de processus
	# on lance les sous processus dans le background
	i=0
	while [ ${i} -lt ${max_nb_processus} ]
	do
		let "i=i+1"
		let "nb_head=${tranche}*i"
		# on prepare le script de telechargement
		head -${nb_head} ${work_dir}/${d}/DELTA/extract.tab | tail -n${tranche} | awk -vdir="${work_dir}/${d}/ALL" 'BEGIN{print "set -x"; FS="\t"} { print "if [ ! -s "dir"/annonce_"$1".txt ]; then incr_ip;  wget --bind-address=${IP_ARR[$ip]}  --timeout=12 --tries=7 --random-wait -c \""$2"\" -O "dir"/annonce_"$1".txt; fi"}END{print "set +x"}' > ${work_dir}/${d}/lynx_detail_annonce_${i}.$$

		# on lance le script de telechargement
		. ${work_dir}/${d}/lynx_detail_annonce_${i}.$$ > ${work_dir}/${d}/log_detail_${i}.$$ 2>&1 &		
	done
	# on attend la fin de tous les sous processu
	wait	
fi

# cree le fichier SQL des insert du mode liste
awk -vdate=${date} -vtable=${table}  -f ../Lib_Offy/Utils.awk -f "${work_dir}/liste_tab.awk" -f "${work_dir}/put_tab_into_db.awk" ${work_dir}/${d}/DELTA/extract.tab > ${work_dir}/${d}/DELTA/insert.sql

#call funtion remove_incompleted_files_html in ../Lib_Offy/Utils.sh
remove_incompleted_files_html ${work_dir}/${d}/ALL

while read id_client A1 A2 A3 A4 A5 A6 A7 A8 A9 A10
do
	if [ ! -s ${work_dir}/${d}/UPD/annonce_"$id_client".upd -a -s ${work_dir}/${d}/ALL/annonce_"$id_client".txt ]; then

		#python3 ../Lib_Offy/removeIcon.py ${work_dir}/${d}/ALL/annonce_"$id_client".txt ${work_dir}/${d}/ALL/annonce_"$id_client".html  

		awk   -f ../Lib_Offy/Utils.awk -vid=${id_client} -vtable=${table} -f "${work_dir}/all_html.awk" ${work_dir}/${d}/ALL/annonce_"$id_client".txt > ${work_dir}/${d}/UPD/annonce_"$id_client".upd ;
	fi
done < ${work_dir}/${d}/DELTA/extract.tab
	
# cree le fichier des update du mode detail
find ${work_dir}/${d}/UPD/ -type f -exec cat {} \; > ${work_dir}/${d}/DELTA/update.sql


# import into database 
mysql -u root -p123456789 REAL_ESTATE_VN < ${work_dir}/${d}/DELTA/insert.sql
mysql -u root -p123456789 REAL_ESTATE_VN < ${work_dir}/${d}/DELTA/update.sql

# call procedure in database
mysql -u root -p123456789 REAL_ESTATE_VN -e 'call Clean_All_Ads ("DIAOCONLINE");'

echo "OK" > ${work_dir}/${d}/status	
echo -e "`date +"%Y-%m-%d %H:%M:%S"`\tFIN"
ExitProcess 0
