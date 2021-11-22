BEGIN { c=0 }

/class="js__product-link-for-product-id"/ {
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

/class="re__card-config-area"/ {
    surf=cleanSQL($0)
    val["SURFACE_ORIGINAL", c]=surf
}


/data-microtip-position="right"/ {
    split($0, arr, "aria-label=\"")
    split(arr[2], ar_1, "\"")
    val["ADS_DATE_ORIGINAL", c]=ar_1[1]
    split(ar_1[1], updated_time, "/")
    if (updated_time[3] != "" && updated_time[2] != "" && updated_time[1] != "") {
        val["ADS_DATE", c] = updated_time[3] "-" updated_time[2] "-" updated_time[1]
    }
}

/re__card-config-price/{
    temp_price = cleanSQL($0)
    val["PRICE_ORIGINAL", c]=temp_price
}

/ class="re__icon-image"/{
    getline;getline;
    photo=cleanSQL($0)
    if (photo != "") {
        val["PHOTOS", c] = photo
    }
}

/class="re__card-published-info-contact-name"/ {
    getline;getline;
    name=cleanSQL($0)
    if (name != "") {
        val["DEALER_NAME", c] = name
    }
}

/mobile="/ {
    split($0, arr, "mobile=\"")
    split(arr[2], phone, "\"")
    if (phone[1] != "") {
        val["DEALER_TEL", c] = phone[1]
    }
}

/class="re__card-description js__card-description"/ {
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
