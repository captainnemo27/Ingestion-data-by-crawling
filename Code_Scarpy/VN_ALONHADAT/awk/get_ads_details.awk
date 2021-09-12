BEGIN {
   	col=1
	title[col]="ADS_TITLE"; col++
	title[col]="LAND_TYPE"; col++
	title[col]="PRO_WIDTH"; col++
	title[col]="PRO_LENGTH"; col++
	title[col]="DETAILED_BRIEF"; col++	
	title[col]="PRO_DIRECTION"; col++
	title[col]="LEGAL_STATUS"; col++
	title[col]="DEALER_ID"; col++
	title[col]="MINI_SITE"; col++
	title[col]="ADS_DATE"; col++	
	title[col]="PHOTOS"; col++
	title[col]="FULL_ADDRESS"; col++
	title[col]="PRICE"; col++
	title[col]="PRICE_UNIT"; col++
	title[col]="SURFACE"; col++
	title[col]="SURFACE_UNIT"; col++
	title[col]="NB_ROOMS"; col++
	title[col]="NB_FLOORS"; col++
	title[col]="KITCHEN"; col++
	title[col]="BEDROOM"; col++
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
	title[col]="LON"; col++
	title[col]="LAT"; col++
	title[col]="PRICE_ORIGINAL"; col++
	title[col]="SURFACE_ORIGINAL"; col++
	title[col]="USED_SURFACE_ORIGINAL"; col++
	title[col]="ADS_DATE_ORIGINAL"; col++
	title[col]="CREATED_DATE"; col++
	title[col]="PRO_FLAG"; col++

	max_col=col
	photo=0

	#Input
	val["CREATED_DATE"]=DATE
	val["PRO_FLAG"]=0
	val["DATE_ORIGINAL"]=strftime("%Y-%m-%d", systime())
}

# ADS_TITLE
# <div class='title'><h1>Cần vốn mở Spa sang gấp 360m2(12x30) đất thổ cư 100%, SHR, giá 4tr8/m2. Nhàn</h1><span class='date'>Ngày đăng: Hôm nay</span></div>
/<h1>/{
	split($0, ar, "</h1>");
	val["ADS_TITLE"]=cleanSQL(ar[1]);
}

# ADS_DATE
#<span class='date'>Ngày đăng: Hôm nay</span>
/<span class='date'>/{
	split($0, ar, "<span class='date'>");
	split(ar[2],arr, "<");
	gsub("Ngày đăng:", "", arr[1]);
	temp=arr[1]
	val["ADS_DATE_ORIGINAL"]=temp;
	if(match(temp, "Hôm nay")> 0){
		temp=strftime("%Y-%m-%d", systime())	
	} else if(match(temp, "Hôm qua")> 0){
		temp=strftime("%Y-%m-%d", systime() - 86400)
	} else {
		n=split(temp, ar, "/");
		temp=trim(ar[n])"-"trim(ar[n-1])"-"trim(ar[n-2])
	}
	val["ADS_DATE"]=temp
}

# DETAIL_BRIEF
# <div class='detail '><p>
# <span style="color:#000000;"><span style="font-family: Helvetica, Arial, sans-serif; font-size: 16px;">
#Gia đ&igrave;nh t&ocirc;i cần tiền kinh doanh Spa n&ecirc;n b&aacute;n gấp l&ocirc; đất 360m2 ( 4tr8/m2). 
#T&ocirc;i t&aacute;ch l&agrave;m 2 sổ. Mỗi sổ 180m2 = 6m x 30m gi&aacute; 880tr. Ai mua cả 360m2 t&ocirc;i b&aacute;n gi&aacute; 1ty750 th&ocirc;i. 
#Bởi v&igrave; b&aacute;n gấp n&ecirc;n t&ocirc;i chỉ thương lượng ch&uacute;t &iacute;t lấy lộc.</span></span>

# <div class='detail text-content'>GIÁ SỐC MÙA DỊCH  chỉ còn 6.5 triệu, Căn 1 ngủ +1 khách liền bếp – ( Vào ở được ngay) 
# • Bạn đi công tác , du lịch , học tập .
# • Bạn muốn sống tự lập , Mới cưới , Sống thử . Tự khẳng định mình.
# • Bạn cần chỗ ở trong lúc chờ nhận nhà , sửa nhà !
# • Bạn đang tìm chỗ ở yên tĩnh , thoáng mát nghỉ ngơi sau một ngày làm việc , học tập vất vả !

#<div class='detail text-content'>Cần thuê khách sạn và nhà nguyên căn có nhiều phòng để kinh doanh lĩnh vực cho thuê phòng ngắn hạn, dài hạn và hình thành thương hiệu hệ thống phòng cho thuê lớn trong khu vực, cần thuê gấp số lượng lớn khách sạn, căn hộ, nhà nghĩ, phòng cho thuê, phòng trọ từ nhỏ đến lớn thuộc khu vực Tp.HCM. Quý chủ nhà nào cần cho thuê hoặc sang nhượng lại hợp đồng thuê nhà có nhiều phòng vui lòng liên hệ 0909026586</div>

