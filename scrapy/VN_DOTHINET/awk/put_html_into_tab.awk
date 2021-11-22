BEGIN	{
	row=0
}
# <a class="vip2" title="Ưu đãi Khủng, Free 2 tháng - Cho thuê văn phòng ảo giá chỉ từ 600 nghìn/tháng tại Hà Nội" href="/cho-thue-van-phong-pho-trung-kinh-phuong-yen-hoa-2/uu-dai-khung-free-2-thang-cho-thue-van-phong-ao-gia-chi-tu-600-nghinthang-tai-ha-noi-pr13136126.htm">Ưu đãi Khủng, Free 2 tháng - Cho thuê văn phòng ảo giá chỉ từ 600 nghìn/tháng tại Hà Nội</a>

/<a class="vip/{
    row++;
	split($0,arr,"href=\"");
	split(arr[2],arr,"\"");
	value[row, "ADS_LINK"] = "https://dothi.net"cleanSQL(arr[1])

	if ( value[row, "ADS_LINK"] ~ "cho-thue"){
		value[row,"FOR_LEASE"]=1;
		value[row,"FOR_SALE"]=0;
			  
	} else {
		value[row,"FOR_SALE"]=1;
		value[row,"FOR_LEASE"]=0; 
    }

	split($0,tt,"title=\"");
	split(tt[2],tt,"\"");
	value[row, "ADS_TITLE"] = cleanSQL(tt[1])
	value[row, "CREATED_DATE"]=created_day;
	value[row, "DATE_ORIGINAL"]=created_day;

}

# <a rel="nofollow" onclick="productSaved(this,'12866046');" class="listProductSearch saveProductDetail" id="12866046">Lưu tin</a>
/class="listProductSearch saveProductDetail"/{
    split( $0, arrId, "id=\"" );
    split(arrId[2],arrId,"\"");
    value[row, "ID_CLIENT"] = arrId[1]
}
#     <label>Vị trí<span>:</span></label>
#     <strong>Phan Rang - Tháp Chàm - Ninh Thuận</strong>
/>Vị trí</{
	getline;getline;
	loc=cleanSQL($0)
	split (loc, arr_l, "-")
	value[row, "CITY"] = arr_l[2]
	value[row, "DISTRICT"] = arr_l[1]
}

/class="price"/{
getline;
getline;
getline;
temp_price=cleanSQL($0);
value[row, "PRICE_ORIGINAL"] = temp_price
}

/class="area"/{
getline;
	getline;
	getline;
	temp=cleanSQL($0)
	value[row,"SURFACE_ORIGINAL"]=temp
}

/class="date"/{
	getline;
 	dd = cleanSQL($0)
	value[row,"ADS_DATE_ORIGINAL"] = dd
     gsub(" ","",dd)
     # 12/01/2020 => Yyyy-mm-dd
     nb=split(dd,arr_d,"/")
     d_n=arr_d[3]"-"arr_d[2]"-"arr_d[1]
     value[row,"ADS_DATE"] = d_n
}

END	{
	max_row = row
    #check data parsing empty
    checkParsingEmpty(value)
	for(row = 1; row <= max_row; row++){
		 if (value[row,"ID_CLIENT"] != "") {
			for(col = 1; col <= max_i; col++){
				gsub("\r|\t", "", value[row, title[col]])
                gsub("\"", "", value[row, title[col]])
				printf("%s\t", value[row, title[col]])
			}
		   print("\n")

		}

	}
}

