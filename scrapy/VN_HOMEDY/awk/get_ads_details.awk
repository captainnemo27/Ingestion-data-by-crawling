BEGIN {
   	col=1
	title[col]="ADS_TITLE"; col++
	title[col]="CITY"; col++
	title[col]="DISTRICT"; col++
	title[col]="FULL_ADDRESS"; col++
	title[col]="LAND_TYPE"; col++
	title[col]="SURFACE"; col++
	title[col]="SURFACE_UNIT"; col++
	title[col]="SURFACE_ORIGINAL"; col++
	title[col]="PRICE"; col++
	title[col]="PRICE_UNIT"; col++
	title[col]="PRICE_ORIGINAL"; col++
	title[col]="PRO_DIRECTION"; col++
	title[col]="LEGAL_STATUS"; col++
	title[col]="ADS_DATE"; col++
	title[col]="ADS_DATE_ORIGINAL"; col++
	title[col]="NB_FLOORS"; col++
	title[col]="BEDROOM"; col++
	title[col]="BATHROOM"; col++
	title[col]="FRONTAGE"; col++
	title[col]="ALLEY_ACCESS"; col++
	title[col]="LAT"; col++
	title[col]="LON"; col++
	title[col]="DETAILED_BRIEF"; col++
	title[col]="PHOTOS"; col++
	title[col]="PROJECT_NAME"; col++
	title[col]="DEALER_ID"; col++
	title[col]="DEALER_NAME"; col++
	title[col]="DEALER_TEL"; col++
	title[col]="MINI_SITE"; col++
	title[col]="CREATED_DATE"; col++
	title[col]="PRO_FLAG"; col++
	
	max_col=col
	count_lon=0
	count_lat=0
	photo=0
	count=0
	#Input
	val["CREATED_DATE"]=DATE
	val["PRO_FLAG"]=0

}

/class="col-sm-8"/{
	getline
	t=decode_hex(decodeHTML(removeHtml($0)))
	val["ADS_TITLE"]=cleanSQL(t)
}
/itemprop="position" content="3"/{
	getline; getline; getline; getline
	val["CITY"] = cleanSQL($0)
}
/itemprop="position" content="4"/{
	getline; getline; getline; getline
	val["DISTRICT"] = cleanSQL($0)
}

/div class="address"/{
	count++
	if (val["LAND_TYPE"] == ""){
		getline;
		split($0,ar,"title=\"")
		split(ar[2],arr,"\">")
		s=cleanSQL(removeHtml(arr[1]))
		split(s,ss,"tại")
		gsub("Cho thuê","",ss[1])
		gsub("Bán","",ss[1])
		if (cleanSQL(ss[1]) != "Nhà đất"){
			val["LAND_TYPE"] = cleanSQL(ss[1])
		}
	}
	if (count == 1){
		while (match($0,"<span>")==0){
			getline
		}
		split($0,ar,"</a> -")
		adr=decode_hex(cleanSQL(ar[2]))
    	val["FULL_ADDRESS"]=decode_hex(adr)
	}
}

/class="product-info"/{
	getline;getline; getline
	t=cleanSQL(decodeHTML($0))
	temp = decode_hex(t)
	val["ADS_DATE_ORIGINAL"] = temp
	number=temp
	gsub(/[^0-9]/,"",number)
	number=int(number)
	if(match(temp, "phút trước")){
		temp=strftime("%Y-%m-%d", systime() - number*60)	
	} else if(match(temp, "giờ trước")){
		temp=strftime("%Y-%m-%d", systime() - number*3600)
	} else if(match(temp, "ngày trước")){
		temp=strftime("%Y-%m-%d", systime() - number*86400)
	} else if(match(temp, "tuần trước")){
		temp=strftime("%Y-%m-%d", systime() - 7*number*86400)
	} else if(match(temp, "tháng trước")){
		temp=strftime("%Y-%m-%d", systime() - 30*number*86400)
	} else if(match(temp, "năm trước")){
		temp=strftime("%Y-%m-%d", systime() - 365*number*86400)
	}
	if (temp!=""){
		val["ADS_DATE"]=temp
	}
}

