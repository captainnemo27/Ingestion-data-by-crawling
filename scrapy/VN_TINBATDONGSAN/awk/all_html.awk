BEGIN {
    i=0
    #title[i]="ID_CLIENT"; i++
    title[i]="ADS_DATE"; i++;
    title[i]="ADS_DATE_ORIGINAL";		i++;
    title[i]="PRICE"; i++;
    title[i]="PRICE_UNIT"; i++;
    title[i]="PRICE_ORIGINAL";		i++;
    title[i]="SURFACE"; i++;
    title[i]="SURFACE_UNIT"; i++;
    title[i]="SURFACE_ORIGINAL";		i++;	
    title[i]="ALLEY_ACCESS"; i++
    title[i]="TOILET"; i++
    title[i]="NB_ROOMS"; i++
    title[i]="NB_FLOORS"; i++
    title[i]="PRO_DIRECTION"; i++
    title[i]="CREATED_DATE"; i++
    title[i]="FRONTAGE"; i++
    title[i]="PHOTOS"; i++
    title[i]="DEALER_NAME"; i++
    title[i]="DEALER_ADDRESS"; i++
    title[i]="DEALER_EMAIL"; i++
    title[i]="DEALER_TEL"; i++
    title[i]="LAND_TYPE"; i++
    title[i]="DETAILED_BRIEF"; i++
    title[i]="FULL_ADDRESS"; i++
    title[i]="DISTRICT"; i++
    title[i]="CITY"; i++
    title[i]="STREET"; i++

    val["PHOTOS"]=0
    val["FULL_ADDRESS"]=""
    max_i=i;
    ad_link=""
}

/class="pull-right"/{
    max_loop=10
    loop=0
    if (val["SURFACE_ORIGINAL"] == ""){
        getline;getline
        if ($0 ~ "Diện tích"){
            do {
                getline
                loop++
            } while($0 !~ /class="fsize-17 green-clr fweight-700"/ && loop < max_loop)
            getline;
            val["SURFACE_ORIGINAL"]=cleanSQL($0)
        }
    }
}

/rel="canonical"/{
    split($0, arr, "href=\"")
    split(arr[2], arr_1, "\"")
    ad_link = arr_1[1]

    #split(arr_1[1], arr_2, ".htm")
    #n = split(arr_2[1], ar_id, "-")
    #if(match(ar_id[n], /pr[0-9]+/) != 0){
        #val["ID_CLIENT"]= ar_id[n];
    #}
}
#<div class="pd-bottom-15 pd-top-15 clearfix">
#<div class="pull-left" style="width: 60%;">
#<span class="fsize-13">
#Giá
#</span>
#<br>
#<span class="fsize-17 green-clr fweight-700">
#                                2,650 Tỷ
/class="pd-bottom-15 pd-top-15 clearfix"/{
    getline; getline; getline; getline; getline;
    temp_price = cleanSQL($0)
    if ( temp_price == ""){
        getline; getline;
        temp_price = cleanSQL($0)
    }
    val["PRICE_ORIGINAL"]=temp_price
}
/class="list-info clearfix"/{
    two_previous_line=""
    previous_line=""
    current_line=$0
    max_loop=80
    loop=0

    while (current_line !~ /id="myGallery"/ && loop < max_loop) {

        if (current_line ~ /Mặt tiền/) {
            gsub("m", "", two_previous_line)
            val["FRONTAGE"]=two_previous_line
        } else if (current_line ~ /Đường vào/) {
            gsub("m", "", two_previous_line)
            val["ALLEY_ACCESS"]=two_previous_line
        } else if (current_line ~ /Số tầng/) {
            val["NB_FLOORS"]=two_previous_line
        } else if (current_line ~ /Số phòng/) {
            val["NB_ROOMS"]=two_previous_line
        } else if (current_line ~ /Số toilet/) {
            val["TOILET"]=two_previous_line
        } else if (current_line ~ /Hướng nhà/) {
            val["PRO_DIRECTION"]=two_previous_line
        } else if ( current_line ~ "value line") {
             if (val["ADS_DATE"] == "") {
                date_ads = cleanSQL($0)
                year_ads=""
                if (date_ads != ""){
                    if (date_ads ~ " " && date_ads ~ /[0-9]{4}/) {
                        val["ADS_DATE"] = date_ads
                        sub(" ","/",val["ADS_DATE"])
                    }
                    else {
                        getline;getline;
                        val["ADS_DATE"] = date_ads 
                        year_ads = cleanSQL($0)
                        if (year_ads != ""){
                            val["ADS_DATE"] = val["ADS_DATE"] "/" year_ads 
                            }
                        }
                }
                val["ADS_DATE_ORIGINAL"] = date_ads " " year_ads
            }

        }

        two_previous_line=previous_line
        previous_line=current_line
        current_line=$0
        getline
        loop++
    }

    if (current_line ~ /id="myGallery"/) {
        while (match($0, "id=\"imgPrint\"") == 0 && loop < max_loop) {
            if(match($0, "<img src=") != 0) {
                photo_count++;
            }
            getline;
            loop++
        }	
        val["PHOTOS"]=photo_count;
    }
}


