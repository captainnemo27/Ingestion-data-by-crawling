BEGIN	{
	col=1;
	title[col]="ID_CLIENT"; col++
	title[col]="ADS_LINK"; col++
    title[col]="ADS_TITLE"; col++
    title[col]="FOR_LEASE"; col++
    title[col]="FOR_SALE"; col++
    title[col]="PRICE"; col++
    title[col]="PRICE_UNIT"; col++
    title[col]="PRICE_ORIGINAL"; col++
	title[col]="SURFACE"; col++
    title[col]="SURFACE_UNIT"; col++
    title[col]="SURFACE_ORIGINAL"; col++
    title[col]="FULL_ADDRESS"; col++
    title[col]="TYPE"; col++
    title[col]="CREATED_DATE"; col++
    title[col]="DATE_ORIGINAL"; col++
	max_col=col
	row=0
}
#<a href="danh-sach-cho-thue-can-ho-westbay-aquabay-gia-tot-khu-do-thi-ecopark-lien-he-em-ha-es1269950" title="Danh s&#xE1;ch cho thu&#xEA; c&#x103;n h&#x1ED9; Westbay - Aquabay gi&#xE1; t&#x1ED1;t khu &#x111;&#xF4; th&#x1ECB;  Ecopark, li&#xEA;n h&#x1EC7; em H&#xE0;" class="thumb-image">
/class="product-item/{
    row++
    getline
    split($0,ar,"href=\"")
    split(ar[2],arr,"\"")
    value[row, "ADS_LINK"] = "https://homedy.com"arr[1]

    if (arr[1] ~ "cho-thue"){
        value[row,"FOR_SALE"]=0
        value[row,"FOR_LEASE"]=1
    }else{
        value[row,"FOR_SALE"]=1
        value[row,"FOR_LEASE"]=0
    }

    nb=split(arr[1],arrr,"-")
    value[row, "ID_CLIENT"]=arrr[nb]
    gsub(/[^0-9]/,"",value[row, "ID_CLIENT"]);
    
    split($0,ar,"title=\"")
    split(ar[2],arr,"\"")
    value[row, "ADS_TITLE"]=decode_hex(cleanSQL(arr[1]))
    
}

#ads_address
/class="address"/{
    getline;getline
    adr=decode_hex(cleanSQL($0))
    value[row, "FULL_ADDRESS"]=decode_hex(adr)
}   

/class="price"/{
    temp_price = decode_hex(cleanSQL($0))
	value[row, "PRICE_ORIGINAL"]=temp_price
}

/class="acreage"/{
    surf=decode_hex(cleanSQL($0))
    value[row, "SURFACE_ORIGINAL"] = surf
}


END	{
	max_row = row
	for(row = 1; row <= max_row; row++){
		#print(row)
        if (value[row, "ID_CLIENT"] !=""){
            value[row, "DATE_ORIGINAL"] = value[row, "CREATED_DATE"]=DATE
            for(col = 1; col <= max_col; col++){
                printf("%s\t", value[row, title[col]])
            }
            printf("\n")
        }
	}
}