# /<div class='detail >/{
/class='detail/{
	if (match($0, "text-content")!=0){
		original=$0
		#case one line
		if(match($0, "<div class='moreinfor'>")!=0){
			split(original, ar, "text-content'>");
			split(ar[2], arr, "</div><div class='moreinfor'>");
			temp=arr[1]
		}
		#case many lines
		else{
			# print($0)
			# getline
			# print($0)
			split(original, ar, "text-content'>");
			temp=ar[2]
			getline
			while (match($0, "<div class='moreinfor'>")==0 && (match($0, "</div>")==0))
			{
				if (match($0, "<img src=")!=0){
					photo++;
				}

				t=removeHtml($0)
				if ( length(trim(t)) != 0 ){
				temp=temp" "trim(t)
				}
				getline
			};

			split($0, arr, "</div><div class='moreinfor'>");
			temp=temp" "trim(arr[1])

			val["PHOTOS"]=photo
		}
	}
	else {
		split($0, ar, "text-content'>");
		temp=ar[2]

		do {
			getline

			if (match($0, "<img src=")!=0){
				photo++;
			}

			if (match($0, "<div class='moreinfor'>")!=0 || (match($0, "</p>")!=0)){
				break
			}

			t=removeHtml($0)
			if ( length(trim(t)) != 0 ){
			temp=temp" "trim(t)
			}
		} while (match($0, "<div class='moreinfor'>")==0 || (match($0, "</p>")==0));

		val["PHOTOS"]=photo
	}

	val["DETAILED_BRIEF"]=decodeHTML(removeHtml(temp))
}

# PRICE
# <span class='price'><span class='label'>Giá: </span> <span class='value'> 880 triệu </span></span>
# <span class='price'><span class='label'>Giá: </span> <span class='value'> 30 triệu /&nbsp;m<sup>2</sup>&nbsp;&nbsp;</span></span>
# <span class='price'><span class='label'>Giá: </span> <span class='value'> 100 triệu /&nbsp;tháng</span></span>
/class='label'>Giá:/{
	split($0,ar, "class='value'>");
	split(ar[2], arr, "</");
	gsub("<sup>", "", arr[1]);
	s=decodeHTML(arr[1])
	val["PRICE_ORIGINAL"]=s;
	# if (s ~ /[0-9]/){
	# 	val["PRICE_ORIGINAL"]=s;
	# 	# split(s, ar_1, " ");
	# 	# f="";
	# 	# for (x = 2; x <= length(ar_1); x++){
	# 	# 	f=f""ar_1[x]
	# 	# }
	# 	# sub(",",".",ar_1[1])
	# 	# val["PRICE"]=ar_1[1];
	# 	# val["PRICE_UNIT"]=cleanSQL(f);
	# }
}

# SURFACE
# <span class='square'><span class='label'>Diện tích: </span> <span class='value'> 360 m<sup>2</sup></span></span>
/class='label'>Diện tích:/{
	split($0,ar, "Diện tích: </span> <span class='value'>");
	split(ar[2], arr, "</sup>");
	gsub("<sup>", "", arr[1]);
	temp=cleanSQL(arr[1])
	val["SURFACE_ORIGINAL"]=temp;
	# split(temp, ar_1, " ");
	# val["SURFACE"]=ar_1[1];
	# val["SURFACE_UNIT"]=ar_1[2]
}


# FULL_ADDRESS
# <div class='address'><span class='label'>Địa chỉ tài sản:</span><span class='value'> Đường Đại Lộ Bình Dương, Phường Định Hòa, Thành phố Thủ Dầu Một, Bình Dương</span></div>
/class='label'>Địa chỉ tài sản/{
	getline
	split($0, ar, "class='value'>");
	split(ar[2], arr, "<");
	val["FULL_ADDRESS"]=cleanSQL(arr[1]);

	# temp=val["FULL_ADDRESS"];
	# n=split(temp, arrr, ",");
	# val["CITY"]=cleanSQL(arrr[n])
	# val["DISTRICT"]=cleanSQL(arrr[n-1]);
	# val["WARD"]=cleanSQL(arrr[n-2]);
	# val["STREET"]=cleanSQL(arrr[n-3]);
}


# PRO_DIRECTION
#<td>Hướng</td><td>_</td>
/<td>Hướng/{
	getline
	split($0, ar, "<td>");
	split(ar[2], arr, "<");
	if (match(arr[1],"_")==0){
		val["PRO_DIRECTION"]=cleanSQL(arr[1]);
	}
}


