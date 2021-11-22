BEGIN{
    # PARAMETER
    ## type
    ## model
    row=0;
}

#################################
# PARSING ID_CLIENT FOR DETAIL  #
#################################
# <h2 class="prop-title">
# <a class="link-overlay" href="https://mogi.vn/quan-go-vap/mua-nha-biet-thu-lien-ke/ban-nha-hem-2mt-hxh-6m-nguyen-van-luong-4x10m-1-lau-p16-q-go-vap-id20679372">Bán nhà hẻm 2MT - HXH 6m Nguyễn Văn Lượng 4x10m, 1 Lầu, P16, Q Gò Vấp</a>
# </h2>
/"prop-info"/{
    getline;
    row++
	val["NAME",row]=cleanSQL($0);
    split($0,href_1,"href=\"");
    split(href_1[2],href_2,"\">");
    temp=href_2[1];
    val["ADS_LINK",row]=temp;
    match(temp,"-id[0-9]+$");
    val["ID_CLIENT",row]=substr(temp,RSTART,RLENGTH);
    gsub("-id","",val["ID_CLIENT",row]);  
    getline;
    if(match($0,"class=\"prop-title\"")){
        val["ADS_TITLE",row]=cleanSQL($0)
    }
}
/class="prop-attr"/{
    getline;
     temp=cleanSQL($0);
        if (temp ~ /[0-9]/)  {
            val["SURFACE_ORIGINAL",row]=temp
        }
        getline;
        getline;
        temp=cleanSQL($0)
        if( temp ~ "PN" ){
            val["BEDROOM",row]=temp
            gsub(/[^0-9|^.]/, "", val["BEDROOM",row]);
        }
        getline;
        temp=cleanSQL($0)
        if( temp ~ "WC" ){
            val["BATHROOM",row]=temp
            gsub(/[^0-9|^.]/, "", val["BATHROOM",row]);
        }
}

/class="price"/{   
        temp_price=cleanSQL($0);
        val["PRICE_ORIGINAL",row] = temp_price
}

END {
    max_row = row;
    for (c=1; c <= max_row; c++) {
        val["LAND_TYPE",c]=model;
        
        val["FOR_SALE",c]=0;
        val["FOR_LEASE",c]=0;
        if(type=="mua"){
            val["FOR_SALE",c]=1;
        }else if(type=="thue"){
            val["FOR_LEASE",c]=1;
        }

        val["CREATED_DATE",c]=created_day;
        val["DATE_ORIGINAL",c]=created_day;

		if (val["ID_CLIENT",c] != "") {
			for (i=1; i < max_i; i++) {
				printf ("%s\t", cleanSQL(val[title[i],c]))
			}
			printf ("\n" )
		}
    }
}