/id="infoDetail"/ {
	str="";
    loop=0
    max_loop=100
	while (match($0, "</div>") == 0 && loop<max_loop) {
		getline;
        loop++
		temp = trim(removeHtml(decodeHTML($0)));
		str=str"- "temp;
	}
	sub("-", "", str);
	val["DETAILED_BRIEF"]=str;
}


/id="myGallery"/ {
    loop=0;
    max_loop=50
    while (match($0, "id=\"imgPrint\"") == 0 && loop< max_loop) {
        if(match($0, "<img src=") != 0) {
            photo_count++;
        }
        getline;
        loop++
    }	
    val["PHOTOS"]=photo_count;
}

/class="fweight-bold dblue-clr"/{
	getline;
	val["DEALER_NAME"]=$0
}

/id="toPhone"/ {
	getline;
	val["DEALER_TEL"]=$0
}

/id="toEmail"/ {
	getline;
    temp_email=cleanSQL($0)
    if (temp_email != "--") {
        val["DEALER_EMAIL"]=temp_email
    }
}

/id="toAddress"/ {
	getline;
    temp_address=cleanSQL($0)
    if (temp_address != "--") {
        val["DEALER_ADDRESS"]=temp_address
    }
}

/class='green-clr'/{
    temp_place=cleanSQL($0)
    loop=0
    max_loop=5
    if (temp_place !~ "-") {
        do {
            getline; 
            if (cleanSQL($0) != "" ){
                temp_place=temp_place " " cleanSQL($0)
            }
            loop++
        }while (loop<max_loop && $0 !~ /<\/div>/) 

    }
    nb=split(temp_place, arr, "-")
    if (nb >= 2) {
        gsub(/[B|b]án/, "", arr[1])
        gsub(/Cho thuê/, "", arr[1])
        val["LAND_TYPE"] = arr[1]
        val["FULL_ADDRESS"]=arr[2]
        for(el=3;el<=nb;el++) {
            val["FULL_ADDRESS"]=val["FULL_ADDRESS"]" - "arr[el]
        }
    }
}


END {
    upd=""
     #check data parsing empty
	checkParsingEmpty(val)
	for(i=0;i<max_i;i++) {
		if (val[title[i]]!="") {
			upd=upd""sprintf(" %s=\"%s\",", title[i], cleanSQL(val[title[i]]))
		}
	}
	if (upd!="" && id_client != "")
		printf ("update ignore %s set %s CREATED_DATE=\"%s\", PRO_FLAG=0, site=\"tinbatdongsan\" where ID_CLIENT=\"%s\";\n", table, upd, created_date, id_client)
}
