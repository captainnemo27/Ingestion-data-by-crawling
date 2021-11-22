BEGIN { c=0 }
/id="hplTitle"/{
    c++
    val["CREATED_DATE", c] = created_day
    val["DATE_ORIGINAL", c] = created_day
    split($0, arr, "title=\"")
    split(arr[2], arr_1, "\"")
    val["ADS_TITLE",c] = arr_1[1]

    split($0, arr, "href=\"")
    split(arr[2], arr_1, "\"")
    val["ADS_LINK",c] = "https://tinbatdongsan.com"arr_1[1]

    split(arr_1[1], arr_2, ".htm")
    n = split(arr_2[1], ar_id, "-")

    if(match(ar_id[n], /pr[0-9]+/) != 0){
        gsub("pr","",ar_id[n]);
        val["ID_CLIENT",c]= ar_id[n];
    } else {
        val["ID_CLIENT",c] = "";
    }
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
/class="fa fa-map-marker hint fsize-14 mg-right-5"/{
    getline;
    getline;
    add=cleanSQL($0)
    nb=split(add,arr,"-")
    val["CITY",c]=arr[nb]
    val["DISTRICT",c]=arr[1]
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
