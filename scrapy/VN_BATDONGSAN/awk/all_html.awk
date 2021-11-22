BEGIN {
    i=0
    title[i]="ID_CLIENT"; i++

    title[i]="ALLEY_ACCESS"; i++
    title[i]="BATHROOM"; i++
    title[i]="BEDROOM"; i++
    title[i]="CREATED_DATE"; i++
    title[i]="DEALER_ADDRESS"; i++
    title[i]="DEALER_EMAIL"; i++
    title[i]="DEALER_ID"; i++
    title[i]="DEALER_TEL"; i++
    title[i]="DETAILED_BRIEF"; i++
    title[i]="FRONTAGE"; i++
    title[i]="FULL_ADDRESS"; i++
    title[i]="LAND_TYPE"; i++
    title[i]="LEGAL_STATUS"; i++
    title[i]="NB_FLOORS"; i++
    title[i]="PHOTOS"; i++
    title[i]="PRO_DIRECTION"; i++
    title[i]="PRO_UTILITIES"; i++
    title[i]="STREET"; i++
    title[i]="ADS_DATE"; i++;
    title[i]="ADS_DATE_ORIGINAL"; i++;
    title[i]="SURFACE"; i++
    title[i]="SURFACE_UNIT"; i++;
    title[i]="SURFACE_ORIGINAL"; i++;
    title[i]="PRICE_ORIGINAL"; i++;
    val["PHOTOS"]=0

    max_i=i;
    ad_link=""
    max_loop=100
}
/Mã tin:/{
    getline; getline; getline
    val["ID_CLIENT"]=trim(decodeHTML(removeHtml($0)))
}

/canonical/{
    split($0,ar_1,"href=")
    gsub(/"/,"",ar_1[2])
    gsub("/>","",ar_1[2])
    ad_link=trim(ar_1[2])
}

/<div class="email">/{
    getline
    getline
    val["DEALER_EMAIL"]=trim(decodeHTML(removeHtml($0)))
}

/<div class="phone">/{
    getline
    getline
    getline
    getline
    getline
    val["DEALER_TEL"]=trim(decodeHTML(removeHtml($0)))
}

/<div class="Addrees">/{
    getline
    temp=trim(decodeHTML(removeHtml($0)))
    if (length(temp) != 0){
      val["DEALER_ADDRESS"]=temp
    }
}

/Loại:/{
    if (val["LAND_TYPE"] == ""){
        for (j=1; j<=5; ++j) {
            getline
        }
        val["LAND_TYPE"]=trim(decodeHTML(removeHtml($0)))
    }
}

/Địa chỉ:/{
    if (val["FULL_ADDRESS"] == ""){
        getline; getline; getline
        temp = cleanSQL($0)
        if (length(temp) < 250)
            val["FULL_ADDRESS"] = temp
    }
}

/Đường\/phố/{
    getline; getline; getline; getline; getline
    val["STREET"] = cleanSQL($0)
}

/Mặt tiền \(m\)/{
    getline
    getline
    getline
    val["FRONTAGE"]=trim(decodeHTML(removeHtml($0)))
    gsub(",",".",val["FRONTAGE"])
}
/Diện tích:/{
    getline
    getline
    getline
    if ($0 ~ "product-area"){
        getline
        temp=trim(decodeHTML(removeHtml($0)));
        val["SURFACE_ORIGINAL"]=temp
    }
}
/Đường vào \(m\)/{
    if (val["ALLEY_ACCESS"] == ""){
        getline
        getline
        getline
        val["ALLEY_ACCESS"]=trim(decodeHTML(removeHtml($0)))
        gsub(",",".",val["ALLEY_ACCESS"])
    }
}

/class='huongnha/{
    if (val["PRO_DIRECTION"] == ""){
        getline
        getline
        getline
        getline
        getline
        pro_direction = cleanSQL($0)
        if ( pro_direction !~ "http") {
            val["PRO_DIRECTION"] = pro_direction
        }  
    }
}

/Ngày đăng tin:/ {
    if (val["ADS_DATE"] == ""){
    getline; getline; getline
    ads_date = cleanSQL($0)
    val["ADS_DATE_ORIGINAL"] = ads_date
    split(ads_date, arr, "/")
    if (arr[3] != "" && arr[2] != "" && arr[1] != "")
        val["ADS_DATE"] = arr[3]"-"arr[2]"-"arr[1]
    }
}

/class='phaply/{
    if (val["LEGAL_STATUS"] == ""){
        getline
        getline
        getline
        getline
        getline
        legal_status=cleanSQL($0)
        if( legal_status !~ "http") {
            val["LEGAL_STATUS"]=legal_status
        }
    }
}

/class='sotang/{
    if (val["NB_FLOORS"] == ""){
        getline
        getline
        getline
        getline
        getline
        val["NB_FLOORS"]=trim(decodeHTML(removeHtml($0)))
        gsub(",",".",val["NB_FLOORS"])
    }
}

/class='sophongngu/{
     if (val["BEDROOM"] == ""){
        getline
        getline
        getline
        getline
        getline
        val["BEDROOM"]=trim(decodeHTML(removeHtml($0)))
     }
}

/class='sophongtam/{
    if (val["BATHROOM"] == ""){
        getline
        getline
        getline
        getline
        getline
        val["BATHROOM"]=trim(decodeHTML(removeHtml($0)))
    }
}

/class="changemedia"/ {
  val["PHOTOS"]++
}

/class='tienichkemtheo/ {
  getline; getline; getline
  loop = 0
  utilities=""
  while($0 !~ /<\/li>/ && loop<max_loop){
      temp=cleanSQL($0)
      if (temp != "" ){
        utilities = utilities "  " temp
      }
    getline
    loop++
  }
  val["PRO_UTILITIES"] = utilities
}

/class="PD_Gioithieu/{
    temp = ""
    loop = 0
    while ($0 !~ "product-tag" && loop<max_loop){
        getline
        line=trim(decodeHTML(removeHtml($0)))
        if (line != "")
        {
            if (temp == ""){
                temp = line
            }
            else{
                temp=temp", "line
            }
        }
        loop++
    }
    val["DETAILED_BRIEF"]=temp
}
/class="button-price"/{
    getline;
    getline;
    val["PRICE_ORIGINAL"] = cleanSQL($0)
}
END {
    upd=""
    #check data parsing empty
	checkParsingEmpty(val)
	for(i=1;i<max_i;i++) {
		if (val[title[i]]!="") {
			upd=upd""sprintf(" %s=\"%s\",", title[i], cleanSQL(val[title[i]]))
		}
	}
	if (upd!="" && val["ID_CLIENT"]!="")
		printf ("update ignore %s set %s PRO_FLAG=0, CREATED_DATE=\"%s\", site=\"batdongsan\" where ID_CLIENT=\"%s\";\n", table, upd, created_day, cleanSQL(val["ID_CLIENT"]))
}
