BEGIN {
   	i=1
	title[i]="ADS_DATE"; i++;
    title[i]="ADS_DATE_ORIGINAL";		i++;
	title[i]="ADS_TITLE"; i++;
	title[i]="PHOTOS"; i++;
	title[i]="PRICE"; i++;
	title[i]="PRICE_UNIT"; i++;
    title[i]="PRICE_ORIGINAL";		i++;	
	title[i]="SURFACE"; i++;
	title[i]="SURFACE_UNIT"; i++;
    title[i]="SURFACE_ORIGINAL";		i++;
	title[i]="FULL_ADDRESS"; i++;
    title[i]="CITY"; i++
	title[i]="LEGAL_STATUS"; i++;
	title[i]="PRO_DIRECTION"; i++;
	title[i]="DEALER_NAME"; i++;
	title[i]="DEALER_ID"; i++;
	title[i]="DEALER_TEL"; i++;
	title[i]="DEALER_EMAIL"; i++;
	title[i]="MINI_SITE"; i++;
	title[i]="DETAILED_BRIEF"; i++;
    title[i]="BEDROOM"; i++
    title[i]="FRONTAGE"; i++
    title[i]="LAT"; i++
    title[i]="LON"; i++
    title[i]="LAND_TYPE"; i++;
    title[i]="PROJECT_NAME"; i++;

    max_i=i

    val["PHOTOS"]=0;
}

/var number_images/ {
	split($0, ar, "'");
	split(ar[2], ar2, "'")
    gsub(/[^0-9]/, "", arr[1])
	val["PHOTOS"] = cleanSQL(ar2[1])
}

/var ad_id/ {
    if (id_client == "") {
        split($0, ar, "'");
        split(ar[2], ar2, "'")
        id_client=ar2[1]
    }
}

#var ad_title = 'Chỉ Với 400 triệu  30GTCH  sở hữu ngay Căn Hộ Cao Cấp Phú Mỹ An Tower ngay TTTP Huế';
/var ad_title/ {
	split($0, ar, "'");
	split(ar[2], ar2, "'")
	val["ADS_TITLE"]=ar2[1]
}

/class="li_100 icon_bds font_14 roboto_regular cl_666"|class="li_100 clear icon_bds font_14 roboto_regular"/ {
    if (val["PRICE_ORIGINAL"] == ""){
        getline; 
        if ($0 ~ "Giá") {
            getline;
            temp2=cleanSQL($0);
            if (temp2 == ""){
                getline;
                temp2=cleanSQL($0);
            }
            if (temp2 ~ "Giá"){
                sub("Giá :", "", temp2);
            }
            temp_price = trim(temp2);
            val["PRICE_ORIGINAL"] = temp_price
        }
    }
}

#"latitude": 21.0009359,
/"latitude"/ {
    split(cleanSQL($0), arr, ":")
    gsub(",", "", arr[2])
    val["LAT"] = cleanSQL(arr[2])
}

/"longitude"/ {
    split(cleanSQL($0), arr, ":")
    gsub(",", "", arr[2])
    val["LON"] = cleanSQL(arr[2])
}
/class="note info_item_popup/{
    if (val["ADS_DATE"] == ""){
        getline; getline
        if ($0 ~ "Thời gian") {
            getline; getline
            if (cleanSQL($0) == ""){
               getline;
            }
            val["ADS_DATE_ORIGINAL"] = cleanSQL($0)
            split(cleanSQL($0), arr, "/")
            if ( arr[3] ~ /[0-9]/ ){
                if (arr[1] != "" && arr[2] != "" && arr[3] != "")
                    val["ADS_DATE"]  = arr[3]"-"arr[2]"-"arr[1]
            }
        }
    }
}

