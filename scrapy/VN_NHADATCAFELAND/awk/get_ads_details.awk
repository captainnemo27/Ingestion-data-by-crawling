BEGIN {
   	col=1
	title[col]="LAND_TYPE"; col++
	title[col]="PRO_WIDTH"; col++
	title[col]="PRO_LENGTH"; col++
	title[col]="DETAILED_BRIEF"; col++
	title[col]="PRO_DIRECTION"; col++
	title[col]="LEGAL_STATUS"; col++
	title[col]="DEALER_NAME"; col++
	title[col]="MINI_SITE"; col++
	title[col]="DEALER_ADDRESS"; col++
	title[col]="DEALER_TEL"; col++
	title[col]="DEALER_EMAIL"; col++
	title[col]="ADS_DATE"; col++
	title[col]="PROJECT_NAME"; col++	
	title[col]="PRICE"; col++
	title[col]="PRICE_UNIT"; col++
	title[col]="SURFACE"; col++
	title[col]="SURFACE_UNIT"; col++
	title[col]="NB_FLOORS"; col++
	title[col]="BEDROOM"; col++
	title[col]="TOILET"; col++
	title[col]="USED_SURFACE"; col++
	title[col]="USED_SURFACE_UNIT"; col++
	title[col]="ALLEY_ACCESS"; col++
	title[col]="GARAGE"; col++
	title[col]="FOR_SALE"; col++
	title[col]="FOR_LEASE"; col++
	title[col]="TO_BUY"; col++
	title[col]="TO_LEASE"; col++
	title[col]="CITY"; col++
	title[col]="DISTRICT"; col++
	title[col]="WARD"; col++
	title[col]="STREET"; col++
	title[col]="FULL_ADDRESS"; col++
	title[col]="LAT"; col++
	title[col]="LON"; col++
	title[col]="PRICE_ORIGINAL"; col++
	title[col]="SURFACE_ORIGINAL"; col++
	title[col]="USED_SURFACE_ORIGINAL"; col++
	title[col]="ADS_DATE_ORIGINAL"; col++
	title[col]="CREATED_DATE"; col++
	title[col]="PRO_FLAG"; col++

	max_col=col
	#Input
	val["CREATED_DATE"]=DATE
	val["PRO_FLAG"]=0
}

/<dt>Vị trí:<\/dt>/{
	getline;
	val["FULL_ADDRESS"]=cleanSQL($0);
}
# # "addressRegion":"TP. Hồ Chí Minh",
# /"addressRegion"/{
#     split($0, city, ":")
#     split(city[2], city, ",")
# 	gsub("\"","",city[1])
# 	val["CITY"] = city[1]
# }
# # "addressLocality":"Tân Định, Quận 1",
# /"addressLocality"/{
#     split($0, wardDis, ":")
#     split(wardDis[2], wardDis, ",")
# 	gsub("\"","",wardDis[2])
# 	val["DISTRICT"] = cleanSQL(wardDis[2])
# 	gsub("\"","",wardDis[1])
# 	val["WARD"] = cleanSQL(wardDis[1])
# }
# # "streetAddress":"Nguyễn Phi Khanh, Tân Định, Quận 1, TP. Hồ Chí Minh",
# /"streetAddress"/{
#     split($0, street, ":")
#     split(street[2], street, ",")
#     if ( street[4] != "" ){
# 		gsub("\"","",street[1])
#         val["STREET"] = cleanSQL(street[1])
#     }
# }

/"latitude"/{
    split($0,ar, "latitude\":\"")
	split(ar[2],arr, "\"")
    val["LAT"] = arr[1]
}

/"longitude"/{
	split($0,ar, "longitude\":\"")
	split(ar[2],arr, "\"")
	val["LON"] = arr[1]
}

/Giá: <b>/{
	split($0,ar,"Giá: <b>")
	total_price = cleanSQL(removeHtml(ar[2]))
	val["PRICE_ORIGINAL"] = total_price
	# if (match(ar[2],/[0-9]+/)){
	# 	total_price = cleanSQL(removeHtml(ar[2]))
	# 	val["PRICE"] = total_price
	# }
}

/<dt>Diện tích:<\/dt>/{
	getline;
	# <dd>100m<sup>2</sup>
	gsub("<sup>","",$0)
    area = cleanSQL(removeHtml($0))
	val["SURFACE_ORIGINAL"]=area
	# if (area ~ /[0-9]/){
	# 	gsub(" ", "", area)
	# 	split(area, areaUnit, "m2")
	# 	val["SURFACE"] = areaUnit[1]
	# 	val["SURFACE_UNIT"] = "m2"	
	# }
}
# DETAIL_BRIEF
/<section id="description"/{
	val["DETAILED_BRIEF"] = ""
	getline
	do {
		getline
		if ( cleanSQL($0) != "" ){
            if ( val["DETAILED_BRIEF"] != "" ) {
                val["DETAILED_BRIEF"] = val["DETAILED_BRIEF"] " " cleanSQL($0)
            } else {
                val["DETAILED_BRIEF"] = cleanSQL($0)
            }
		}
	} while (match($0, "</section>") == 0);
}

