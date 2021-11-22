BEGIN {
    c=0;
}

# ID_CLIENT, ADS_LINK, NAME, PRICE
# <section id="subCateBDS_28343253" lang="28343253" class="subCateWork subCateBDS " >
#/section id="subCateBDS/ {
/id="ad_id_/ {
    c++

    val["CREATED_DATE", c] = created_day
    val["DATE_ORIGINAL", c] = created_day
    if(sale_type == "SALE") {
        val["FOR_LEASE", c] = 0
        val["FOR_SALE", c] = 1
    }
    else {
        val["FOR_LEASE", c] = 1
		val["FOR_SALE", c]= 0
    }

	split($0, ar, "item_id=\"");
	split(ar[2], ar2, "\"");
	val["ID_CLIENT", c]=ar2[1];

    split($0, ar, "href=\"");
    split(ar[2], ar2, "\"");
    val["ADS_LINK", c]=ar2[1];
}

/class="date_ad/ {
    getline;
    val["ADS_DATE_ORIGINAL", c] = cleanSQL($0)
    split(cleanSQL($0), arr, "/")
    if (arr[1] != "" && arr[2] != "")
        val["ADS_DATE", c] = year"-"arr[2]"-"arr[1]
}

/class="salary roboto_bold/ {
    getline
    val["ADS_TITLE", c] = cleanSQL($0)
}

# Rent
/title_object roboto_regular cl_666 font_12/ {
    getline
    if (val["BRIEF", c] == "") {
        val["BRIEF", c] = cleanSQL($0)
    }
}

# Sale
/title_object roboto_regular cl_999 font_12/ {
    getline
    if (val["BRIEF", c] == "") {
        val["BRIEF", c] = cleanSQL($0)
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
