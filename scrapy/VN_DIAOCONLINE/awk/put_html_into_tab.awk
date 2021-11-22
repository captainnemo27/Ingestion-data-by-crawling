BEGIN { c=0 }

/class="hightlight_type_1 margin_bottom"/{
    c++
    for (i=0; i < 6; ++i) {getline}

    val["CREATED_DATE", c] = created_day
    val["DATE_ORIGINAL", c] = created_day
    if ($0 ~ /4 hình/) {
        split(cleanSQL($0), arr, "hình")
        gsub(/[^0-9]+/, " ", arr[1])
        val["PHOTOS", c] = arr[1]
    }
}

/class="info margin_left"/{
    getline; getline
    split($0, arr, "href=\"")
    split(arr[2], ar_1, "\"")
    ads_link = cleanSQL(ar_1[1])
    val["ADS_LINK", c] = "https://diaoconline.vn"ads_link

    split(ads_link, ar_2, "/")
    if (ar_2[2] ~ /thue/) {
        val["FOR_LEASE", c] = "1"
        val["FOR_SALE", c] = "0"
    }
    else if (ar_2[2] ~ /ban/) {
        val["FOR_LEASE", c] = "0"
        val["FOR_SALE", c] = "1"
    }

    getline
    val["ADS_TITLE", c] = cleanSQL($0)
}

/Cập nhật/{
    val["ADS_DATE",c]=created_day;
    val["ADS_DATE_ORIGINAL",c]=cleanSQL($0)
    if($0 ~ /trước/)
        val["ADS_DATE",c]=created_day;
    else {
        temp=cleanSQL($0)
        split(temp, arr, " ");
        split(arr[3], arr_2,"/");

        if (arr_2[3] != "" && arr_2[2] != "" && arr_2[1] != "") {
            val["ADS_DATE",c]=arr_2[3]"-"arr_2[2]"-"arr_2[1]
        }
    }
}

/Vị trí/{
    getline; getline
    val["DISTRICT", c] = cleanSQL($0)

    getline; getline; getline; getline
    val["CITY", c] = cleanSQL($0)
}

/class="price"/{
    for (i=0; i < 5; ++i) {getline}
    temp_price = trim(decodeHTML(removeHtml($0)))
    val["PRICE_ORIGINAL",c] = temp_price 
}

/Mã số tài sản/ {
    getline; getline
    val["ID_CLIENT", c] = cleanSQL($0)
}

/class="contact_info"/{
    for (i = 0; i < 9; ++i) {getline}
    temp = cleanSQL($0)
    if (temp ~ /^[0-9]+/) {
        gsub(/[^0-9]/, "", temp)
        val["DEALER_TEL", c] = temp
    }
} 

END {
    max_c=c

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