/class="description readmore"/{
    temp = ""
    loop = 0
	max_loop = 100
    while ($0 !~ "button-in-content" && loop<max_loop){
        getline
        line=decode_hex(cleanSQL($0))
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
	


/Giá: <\/div>/{
	getline; getline
	pr=decode_hex(removeHtml($0))
	val["PRICE_ORIGINAL"] = cleanSQL(pr)
	getline;
	if (cleanSQL($0) != "")
		val["PRICE_ORIGINAL"] = val["PRICE_ORIGINAL"] " " decode_hex(cleanSQL($0))
	
}

/>Diện tích: <\/div>/{
	getline; getline
	sf=decode_hex(removeHtml($0))
	val["SURFACE_ORIGINAL"] = cleanSQL(sf)
	getline
	if (cleanSQL($0) != "")
		val["SURFACE_ORIGINAL"] = val["SURFACE_ORIGINAL"] " " decode_hex(cleanSQL($0))
}

/class="bed-room"/{
	t=removeHtml($0)
	val["BEDROOM"] = cleanSQL(t)
}

/class="bath-room"/{
	t=removeHtml($0)
	val["BATHROOM"] = cleanSQL(t)
}
#  PageData.ProductId = 1223862;
/PageData.ProductId/{
	split($0,arr,"PageData.ProductId =")
	split(arr[2],arr,";")
	gsub(" ","",arr[1])
	val["ID_CLIENT"]=arr[1];

}	

/var _entityId/{
	if (val["ID_CLIENT"] ==""){
		split($0,arr,"_entityId = '")
		split(arr[2],arr,"'")
		val["ID_CLIENT"]=arr[1];
	}
}

/PageData.BasicProperty/{
	getline
	split($0,ar,"}")
	for (i=0;i<length(ar)-1;i++){
		t = ar[i]
		if (t ~ "Tình trạng pháp lý"){
			split(t,a,"Value:")
			gsub("'","",a[2])
			val["LEGAL_STATUS"]=cleanSQL(a[2])
		} else if (t ~ "Đường vào"){
			split(t,a,"Value:")
			gsub("'","",a[2])
			val["ALLEY_ACCESS"]=cleanSQL(a[2])
		} else if (t ~ "Mặt tiền"){
			split(t,a,"Value:")
			gsub("'","",a[2])
			val["FRONTAGE"]=cleanSQL(a[2])
		} else if (t ~ "Hướng nhà"){
			split(t,a,"Value:")
			gsub("'","",a[2])
			val["PRO_DIRECTION"]=cleanSQL(a[2])
		} else if (t ~ "Số tầng"){
			split(t,a,"Value:")
			gsub("'","",a[2])
			val["NB_FLOORS"]=cleanSQL(a[2])
		}
	}
}

/class="text-name"/{
	split($0,ar,"href=\"")
	split(ar[2],arr,"class=")
	val["MINI_SITE"]="https://homedy.com/"arr[1]

	split(arr[1],arrr,"-ag")
	val["DEALER_ID"]=arrr[2]
	
	getline
	t=decodeHTML(removeHtml($0))
	val["DEALER_NAME"]=cleanSQL(decode_hex(t))
}

/pc-mobile-number/{
	split($0,ar,"data-mobile=")
	split(ar[2],arr,">")
	gsub("\"","",arr[1])
	val["DEALER_TEL"]=cleanSQL(decode_hex(arr[1]))
}

/var _longtitude/{
	count_lon++
	if (count_lon==1){
		split($0,ar,"(")
		split(ar[2],arr,")")
		val["LON"]=arr[1]
	}
}

/var _latitude/{
	count_lat++
	if (count_lat==1){
		split($0,ar,"(")
		split(ar[2],arr,")")
		val["LAT"]=arr[1]
	}
}

/class="project-detail-text"/{
	getline; getline; getline
	t=decodeHTML(removeHtml($0))
	val["PROJECT_NAME"]=cleanSQL(t)
}

/class="o-item image-default"/{
	do {
		getline
		if (match($0,"class=\"owl-lazy\"")){
			if (match($0,"thumb-default.jpg")==0){
				photo++
			}
		}
	} while (match($0,"class=\"product-item\"")==0)
	val["PHOTOS"]=photo
}

END {
    upd=""
	for(i=1;i<max_col;i++) {
		if (val[title[i]]!="") {
			upd=upd""sprintf(" %s=\"%s\",", title[i], cleanSQL(val[title[i]]))
		}
	}
	if (upd!="" && val["ID_CLIENT"]!="")
		printf ("update ignore %s set %s PRO_FLAG=0, site=\"homedy\" where ID_CLIENT=\"%s\";\n", table, upd, cleanSQL(val["ID_CLIENT"]))
}


