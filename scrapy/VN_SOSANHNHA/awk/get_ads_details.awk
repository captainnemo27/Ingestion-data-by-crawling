BEGIN {
   	col=1
	title[col]="LEGAL_STATUS"; col++
	title[col]="NB_FLOORS"; col++
	title[col]="BEDROOM"; col++
	title[col]="TOILET"; col++
	title[col]="FRONTAGE"; col++
	title[col]="DETAILED_BRIEF"; col++
	title[col]="PHOTOS"; col++
	title[col]="PROJECT_NAME"; col++
	title[col]="BANK"; col++
	title[col]="PARK"; col++
	title[col]="SCHOOL"; col++
	title[col]="SUPERMARKET"; col++

	title[col]="SURFACE"; col++
	title[col]="SURFACE_UNIT"; col++
	title[col]="PRICE"; col++
	title[col]="PRICE_UNIT"; col++

	title[col]="LAND_TYPE"; col++
	title[col]="ADS_DATE"; col++
	title[col]="DEALER_NAME"; col++
	title[col]="DEALER_TEL"; col++
	title[col]="DEALER_EMAIL"; col++
    title[col]="FULL_ADDRESS"; col++

	title[col]="CREATED_DATE"; col++
	title[col]="PRO_FLAG"; col++
	
	title[col]="PRICE_ORIGINAL"; col++
	title[col]="SURFACE_ORIGINAL"; col++
	title[col]="ADS_DATE_ORIGINAL"; col++

	max_col=col
	photo=0
	flag=0

	#Input
	val["CREATED_DATE"]=DATE
	val["PRO_FLAG"]=0
}

/<b>Loại tin rao:/{
	flag=1
	getline
	val["LAND_TYPE"]=cleanSQL($0)
}

/<\/section>/{
	getline
	split($0,ar,":\"")
	split(ar[2],ar2,"\",\"")
	split(ar[3],ar3,"\",\"")
	split(ar[4],ar4,"\",\"")
	price = cleanSQL(decode_hex(ar2[1]))
	surface = cleanSQL(decode_hex(ar3[1]))
	telephone = cleanSQL(decode_hex(ar4[1]))
	val["PRICE_ORIGINAL"] = price
	# if (match(price,/[0-9]+/)){
	# 	# val["PRICE"] = price
	# 	val["PRICE_ORIGINAL"] = price
	# }
	val["SURFACE_ORIGINAL"] = surface
	# if (match(surface,/[0-9]+/)){
	# 	val["SURFACE_ORIGINAL"] = surface
	# 	# split(surface,arr,"m")
	# 	# val["SURFACE"]= arr[1]
	# 	# val["SURFACE_UNIT"]=  "m2"
	# }
	if (match(telephone,/[0-9]+/)!=0){
		split(telephone,arr,"}")
		val["DEALER_TEL"]= arr[1]
	}
}

/<div>Pháp lý:/{
	temp = removeHtml($0)
	split(temp,ar,"Pháp lý:")
	val["LEGAL_STATUS"]=cleanSQL(ar[2])
}

/<b>Ngày đăng:/{
	getline
	val["ADS_DATE"]=cleanSQL($0)
	val["ADS_DATE_ORIGINAL"]=cleanSQL($0)
}

/class="avatar_name"/{
	getline
	val["DEALER_NAME"]=cleanSQL($0)
}

/class="mail_detail"/{
	getline; getline; getline
	if (match(cleanSQL($0),"@")){
		val["DEALER_EMAIL"]=cleanSQL($0)
	}
}

/class="dt_lab">Địa chỉ: <\/span>/{
	split($0,ar,"<span>")
	val["FULL_ADDRESS"]=cleanSQL(ar[2])
}

/<div>Số tầng:/{
	temp = removeHtml($0)
	split(temp,ar,"Số tầng:")
	gsub(/[^0-9]/,"",ar[2])
	val["NB_FLOORS"]=cleanSQL(ar[2])
}

/<div>Phòng ngủ :/{
	temp = removeHtml($0)
	split(temp,ar,":")
	val["BEDROOM"]=cleanSQL(ar[2])
}

/div>Nhà vệ sinh :/{
	temp = removeHtml($0)
	split(temp,ar,":")
	val["TOILET"]=cleanSQL(ar[2])
}

/<div>Mặt tiền:/{
	temp = removeHtml($0)
	split(temp,ar,":")
	val["FRONTAGE"]=cleanSQL(ar[2])
}

/<h4>Khu vực:/{
	temp = ""
	loop=0;
	max_loop=300;
	do {
		getline
		loop++
		if (match($0,"Thông tin tóm tắt: <a")==0){
			temp = temp " " $0
		}
	} while (match($0,"Thông tin tóm tắt: <a")==0 && loop < max_loop)
	t = removeHtml(temp)
	val["DETAILED_BRIEF"]=cleanSQL(t)
}

/item item-for/{
	photo++
}

/>Dự án:/{
	if ((match($0,"<br> Thông tin chi tiết"))==0){
		getline
		temp = removeHtml($0)
		val["PROJECT_NAME"]=cleanSQL(temp)
	} else {
		split($0,ar,"<br> Thông tin chi tiết:")
		split(ar[1],arr,"Dự án:")
		temp = removeHtml(arr[2])
		val["PROJECT_NAME"]=cleanSQL(temp)
		p = removeHtml(ar[2])
		loop=0;
		max_loop=300;
		do {
			getline
			loop++
			if (match($0,"<div>")==0){
				p = p " " $0
			}
		} while (match($0,"<div>")==0 && loop < max_loop)
		t = removeHtml(p)
		val["DETAILED_BRIEF"]=cleanSQL(t)
	}
	
}

/<div>Tiện ích:/{
	temp = removeHtml($0)
	if (match(temp,"Ngân Hàng")){
		val["BANK"]=1
	}
	if (match(temp,"Công Viên")){
		val["PARK"]=1
	}
	if (match(temp,"Trường Học")){
		val["SCHOOL"]=1
	}
	if (match(temp,"Siêu Thị")){
		val["SUPERMARKET"]=1
	}
}

END {
    nb=split(FILENAME, ar, "-");
    split(ar[nb], arr, ".html");
    id=arr[1];
	if (flag==1 && id != "*"){
		val["PHOTOS"] = photo 
		printf "UPDATE IGNORE "table" SET "
		for (i=1; i< max_col;i++) {
			str=cleanSQL(val[title[i]]);	
			if (str != "") {
				printf ("%s=\"%s\", ", title[i], str);
				}
		}
		printf (" SITE=\"sosanhnha\" WHERE SITE=\"sosanhnha\" AND ID_CLIENT=\"%s\";\n", id)	
	}
}