/class="li_50 icon_bds icon_dientich/ {
    if (val["SURFACE_ORIGINAL"] == ""){
        loop=0
        max_loop=5
        getline; getline;
        do {
            getline;
            loop++
            if (cleanSQL($0) != "")
                val["SURFACE_ORIGINAL"] = val["SURFACE_ORIGINAL"]""cleanSQL($0)
        } while (loop< max_loop && $0 !~ /<\/sup>/)
    }

}
/class="li_50 icon_bds font_14 roboto_regular"/{
    getline;
    if (cleanSQL($0) ~ "Mặt tiền" ){
        temp = cleanSQL($0)
        split(temp, arr, ":")
        val["FRONTAGE"] = arr[2]
    }
    if (cleanSQL($0) ~ "pháp lý" ){
        temp = cleanSQL($0)
        split(temp, arr, ":")
        val["LEGAL_STATUS"] = arr[2]
    }
    if (cleanSQL($0) ~ "Hướng" ){
        temp = cleanSQL($0)
        split(temp, arr, ":")
        val["PRO_DIRECTION"] = arr[2]
    }
    if (cleanSQL($0) ~ "phòng ngủ" ){
        temp = cleanSQL($0)
        gsub(/[^0-9]/, "", temp)
        val["BEDROOM"] = temp
    }
    if (cleanSQL($0) ~ "Dự án" ){
        getline; getline
        val["PROJECT_NAME"] = cleanSQL($0)
    }
}

# FULL_ADDRESS
/var contentString/ {
	split($0, ar, "\"");
	split(ar[2], ar2, "\"")
	gsub("Khác ,", "", ar2[1]);
	gsub("Khác,", "", ar2[1]);
	val["FULL_ADDRESS"]=ar2[1];
}

/var city_name/ {
	split($0, ar, "'");
	split(ar[2], ar2, "'")
	val["CITY"]=ar2[1]
}

# DEALER_NAME, DEALER_ID
#var ad_userid 	= '1696312';
#    var ad_useremail 	= 'beautysunhb@gmail.com';
#    var ad_user_mobile 	    = '0913332139';
/var ad_username/ {
	split($0, ar, "'");
	split(ar[2], ar2, "'")
	val["DEALER_NAME"]=ar2[1]
}

# EMAIL
/var ad_useremail/ {
	split($0, ar, "'");
	split(ar[2], ar2, "'")
	val["DEALER_EMAIL"]=ar2[1];
}
# TELEPHONE
/var ad_user_mobile/ {
	split($0, ar, "'");
	split(ar[2], ar2, "'")
	val["DEALER_TEL"]=ar2[1];
}

/var ad_userid/ {
	split($0, ar, "'");
	split(ar[2], ar2, "'")
	val["DEALER_ID"]=ar2[1];
}

/div class="info_text"/ {
# DETAILED_BRIEF
	str=""
	do {
		getline;
		temp=cleanSQL($0);
		if(length(temp) > 0) {
			str=str" "temp;
		}
	}while(match($0, "</div>") ==0);
	val["DETAILED_BRIEF"]=str;
}

# MINI_SITE
# <a href='https://rongbay.com/member-1701353.html' rel="nofollow"  class="name_store icon_bds" title="Xem trang cá nhân của thành viên này">Lê Đông</a>
/name_store/ {
	split($0, ar, "href='");
	split(ar[2], ar2, "'");
	val["MINI_SITE"]=ar2[1];
}

/var ad_tt/ {
    split($0, arr, "'")
    split(arr[2], arr_1, "'")
    val["LAND_TYPE"] = arr_1[1]
}

END {
	printf "update IGNORE "table" set "
	for (i=1; i<= max_i;i++) {
		str=cleanSQL(val[title[i]]);
	        if (str != "") {
	            printf ("%s=\"%s\", ", title[i], str);
	        }
	}
	printf (" site=\"rongbay\", PRO_FLAG=\"0\", CREATED_DATE=\"%s\" where site=\"rongbay\" and ID_CLIENT=\"%s\";\n", created_date, id_client)
}