# ALLEY_ACCESS
#<td>Đường trước nhà</td><td>16m</td>
/<td>Đường trước nhà/{
	getline
	split($0, ar, "<td>");
	split(ar[2], arr, "<");
	val["ALLEY_ACCESS"]=cleanSQL(arr[1]);
}

# KITCHEN
#<td>Nhà bếp</td><td>---</td>
/<td>Nhà bếp/{
	getline
	getline
	if (match($0,"check.gif")>0){
		val["KITCHEN"]=1;
	}
}

# LAND_TYPE
#<td>Loại BDS</td><td>Đất thổ cư, đất ở</td>
/<td>Loại BDS/{
	getline
	split($0, ar, "<td>");
	split(ar[2], arr, "<");
	val["LAND_TYPE"]=cleanSQL(arr[1]);
}

# LEGAL_STATUS
#<td>Pháp lý</td><td>Sổ hồng/ Sổ đỏ</td>
/<td>Pháp lý/{
	getline
	split($0, ar, "<td>");
	split(ar[2], arr, "<");
	val["LEGAL_STATUS"]=cleanSQL(arr[1]);
}

# PRO_WIDTH
#<td>Chiều ngang</td><td>12m</td>
/<td>Chiều ngang/{
	getline
	split($0, ar, "<td>");
	split(ar[2], arr, "<");
	val["PRO_WIDTH"]=cleanSQL(arr[1]);
}

# NB_FLOORS
#<td>Số lầu</td><td>---</td>
/<td>Số lầu/{
	getline
	split($0, ar, "<td>");
	split(ar[2], arr, "<");
	if (arr[1] ~ /[0-9]/){
		val["NB_FLOORS"]=arr[1];
	}
}

# GARAGE
#<td>Chổ để xe hơi</td><td><img src='/publish/img/check.gif'/></td>
/<td>Chổ để xe hơi/{
	getline
	getline
	if (match($0,"check.gif")>0){
		val["GARAGE"]=1;
	}
}

# PRO_LENGTH
#<td>Chiều dài</td><td>30m</td>
/<td>Chiều dài/{
	getline
	split($0, ar, "<td>");
	split(ar[2], arr, "<");
	val["PRO_LENGTH"]=cleanSQL(arr[1]);
}

# BEDROOM
#<td>Số phòng ngủ</td><td>---</td>
/<td>Số phòng ngủ/{
	getline
	split($0, ar, "<td>");
	split(ar[2], arr, "<");
	if (arr[1] ~ /[0-9]/){
		val["BEDROOM"]=arr[1];
	}
}

# DEALER_ID
#<input type='hidden' id='hddNguoiDang' value='195145' user='0'/>
/id='hddNguoiDang'/{
	split($0, ar, "hddNguoiDang'");
	split(ar[2], arr, "value='");
	split(arr[2], arrr, "'");
	val["DEALER_ID"]=arrr[1]
}

# MINI_SITE
# <div class='view-more'><a href='/nha-moi-gioi/093-379600.html'>Xem thêm 17 tin khác của thành viên này</a></div>
/div class='view-more'/{
	getline
	split($0,ar, "<a href='");
	split(ar[2],arr, "'>");
	val["MINI_SITE"]="https://alonhadat.com.vn"arr[1]
}

# LAT
# <span class='view-map' tabindex='0' lat='21.03552' lng='105.80381''>Xem bản đồ</span>
/<span class='view-map'/{
	split($0,ar, "lat='");
	split(ar[2],arr, "'");
	val["LAT"]= cleanSQL(arr[1])
}

# LON
# <span class='view-map' tabindex='0' lat='21.03552' lng='105.80381''>Xem bản đồ</span>
/<span class='view-map'/{
	split($0,ar, "lng='");
	split(ar[2],arr, "'");
	val["LON"]= cleanSQL(arr[1])
}

# PHOTOS
# /div class='moreinfor'/{
# 	for(i=1; i<=NF; i++) {
# 		tmp=match($i,"limage")
# 		if(tmp) {
# 			photo++;
# 		}	
# 	}
# 	if(photo>1){
# 		val["PHOTOS"]=photo-1;
# 	}
# 	else{
# 		val["PHOTOS"]=photo;
# 	}
# }

/limage/{
	photo++
	if(photo>1){
		val["PHOTOS"]=photo-1;
	}
	else{
		val["PHOTOS"]=photo;
	}
}


# ADS_ID
# <input type='hidden' id='hddPropertyType' value='11'/><input type='hidden' id='hddPropertyId' value='3455102'/><input type='hidden' id='hddNguoiDang' value='195145' user='0'/>
/id='hddPropertyId'/{
	split($0, ar, "hddPropertyId'");
	split(ar[2], arr, "value='");
	split(arr[2], arrr, "'");
	id=arrr[1]
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
		printf (" SITE=\"alonhadat\" WHERE SITE=\"alonhadat\" AND ID_CLIENT=\"%s\";\n", id)	
	}   
}