# Dealer name
/<dt>Liên hệ:<\/dt>/{
    getline;getline;
	val["DEALER_NAME"] = cleanSQL($0)
	split($0,arr,"href=\"")
	split(arr[2],arrr,"\"")
	val["MINI_SITE"]=arrr[1]
}
# Dealer address
/<b>Địa chỉ:<\/b>/{
    split(cleanSQL($0), dealerAddress, ":")
    val["DEALER_ADDRESS"] = cleanSQL(dealerAddress[2])
}
# Telephone
# $('#detailTelSpan').text('0902349593');
/<b>Mobile:<\/b>/{
	getline; getline; getline
	split($0,ar,"this,")
	split(ar[2],arr,")\"")
	gsub("'","",arr[1])
	val["DEALER_TEL"]=cleanSQL(arr[1])
}
# Email
# <b>Email:</b>
# <a href="mailto:anhmd@batdongsan3c.com"
# title="anhmd@batdongsan3c.com"> anhmd@batdongsan3c.com</a>
/<b>Email:<\/b>/{
    getline
    split($0, email, "mailto:")
    split(email[2], email, "\"")
	val["DEALER_EMAIL"] = cleanSQL(email[1])
}

/<dt>Pháp lý:<\/dt>/{
	getline
	val["LEGAL_STATUS"]=cleanSQL($0)
}

/<dt>Thuộc:<\/dt>/{
	getline
	val["PROJECT_NAME"]=cleanSQL($0)
}

#ads date
# <dt>Ngày đăng:</dt>
# <dd>16-07-2019</dd>
/<dt>Ngày đăng:<\/dt>/{
    getline
	val["ADS_DATE_ORIGINAL"] = cleanSQL($0)
    split(cleanSQL($0),adsDate,"-")
	val["ADS_DATE"] = adsDate[3]"-"adsDate[2]"-"adsDate[1]
}

# # Land type, width, length, direction, legal
/section id="property-features"/{
	do{
		getline

		if ($0 ~ "Chổ đậu xe hơi"){
			val["GARAGE"] = 1
		}else if ($0 ~ "Đường trước nhà"){
			split(cleanSQL($0), alleyaccess, ":")
			val["ALLEY_ACCESS"] = cleanSQL(alleyaccess[2]);
		}else if ($0 ~ "Số phòng ngủ"){
			split(cleanSQL($0), nbroom, ":")
			val["BEDROOM"] = cleanSQL(nbroom[2]);
		}else if ($0 ~ "Số lầu"){
			split(cleanSQL($0), nbfloors, ":")
            val["NB_FLOORS"] = cleanSQL(nbfloors[2]);
		}else if ($0 ~ "Số phòng vệ sinh"){
            split(cleanSQL($0), nbwc, ":")
            val["TOILET"] = cleanSQL(nbwc[2]);
        }else if ($0 ~ "Hướng xây dựng"){
			split(cleanSQL($0), direction, ":")
			val["PRO_DIRECTION"] = cleanSQL(direction[2]);
		}
		else if ($0 ~ "Diện tích sử dụng"){
			split(cleanSQL($0), ar, ":")
			val["USED_SURFACE_ORIGINAL"] = ar[2]
			# if (ar[2] ~ /[0-9]/){
			# 	gsub(" ", "", ar[2])
			# 	val["USED_SURFACE_UNIT"]="m2"
			# 	split(ar[2], arr, val["USED_SURFACE_UNIT"])
			# 	val["USED_SURFACE"] = cleanSQL(arr[1]);
			# }
		}
		else if ($0 ~ "Loại địa ốc"){
			split(cleanSQL($0),landType, ":")
			val["LAND_TYPE"] = cleanSQL(landType[2])
		}else if ($0 ~ "Chiều ngang"){
			split(cleanSQL($0), width, "Chiều ngang:")
			gsub(/[^0-9]/,"",width[2])
			val["PRO_WIDTH"] = cleanSQL(width[2])
		}else if ($0 ~ "Chiều dài"){
			split(cleanSQL($0), proLength, "Chiều dài:")
			gsub(/[^0-9]/,"",proLength[2])
			val["PRO_LENGTH"] = proLength[2]
		}
	}while ( match($0, "</div>" ) == 0 )
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
		printf (" SITE=\"nhadatcafeland\" WHERE SITE=\"nhadatcafeland\" AND ID_CLIENT=\"%s\";\n", id)
	}
}