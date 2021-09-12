BEGIN { c=0 }

/class="wrap-plink"/ {
    c++
    val["CREATED_DATE",c] = created_date;
    val["DATE_ORIGINAL",c] = created_date;
    split($0, arr, "href=\"")
    split(arr[2], ar_1, "\"")
    val["ADS_LINK", c] = "https://batdongsan.com.vn"cleanSQL(ar_1[1])
    ads_link = cleanSQL(ar_1[1])
    nb=split(ads_link,arr,"-")
    gsub(/[^0-9]/,"",arr[nb])
    val["ID_CLIENT", c] = arr[nb]

    split($0, arr, "title=\"")
    split(arr[2], ar_1, "\"")
    val["ADS_TITLE", c] = cleanSQL(ar_1[1])

    if (ads_link ~ /ban/) {
        val["FOR_LEASE", c] = "0"
        val["FOR_SALE", c] = "1"
    }
    else if (ads_link ~ /cho-thue/) {
        val["FOR_LEASE", c] = "1"
        val["FOR_SALE", c] = "0"
    }

}

/class="area"/ {
    surf=cleanSQL($0)
    val["SURFACE_ORIGINAL", c]=surf
}


/class="tooltip-time"/ {
    temp_date=cleanSQL($0)
    val["ADS_DATE_ORIGINAL", c]=temp_date
    split(temp_date, updated_time, "/")
    if (updated_time[3] != "" && updated_time[2] != "" && updated_time[1] != "") {
        val["ADS_DATE", c] = updated_time[3] "-" updated_time[2] "-" updated_time[1]
    }
}

/class="price"/{
    temp_price = cleanSQL($0)
    val["PRICE_ORIGINAL", c]=temp_price
}

/class="product-media"/{
    photo=cleanSQL($0)
    if (photo != "") {
        val["PHOTOS", c] = photo
    }
}

/class="contact-name"/ {
    name=cleanSQL($0)
    if (name != "") {
        val["DEALER_NAME", c] = name
    }
}

/class="hidden-phone/ {
    phone=cleanSQL($0)
    if (phone != "") {
        val["DEALER_TEL", c] = phone
    }
}

/class="product-content"/ {
    loop=0;
    max_loop=10;
    do{
        getline;
        loop++
        temp=cleanSQL($0)
        if (temp != ""){
            val["BRIEF", c]=val["BRIEF", c] " " temp
        }
        

    }while (loop<max_loop && $0 !~ /<\/div>/)
}

END {
    max_c=c
    #check data parsing empty
    checkParsingEmpty(val)
    for(c=1; c<=max_c; c++) {
        if (val["ID_CLIENT",c] != "") {
            for(i=1; i<=max_i; i++) {
                gsub("\r|\t", "", val[title[i], c])
                gsub("\"", "", val[title[i], c])
                printf("%s\t", trim(val[title[i], c]))
            }
            printf("\n")
        }
    }
}
