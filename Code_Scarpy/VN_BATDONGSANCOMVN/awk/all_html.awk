BEGIN {
    i=0
    title[i]="LAND_TYPE"; i++
    title[i]="CITY"; i++
    title[i]="DISTRICT"; i++
    title[i]="PRO_DIRECTION"; i++
    title[i]="LEGAL_STATUS"; i++
    title[i]="SURFACE"; i++
    title[i]="SURFACE_UNIT"; i++
    title[i]="SURFACE_ORIGINAL";		i++;
    title[i]="ADS_DATE"; i++
    title[i]="ADS_DATE_ORIGINAL";		i++;
    title[i]="PRICE"; i++
    title[i]="PRICE_UNIT"; i++
    title[i]="PRICE_ORIGINAL";		i++;
    title[i]="NB_FLOORS"; i++
    title[i]="TOILET"; i++
    title[i]="FRONTAGE"; i++
    title[i]="FULL_ADDRESS"; i++
    title[i]="ALLEY_ACCESS"; i++;
    title[i]="BEDROOM"; i++;
    title[i]="LAT"; i++
    title[i]="LON"; i++

    title[i]="DETAILED_BRIEF"; i++
    title[i]="DEALER_EMAIL"; i++
    title[i]="DEALER_NAME"; i++;
	title[i]="DEALER_TEL"; i++;
    title[i]="MINI_SITE"; i++
    title[i]="LAT"; i++
    title[i]="LON"; i++

    max_i=i;
}
/Thông tin mô tả/{
    if (val["DETAILED_BRIEF"] ==""){
    max_loop=40
    loop=0
    content=""
    do {
        getline
        temp = cleanSQL($0)
        if ( temp != "") {
            content = content " " temp
        }
        loop++
    } while(loop < max_loop && $0 !~ /<\/div>/)

    val["DETAILED_BRIEF"] = content
    }
}

