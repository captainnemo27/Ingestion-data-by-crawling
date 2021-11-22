BEGIN{
    # PARAMETER
    ## table
    ## site

    # DEFINE
    val["PHOTOS"]=0;
}

####################################################
# PARSING PHOTO                                    #
####################################################
# <div class="media-item">
# <img src="https://cloud.mogi.vn/images/201804/28/133/f21fe8064ac841fb93503db34d3904cb.jpg" alt="Hình ảnh Bán gấp căn Villa - Biệt thự ở Đường số 44 , P. Thảo Điền  giá 75 Tỷ" />
# </div>
/media-item/{
    val["PHOTOS"]++;
}

####################################################
# PARSING DEALER_NAME DEALER_ID                    #
####################################################
# <div class="agent-name">
# <a href="/moi-gioi/0902971889-tran-nam-uid22371">Trần Nam</a>
/agent-name/{
    getline;
    if(val["DEALER_NAME"]==""){
        val["DEALER_NAME"]=cleanSQL($0);
        split($0,arr_1,"href=\"");
        split(arr_1[2],arr,"\"");
        match(arr[1],"uid.*$");
        val["DEALER_ID"]=substr(arr[1],RSTART,RLENGTH);
        gsub(/^uid/,"",val["DEALER_ID"]);
    }
}

####################################################
# PARSING DEALER_TEL                                #
####################################################
# <div class="agent-contact">
# <a href="tel:0902971889" class="fa-phone bold" gtm-event="link" gtm-cat="detail" gtm-act="mobile-call" ng-bind="PhoneFormat('0902971889')">0902971889</a>
/agent-contact/{
    if(val["DEALER_TEL"]==""){
        getline;
        match($0,"tel:[0-9]+\"");
        val["DEALER_TEL"]=substr($0,RSTART,RLENGTH);
        gsub(/[^0-9]/,"",val["DEALER_TEL"]);
    }
}

####################################################
# PARSING ADS_TITLE FULL_ADDRESS PRICE PRICE_UNIT       #
####################################################
#<div class="title">
#<h1>Bán Nhà Trả Nợ Ngân Hàng, Nhà Mặt Nguyễn Giản Thanh, DT: 52m2</h1>
/class="title"/{
    getline;
    val["ADS_TITLE"]=cleanSQL($0);
}
/class="address"/{
     val["FULL_ADDRESS"]=cleanSQL($0);
}
/class="price"/{
    temp_price=cleanSQL($0);
    val["PRICE_ORIGINAL"] = temp_price
}



####################################################
# PARSING PRICE PRICE_UNIT                         #
####################################################
# <span>Giá</span>: 75 tỷ</li>
/>Giá</{
    if(val["PRICE_ORIGINAL"]==""){
        split(cleanSQL($0),arr,":");
        temp_price=arr[2];
        val["PRICE_ORIGINAL"] = temp_price
}
      
}

####################################################
# PARSING USED_SURFACE USED_SURFACE_UNIT                 #
####################################################
# <span>Diện tích sử dụng</span>: 297 m<sup>2</sup></li>
/>Diện tích sử dụng</{
    if ($0 !~ /[0-9]/)
        getline;
    split(cleanSQL($0),arr,":");
    if (arr[2] ~ /[0-9]/)
        val["USED_SURFACE_ORIGINAL"]= arr[2]
    else
        val["USED_SURFACE_ORIGINAL"]=cleanSQL($0)
}
####################################################
# PARSING SURFACE SURFACE_UNIT                           #
####################################################
/>Diện tích đất</{
    if ($0 !~ /[0-9]/)
        getline;
    split(cleanSQL($0),arr,":");
    if (arr[2] ~ /[0-9]/)
        val["SURFACE_ORIGINAL"]= arr[2]
    else
        val["SURFACE_ORIGINAL"]=cleanSQL($0)
}


