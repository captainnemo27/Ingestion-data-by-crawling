BEGIN { c=0 }
/class='lazy'/{
  c++
  split($0,ar_1,/'/)
  val["ADS_LINK",c]="http://www.batdongsan.vn"ar_1[2]

  split($0,ar_2,"title=")
  gsub(/'/,"",ar_2[2])
  gsub(">","",ar_2[2])
  val["ADS_TITLE",c]=ar_2[2]

  n=split(ar_1[2], ar_3, "-")
  split(ar_3[n], ar_4, ".")

  gsub("p", "", ar_4[1])
  if (match(ar_4[1], /[0-9]+/) > 0) {
      val["ID_CLIENT", c] = ar_4[1]
  } else {
      val["ID_CLIENT", c] = ""
  }

  val["CREATED_DATE", c] = created_day
  val["DATE_ORIGINAL", c] = created_day

  split($0,ar_5,"data-src=")
  gsub(/title.*/,"",ar_5[2])
  gsub(/'/,"",ar_5[2])
  val["PHOTOS", c]="http://www.batdongsan.vn"trim(ar_5[2])
}

/<div class="al_author_tool hidden-xs">/{
  getline
  getline
  getline
  getline
  split($0,ar_3,"'")
  val["MINI_SITE",c]="http://www.batdongsan.vn"ar_3[2]
  getline 
  val["DEALER_NAME",c]=trim($0)
}

{
  if (sale_type ~ "RENT"){
  #val["SALE_TYPE",c]="Cho thuê"
  val["FOR_SALE",c]=0
  val["FOR_LEASE",c]=1
  }
  else if (sale_type ~ "SALE"){
  #val["SALE_TYPE",c]="Bán"
  val["FOR_SALE",c]=1
  val["FOR_LEASE",c]=0
  }
}

/price_unit/{
  getline

  temp_price = trim(decodeHTML(removeHtml($0)))
	val["PRICE_ORIGINAL", c]= temp_price
}
/class='city-item'/{
    getline
    getline
    val["CITY", c]=trim(decodeHTML(removeHtml($0)))
}

/class='wards-item'/{
    getline
    getline
    val["WARD", c]=trim(decodeHTML(removeHtml($0)))
}

/class='district-item'/{
    getline
    getline
    val["DISTRICT", c]=trim(decodeHTML(removeHtml($0)))
}

/product-area/{
  getline
  temp=trim(decodeHTML(removeHtml($0)));
  val["SURFACE_ORIGINAL", c]=temp;
}

/noidung hidden-xs/{
  temp="";
  for (i=1; i<=10; i++) {
        getline
        if ($0 == "</h3>") {
            break
        }
        temp=sprintf("%s%s",temp, $0)
    }
    val["BRIEF", c] = trim(decodeHTML(removeHtml(temp)))
}

/fa fa-user fa-fw margin-right-5 icon-baseline/{
  getline
  getline
  split($0,ar_3,"\\'")
  val["MINI_SITE",c]="http://www.batdongsan.vn"ar_3[2]
  getline 
  val["DEALER_NAME",c]=trim($0)
}
END {
  max_c=c

	for(c=1; c<=max_c; c++) {
        if (val["ID_CLIENT", c] == "") { continue; } 
        for(i=1; i<=max_i; i++) {
            gsub("\r|\t", "", val[title[i], c])
            gsub("\"", "", val[title[i], c])
            printf("%s\t", cleanSQL(val[title[i], c]))
        }
        printf("\n")
	}
}
