BEGIN {
	col=1
	title[col]="PRICE"; col++
	title[col]="PRICE_UNIT"; col++
	title[col]="USED_SURFACE"; col++
	title[col]="USED_SURFACE_UNIT"; col++
	title[col]="SURFACE"; col++
	title[col]="SURFACE_UNIT"; col++
	title[col]="PRO_DIRECTION"; col++
	title[col]="PHOTOS"; col++
	title[col]="PRO_WIDTH"; col++
	title[col]="PRO_LENGTH"; col++
	title[col]="DETAILED_BRIEF"; col++	
	title[col]="LEGAL_STATUS"; col++
	title[col]="NB_FLOORS"; col++
	title[col]="ALLEY_ACCESS"; col++
	title[col]="FRONTAGE"; col++
	title[col]="SUPERMARKET"; col++
	title[col]="HOSPITAL"; col++
	title[col]="SCHOOL"; col++
	title[col]="PARK"; col++
	title[col]="PRICE_ORIGINAL"; col++
	title[col]="SURFACE_ORIGINAL"; col++
	title[col]="ADS_DATE_ORIGINAL"; col++
	title[col]="CREATED_DATE"; col++
	title[col]="PRO_FLAG"; col++
	max_col=col
	max_line = 50
	photo=0
	#Input
	val["CREATED_DATE"]=DATE
	val["PRO_FLAG"]=0
}



/class="p-price-n"/{
	split($0,p,"p-price-n\">")
	split(p[2],pp,"<span")
	pr = pp[1]
	val["PRICE_ORIGINAL"]=pr
	# if (match(pr,/[0-9]+/)){
	# 	# val["PRICE"]=pr
	# 	val["PRICE_ORIGINAL"]=pr
	# }
}


/class="img tRes_60"/{
	split($0,ar,"img src=")
	photo = length(ar) - 1
	val["PHOTOS"] = photo
}

/id="tab-overview"/{
	getline
	line = 0
	temp = ""
	while (match($0, "id=\"tab-utilities\"")==0 && match($0, "id=\"tab-detail\"")==0  && (line <= max_line)){
		line++
		getline
		if (match($0, "id=\"tab-utilities\"")!=0 || match($0,"id=\"tab-detail\"")!=0 ) {
			break
		}
		t=removeHtml(decodeHTML($0))
		temp=temp", "cleanSQL(t)
	}
	val["DETAILED_BRIEF"]=temp
}

/class="tab-title">THÔNG TIN CHI TIẾT<span/{
	lines = 0
	do {
		getline
		lines++
		if (match($0,"Giấy tờ </span>")){
			split($0,ar,"class=\"sp-info\">")
			split(ar[2],arr,"</span>")
			val["LEGAL_STATUS"]=cleanSQL(arr[1])
		}
		if (match($0,"Diện tích sử dụng </span>")){
			split($0,ar,"class=\"sp-info\">")
			split(ar[2],arr,"</span>")
			sf = arr[1]
			val["USED_SURFACE_ORIGINAL"]=sf
			# if (match(sf,"m")){
			# 	split(sf,sf1,"m")
			# 	val["USED_SURFACE"]=cleanSQL(sf1[1])
			# 	val["USED_SURFACE_UNIT"] = "m2"
			# }	
		}
		if (match($0,"Diện tích đất </span>")){
			split($0,ar,"class=\"sp-info\">")
			split(ar[2],arr,"</span>")
			sf = arr[1]
			val["SURFACE_ORIGINAL"]=sf
			# if (match(sf,"m")){
			# 	split(sf,sf1,"m")
			# 	val["SURFACE"]=cleanSQL(sf1[1])
			# 	val["SURFACE_UNIT"] = "m2"
			# }	
		}
		if (match($0,"Hướng </span>")){
			split($0,ar,"class=\"sp-info\">")
			split(ar[2],arr,"</span>")
			val["PRO_DIRECTION"]=cleanSQL(arr[1])
		}
		if (match($0,"Độ rộng hẻm </span>")){
			split($0,ar,"class=\"sp-info\">")
			split(ar[2],arr,"</span>")
			if (! match(arr[1],"--")){
				val["ALLEY_ACCESS"]=cleanSQL(arr[1])
			}
		}
		if (match($0,"Độ rộng mặt tiền đường </span>")){
			split($0,ar,"class=\"sp-info\">")
			split(ar[2],arr,"</span>")
			if (! match(arr[1],"--")){
				val["FRONTAGE"]=cleanSQL(arr[1])
			}
		}
		if (match($0,"Kết cấu nhà </span>")){
			split($0,ar,"class=\"sp-info\">")
			split(ar[2],arr,"</span>")
			if (! match(arr[1],"--")){
				val["NB_FLOORS"]=cleanSQL(arr[1])
			}
		}
		if (match($0,"Chiều dài </span>")){
			split($0,ar,"class=\"sp-info\">")
			split(ar[2],arr,"</span>")
			l = arr[1]
			if (match(l,"m")){
				split(l,l1,"m")
				val["PRO_LENGTH"]=cleanSQL(l1[1])
			}
		}
		if (match($0,"Chiều rộng </span>")){
			split($0,ar,"class=\"sp-info\">")
			split(ar[2],arr,"</span>")
			w = arr[1]
			if (match(w,"m")){
				split(w,w1,"m")
				val["PRO_WIDTH"]=cleanSQL(w1[1])
			}	
		}
		if(match($0, "siêu thị") || (match($0,"cửa hàng tiện lợi"))){
			val["SUPERMARKET"]=1
		}

		if(match($0, "trường")){
			val["SCHOOL"]=1
		} 

		if(match($0, "công viên")){
			val["PARK"]=1
		} 

		if(match($0, "bệnh viện")){
			val["HOSPITAL"]=1
		} 

	} 	while (!match($0, "id=\"tab-bankLoanBody\"") && !match($0, "id=\"tab-fluctuation\"") && (lines <= max_line))
}

END {
	if (id != "*"){
		printf "UPDATE IGNORE "table" SET "
		for (i=1; i< max_col;i++) {
			str=cleanSQL(val[title[i]]);	
			if (str != "") {
				printf ("%s=\"%s\", ", title[i], str);
				}
		}
		printf (" SITE=\"propzyvn\" WHERE SITE=\"propzyvn\" AND ID_CLIENT=\"%s\";\n", id)	
	}
}