/area: '/{
    if (val["SURFACE_ORIGINAL"] == ""){
        split(cleanSQL($0),arr,"area: '")
        split(arr[2],arr,"'")
        val["SURFACE_ORIGINAL"] = arr[1]    
    }
}
#      <div class="scroll-info">
#<label>Giá thỏa thuận</label>
/class="scroll-info"/{
        getline;
    if (val["PRICE_ORIGINAL"] == "")
        val["PRICE_ORIGINAL"] = cleanSQL($0)
}
/class="name"/{
    if (val["DEALER_NAME"] == ""){
        split($0,arr,"title=\"")
        split(arr[2],arr,"\"")
        val["DEALER_NAME"] = arr[1]
    }
}
# <a href="/ban-dat-ha-noi" level="2" title="Bán đất tại Hà Nội">Hà Nội</a>
/level="2"/{
    val["CITY"] = cleanSQL($0)
}
# <a href="/ban-dat-quoc-oai" level="3" title="Bán đất tại Huyện Quốc Oai">Quốc Oai</a>
/level="3"/{
    val["DISTRICT"] = cleanSQL($0)
}
/contactMobile: '/{
    if (val["DEALER_TEL"] == ""){
        split(cleanSQL($0),arr,"contactMobile: '")
        split(arr[2],arr,"'")
        val["DEALER_TEL"] = arr[1]
    }
}
/updatedTime:/{
    if (val["ADS_DATE_ORIGINAL"] == ""){
        split(cleanSQL($0),arr,"updatedTime: '")
        split(arr[2],arr,"'")
        val["ADS_DATE_ORIGINAL"]=arr[1]
        if (arr[1] ~ /[0-9]/) {
            val["ADS_DATE"] = arr[1]
        }
    }
}
/class="product-save|id="iconSave"/{
    max_loop=40
    loop=0
    do {
        if ($0 ~ /data-area/) {
           split($0, arr, "data-area=\"")
           split(arr[2], ar_1, "\"")
            val["SURFACE_ORIGINAL"] = ar_1[1]
        }
        if ($0 ~ /data-updatedtime/) {
           split($0, arr, "data-updatedtime=\"")
           split(arr[2], ar_1, "\"")
            if (ar_1[1] != "") {
                val["ADS_DATE"] = val["ADS_DATE_ORIGINAL"] = ar_1[1]
            }
        }
        if ($0 ~ /data-contactname/) {
           split($0, arr, "data-contactname=\"")
           split(arr[2], ar_1, "\"")
            if (ar_1[1] != "") {
                val["DEALER_NAME"] = ar_1[1]
        
            }
        }
           if ($0 ~ /data-contactmobile/) {
           split($0, arr, "data-contactmobile=\"")
           split(arr[2], ar_1, "\"")
            if (ar_1[1] != "") {
                val["DEALER_TEL"] = ar_1[1]
        
            }
        }
        if ($0 ~ /data-toilets/) {
           split($0, arr, "data-toilets=\"")
           split(arr[2], ar_1, "\"")
            gsub(/[^0-9]/, "", ar_1[1])
            if (ar_1[1] != "") {
                val["TOILET"] = ar_1[1]
            
            }
        }
        if ($0 ~ /data-price/) {

            split($0, arr, "data-price=\"")
            split(arr[2], ar_1, "\"")
            temp_price = cleanSQL(ar_1[1])
            val["PRICE_ORIGINAL"]= temp_price
        }
        getline
        loop++
    } while(loop < max_loop && $0 !~ /<div/)
}
/Đặc điểm bất động sản/ {
    max_loop=200
    loop=0
    getline;
    if ($0 ~ /span|class/){
        do {
            if ($0 ~ /Loại tin đăng/) {
                getline; 
                if (cleanSQL($0) == ""){getline; getline}
                val["LAND_TYPE"] = cleanSQL($0)
                gsub(/Cho thuê|Bán|Mua/,"",val["LAND_TYPE"])

            } else if ($0 ~ /Hướng nhà/) {
                getline; 
                if (cleanSQL($0) == ""){getline; getline}
                val["PRO_DIRECTION"] = cleanSQL($0)

            } else if ($0 ~ /Pháp lý/) {
                getline; 
                if (cleanSQL($0) == ""){getline; getline}
                val["LEGAL_STATUS"] = cleanSQL($0)

            } else if ($0 ~ /Số tầng/) {
                getline; 
                if (cleanSQL($0) == ""){getline; getline}
                temp = cleanSQL($0)
                gsub(/[^0-9]/, "", temp)
                val["NB_FLOORS"] = temp

            } else if ($0 ~ /Địa chỉ/) {
                getline; 
                if (cleanSQL($0) == ""){getline; getline}
                val["FULL_ADDRESS"] = cleanSQL($0)

            } else if ($0 ~ /Số phòng ngủ/) {
                getline; 
                if (cleanSQL($0) == ""){getline; getline}
                temp = cleanSQL($0)
                gsub(/[^0-9]/, "", temp)
                val["BEDROOM"] = temp

            } else if ($0 ~ /Mặt tiền/) {
                getline; 
                if (cleanSQL($0) == ""){getline; getline}
                temp = cleanSQL($0)
                val["FRONTAGE"] = temp

            } else if ($0 ~ /Đường vào/) {
                getline; 
                if (cleanSQL($0) == ""){getline; getline}
                temp = cleanSQL($0)
                val["ALLEY_ACCESS"] = temp
            }

            getline
            loop++
        } while(loop < max_loop && $0 !~ /class="title-detail"/)
    }
}

/id="email"/ {
    split($0, arr, "data-email=\"")
    split(arr[2], ar_1, "\"")
    val["DEALER_EMAIL"] = cleanSQL(ar_1[1])
}

/class="info"/ {
    getline
    split($0, arr, "href=\"")
    split(arr[2], ar_1, "\"")
    if (ar_1[1] != "")
        val["MINI_SITE"] = "https://batdongsan.com.vn"cleanSQL(ar_1[1])
}

/class="map"/ {
    getline
    split($0, arr, "src=\"")
    split(arr[2], ar_1, "\"")
    split(ar_1[1], ar_2, "?q=")
    split(ar_2[2], ar_3, "&amp;")
    split(ar_3[1], lat_lon, ",")
    if (lat_lon[1] != "" && lat_lon[2] != "") {
        val["LAT"] = lat_lon[1]
        val["LON"] = lat_lon[2]
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
    if (upd!="" && id_client!="")
        printf ("update ignore %s set %s CREATED_DATE=\"%s\", PRO_FLAG=0, site=\"batdongsan.com.vn\" where ID_CLIENT=\"%s\";\n", table, upd, created_date, id_client)
}
