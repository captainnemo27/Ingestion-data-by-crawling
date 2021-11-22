####################################################
# PARSING PHOTO                                    #
####################################################
#  <input type="hidden" name="ctl00$ContentPlaceHolder1$ProductDetail1$CountImage" id="CountImage" value="3" />
/CountImage/{
    if (val["PHOTOS"]==""){
	split($0,photo,"value=\"");    
	split(photo[2],photo,"\"");
	val["PHOTOS"]=photo[1]
    }
}
/class="spanprice"/{
    getline;
	val["PRICE_ORIGINAL"]=cleanSQL($0)
}
/>Ngày đăng tin</{
    getline;getline;getline;
    val["ADS_DATE_ORIGINAL"]=cleanSQL($0)
}

/>Số phòng ngủ</{
if (val["BEDROOM"]==""){
    getline;
    getline;
    val["BEDROOM"] = cleanSQL($0);
    }
}
####################################################
# PARSING DETAILED_BRIEF                           #
####################################################
#  <div class="pd-desc-content">             - View đẹp, thoáng mát.^M<br/>- 2PN 1WC.^M<br/>- Đầy đủ nội thất sang chảnh.^M<br/>* Giá thương lượng cho khách thiện chí.^M<br/>LH 0938178898 </div>
/class="pd-desc-content"/{
if (val["DETAILED_BRIEF"]==""){
    temp = ""
    loop = 0
    max_loop=80
    while ($0 !~ /<\/div>/ && loop<max_loop){
        getline
        line=cleanSQL($0)
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
}

# <div class="mg-bottom-25 textdescription" id="txtdescription">
#        <div class="text-content">
#            Do định cư nước ngoài nên cần bán gấp căn 3 PN diện tích 100m2, giá bán 5.4 tỷ. View thoáng mát không bị chắn, nhà hiện tại đang trống nên còn mới, xem nhà liên hệ trước 1 tiếng.<br/>LH Bình 0938497815.

/id="txtdescription"/{
    if ( val[DETAILED_BRIEF] =="") {
          temp = ""
          loop = 0
          max_loop=80
          while ($0 !~ /<\/div>/ && loop<max_loop){
              getline
              line=cleanSQL($0)
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
}
/class="product-detail"/{
if (val["ADS_TITLE"]==""){
    getline; getline;
     val["ADS_TITLE"]=cleanSQL($0);
    }
}

/class="bl-title-02"/{
if (val["ADS_TITLE"]==""){
    getline; getline;
     val["ADS_TITLE"]=cleanSQL($0);
    }
}

/>Email</{
if (val["DEALER_EMAIL"]==""){
    getline; getline;getline; getline;getline; getline;getline;
     val["DEALER_EMAIL"]=cleanSQL($0);
    }
}

####################################################
# PARSING LAT LON                                  #
####################################################
#   <input type="hidden" name="ctl00$ContentPlaceHolder1$ProductDetail1$hddLatitude" id="hddLatitude" value="14.058324" />
# <input type="hidden" name="ctl00$ContentPlaceHolder1$ProductDetail1$hddLongtitude" id="hddLongtitude" value="108.277199" />

/hddLatitude/{
	split( $0, lat, "value=\"" );
	split(lat[2],lat,"\"");
	val["LAT"]=lat[1];
}

/hddLongtitude/{
	split( $0, lon, "value=\"" );
	split(lon[2],lon,"\"");
	val["LON"]=lon[1];
}
####################################################
# PARSING DISTRICT/CITY                                     #
####################################################
# <input type="hidden" name="ctl00$ContentPlaceHolder1$ProductDetail1$hddDiadiem" id="hddDiadiem" value="Đường Mạc Thái Tông, Phường Trung Hòa, Cầu Giấy, Hà Nội" />
/id="hddDiadiem"/{
    split( $0, arr_1, "value=\"" );
   split(arr_1[2],arr_1,"\"");
   val["FULL_ADDRESS"]=arr_1[1]  
}

####################################################
# PARSING DETAIL
# 

/>Đường vào</{
  if (val["ALLEY_ACCESS"] ==""){
     getline;
     getline;
     sizes = cleanSQL($0);
     if (sizes == ""){
        getline;
     }
     val["ALLEY_ACCESS"] = cleanSQL($0);
     }
}

/>Số tầng</{
  if (val["NB_FLOORS"] ==""){
     getline;
     getline;
     tmp = cleanSQL($0);
     if (tmp == ""){
     getline;
     }
     val["NB_FLOORS"] = cleanSQL($0);
     }
}


/>Mặt tiền</{
  if (val["FRONTAGE"] ==""){
     getline;
     getline;
     getline;
     val["FRONTAGE"] =  cleanSQL($0);
  } 
}

/>Hướng nhà</{
	if (val["PRO_DIRECTION"] ==""){
      getline;
     getline;
     tmp= cleanSQL($0);
     if (tmp == "" ){
     getline;}

     val["PRO_DIRECTION"] = cleanSQL($0);
     
     }
}
/>Số phòng</{
if (val["NB_ROOMS"]==""){
    getline;
    getline;
    tmp =  cleanSQL($0);
    if (tmp == ""){
            getline;}
    val["NB_ROOMS"] = cleanSQL($0);
    }
}

/>Loại tin rao</{
if (val["LAND_TYPE"]==""){
    getline;
    getline;
    tmp = cleanSQL($0);
    if (tmp == ""){
            getline;}
    val["LAND_TYPE"] = cleanSQL($0);
    }
    gsub(/Bán|Cho thuê/,"",val["LAND_TYPE"])
}
/Diện tích:<span>/{
    getline;
    temp=cleanSQL($0)
	val["SURFACE_ORIGINAL"]=temp
}
/>Số toilet</{
 if (val["BATHROOM"]==""){
   getline;
   getline;
   tmp =  cleanSQL($0);
    if (tmp == ""){
            getline;}
     val["BATHROOM"] = cleanSQL($0);
   }
}

/>Tên liên lạc</{
 if (val["DEALER_NAME"]==""){
   getline;
   getline;
   getline;
   val["DEALER_NAME"] = cleanSQL($0); 
   }
}

/>Di động</{
if (val["DEALER_TEL"]==""){
   getline;
   getline;
   getline;
   val["DEALER_TEL"] = cleanSQL($0);
   }
 }

/>Địa chỉ</{
if (val["DEALER_ADDRESS"]==""){
	   getline;
	      getline;
	         getline;
		    val["DEALER_ADDRESS"] = cleanSQL($0);
	    }
	
}


END {

	if(val["PHOTOS"]==0)
	    val["PHOTOS"]=""

  val["PRO_FLAG"]=0;
  val["CREATED_DATE"]=day
	 #check data parsing empty
	checkParsingEmpty(val)
	     # add SITE
	val["SITE"]=site
	            #check data parsing empty
        if ( id != ""){
		 printf "update IGNORE "table" set "
		 for (i=1; i<max_i;i++) {
	           if (val[title[i]] != "") {
	             printf ("%s=\"%s\", ", title[i], cleanSQL(val[title[i]]))
	           }
	      }
	    printf (" SITE=\""site"\" WHERE SITE=\""site"\" AND ID_CLIENT=\"%s\";\n", id)
	  }
}
