BEGIN {
    i=0
    title[i]="PRICE"; i++;
    title[i]="PRICE_UNIT"; i++;
    title[i]="CITY"; i++;
    title[i]="DISTRICT"; i++;
    title[i]="PRICE_ORIGINAL";		i++;	
    title[i]="USED_SURFACE"; i++;
    title[i]="USED_SURFACE_UNIT"; i++;
    title[i]="USED_SURFACE_ORIGINAL";		i++;	
    title[i]="ALLEY_ACCESS"; i++
    title[i]="TOILET"; i++
    title[i]="NB_ROOMS"; i++
    title[i]="NB_FLOORS"; i++
    title[i]="PRO_DIRECTION"; i++
    title[i]="FRONTAGE"; i++
    title[i]="PRO_WIDTH"; i++
    title[i]="PRO_LENGTH"; i++
    title[i]="DEALER_NAME"; i++
    title[i]="DEALER_ADDRESS"; i++
    title[i]="DEALER_EMAIL"; i++
    title[i]="DEALER_TEL"; i++
    title[i]="LAND_TYPE"; i++
    title[i]="DETAILED_BRIEF"; i++
    title[i]="BEDROOM"; i++;
    title[i]="BATHROOM"; i++;
    title[i]="LEGAL_STATUS"; i++
    title[i]="FULL_ADDRESS"; i++
    count=0
    max_i=i;
}

/class="location"/ {
    getline; getline
    val["FULL_ADDRESS"] = cleanSQL($0)
}

/div itemscope itemtype="/{
    count++
    if (count == 3 ){
        getline;getline;getline;
        val["CITY"] = cleanSQL($0)
    }
    if (count == 4 ){
        getline;getline;getline;
        val["DISTRICT"] = cleanSQL($0)
    }
}
/Diện tích khuôn viên:/{
    loop=0
    max_loop=20
    getline;
    if ($0 ~ /<\/strong>/){
        if (val["PRO_WIDTH"] == ""){
            do{
                getline;
                loop++
                if ($0 ~ "ngang trước"){
                    getline;getline;
                    temp=cleanSQL($0)
                    if (temp != ""){
                        gsub("m", "", temp)
                        val["PRO_WIDTH"] = temp
                    }
                }
                if ($0 ~ "Chiều dài"){
                    getline;getline;
                    temp=cleanSQL($0)
                    if (temp != ""){
                        gsub("m", "", temp)
                        val["PRO_LENGTH"] = temp
                    }
                }
            }while(loop<max_loop && $0 !~ "bg_grey")
        }
    }
}
/Tổng diện tích sử dụng:/{
    if (val["USED_SURFACE_ORIGINAL"] == ""){
        getline; getline; getline
        val["USED_SURFACE_ORIGINAL"]=cleanSQL($0)
    }
}

# DETAILED_BRIEF
/MÔ TẢ CHI TIẾT/ {
	str="";	
    loop=0;
    max_loop=100
    for (i=0; i < 6; ++i) {getline}
	do{
		getline;
        loop++;
		temp = cleanSQL($0);
    		if(length(temp)>0){
			str=str "  " temp;
		}
	}while(match($0,"<div class=")==0 && loop<max_loop);
	val["DETAILED_BRIEF"]=str;
}

#LEGAL_STATUS
/Tình trạng pháp lý:/{
    if  (val["LEGAL_STATUS"] == ""){
        getline; getline; getline
        val["LEGAL_STATUS"]=cleanSQL($0)
    }
}
/class="money"/{
    getline;
    temp_price=cleanSQL($0);
    gsub("Giá:","",temp_price)
    val["PRICE_ORIGINAL"] = temp_price 
}
# LAND_TYPE 
/Loại địa ốc:/{
    if  (val["LAND_TYPE"] == ""){
        getline; getline; getline
	    val["LAND_TYPE"] = cleanSQL($0)
    }
}

# DIRECTION
/Hướng:/{
    getline; getline; getline
	val["PRO_DIRECTION"] = cleanSQL($0)
}

/Đường trước nhà:/{
    getline; getline;
    temp = cleanSQL($0)
    gsub("m", "", temp)
    val["ALLEY_ACCESS"] = temp
}

/Số lầu:/{
    getline; getline;
    val["NB_FLOORS"] = cleanSQL($0)
}

/Số phòng khách:/{
    getline; getline;
    val["NB_ROOMS"] = cleanSQL($0)
}

/Số phòng ngủ:/{
    getline; getline;
    val["BEDROOM"] = cleanSQL($0)
}

/Số phòng tắm:/{
    getline; getline;
    val["BATHROOM"] = cleanSQL($0)
    val["TOILET"]   = val["BATHROOM"]
}

/THÔNG TIN LIÊN HỆ/{
    for(i = 0; i< 5; ++i) {getline;}
    val["DEALER_NAME"] = cleanSQL($0)
}

/Địa chỉ:/{
    for(i = 0; i< 3; ++i) {getline;}
    val["DEALER_ADDRESS"] = cleanSQL($0)
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
		printf ("update ignore %s set %s CREATED_DATE=\"%s\", PRO_FLAG=0, site=\"diaoconline\" where ID_CLIENT=\"%s\";\n", table, upd, created_date, id_client)
}
