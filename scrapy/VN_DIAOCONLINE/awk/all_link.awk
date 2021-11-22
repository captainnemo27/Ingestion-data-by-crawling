BEGIN {
    i=0
    MAX_LOOP=800
}

/id="showCityProductBoxCount"/{
    i++
    if (i == 1) {
        loop=0
        while ($0 !~ /id="showBoxhot"/ && loop < MAX_LOOP) {
            if ($0 ~ /href/) {
                split($0, arr, "href=\"/")
                split(arr[2], ar_1, "\"")

                printf("%s\n", ar_1[1])
            }
            getline; loop++;
        }
    }
}

#END {
    #upd=""
	#for(i=0;i<max_i;i++) {
		#if (val[title[i]]!="") {
			##upd=upd""sprintf(" %s=\"%s\",", title[i],trim(cleanSQL(decodeHTML(val[title[i]]))))
			#upd=upd""sprintf(" %s=\"%s\",", title[i], cleanSQL(val[title[i]]))
		#}
	#}
	#if (upd!="" && ad_link!="")
		#printf ("update ignore %s set %s site=\"tinbatdongsan\" where ADS_LINK=\"%s\" and CREATED_DATE=\"%s\";\n", table, upd, ad_link, val["CREATED_DATE"])
#}