####################################################
# PARSING ADS_DATE                                 #
####################################################
/>Ngày đăng</{
    if ($0 !~ /[0-9]/)
        getline;
    split(cleanSQL($0),arr,":");
    if (arr[2] ~ /[0-9]/)
        val["ADS_DATE_ORIGINAL"]=val["ADS_DATE"]= arr[2]
    else
        val["ADS_DATE_ORIGINAL"]=val["ADS_DATE"]= cleanSQL($0)
}


####################################################
# PARSING ID_CLIENT                                #
####################################################
#<span>Mã BĐS</span>
#<span>20128860</span>
/>Mã BĐS</{
    getline;
    val["ID_CLIENT"]=cleanSQL($0)
}

####################################################
# PARSING BEDROOM                                  #
####################################################
/>Phòng ngủ</{
    getline;
    val["BEDROOM"]=cleanSQL($0)
}

####################################################
# PARSING BATHROOM                                 #
####################################################
/>Nhà tắm</{
    getline;
    val["BATHROOM"]=cleanSQL($0)
}
####################################################
# PARSING LEGAL_STATUS                             #
####################################################
/>Pháp lý</{
    getline;
    val["LEGAL_STATUS"]=cleanSQL($0)
}

####################################################
# PARSING DIRECTION                                #
####################################################
/>Hướng</{
    getline;
    val["PRO_DIRECTION"]=cleanSQL($0);
}

####################################################
# PARSING DETAILED_BRIEF                           #
####################################################
/property="og:description"/{
    split($0,arr,"content=\"")
    split(arr[2],arr,"\"")
    val["DETAILED_BRIEF"]=arr[1]
}

####################################################
# PARSING LAT LON                                  #
####################################################
/title="map"/{
    split($0,arr,"src=\"");
    split(arr[2],arr_1,"\"");
    match(arr_1[1],"&q=.*$");
    temp=substr(arr_1[1],RSTART,RLENGTH);
    split(temp,arr,",");
    gsub(/[^0-9.]/,"",arr[1]);
    val["LAT"]=arr[1];
    val["LON"]=arr[2];
}

####################################################
# PARSING WARD                                     #
####################################################
# <a href="/review-khu-vuc/phuong-thao-dien-wid10943" class="ward-title link-overlay">Phường Thảo Điền</a>
/ward-title/{
    val["WARD"]=cleanSQL($0);
}

####################################################
# PARSING DISTRICT                                 #
####################################################
# <div class="ward-adress">Quận 2</div>
/ward-adress/{
    val["DISTRICT"]=cleanSQL($0);
}

####################################################
# PARSING CITY                                     #
####################################################
# <li property="itemListElement" typeof="ListItem">
# <a property="item" typeof="WebPage" href="/ho-chi-minh/mua-nha-biet-thu-lien-ke" title="TPHCM" gtm-event="link" gtm-cat="listing" gtm-act="breadcrumb">
# <span property="name">TPHCM</span>
# </a>
# <meta property="position" content="3">
/itemListElement/{
    if(val["CITY"]==""){
        getline;
        getline;
        temp=$0;
        getline;
        getline;
        if(match($0,"content=\"3\"")){
            val["CITY"]=cleanSQL(temp);
        }
        if(match($0,"content=\"4\"")){
            val["DISTRICT"]=cleanSQL(temp);
        }
    }
}


END {
    #check if there is no photo dont print it
    if(val["PHOTOS"]==0)
        val["PHOTOS"]=""

    # add SITE
    val["SITE"]=site
    val["PRO_FLAG"]=0;
    val["CREATED_DATE"]=today;
	#check data parsing empty
	checkParsingEmpty(val)
	if (val["ADS_TITLE"]!=""){
	    printf "update IGNORE "table" set "
	    for (i=2; i<max_i;i++) {
	        if (val[title[i]] != "") {
                printf ("%s=\"%s\", ", title[i], cleanSQL(val[title[i]]))
	        }
	    }
	    printf " SITE=\""val["SITE"]"\" where ID_CLIENT=\""cleanSQL(val["ID_CLIENT"])"\";\n"
	}
}
