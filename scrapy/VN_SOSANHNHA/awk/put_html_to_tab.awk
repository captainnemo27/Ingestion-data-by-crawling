BEGIN	{
	col=1;
	title[col]="ID_CLIENT"; col++
	title[col]="ADS_LINK"; col++
	title[col]="TYPE"; col++
    title[col]="ADS_TITLE"; col++
	title[col]="BRIEF"; col++
    
    title[col]="LAND_TYPE"; col++
	title[col]="ADS_DATE"; col++
	title[col]="ALL_SURFACE"; col++
	title[col]="ALL_PRICE"; col++
    title[col]="DEALER_NAME"; col++
	title[col]="DEALER_TEL"; col++
	title[col]="DEALER_EMAIL"; col++
    title[col]="FULL_ADDRESS"; col++

	max_col=col
	row=0
    flag=0
    count=1

	start_to_take = 0
}

/class="box_empty"/{
    flag=1
}

/<\/section>/{
    getline

    #<script>function fn303a65f988f998e4de65b8be038c1a9b(){var data1618565991={"bc92f472fc03cdef5f5bb8a111aaf91e":"1,8 t\u1ef7","dd979fbbc587785ee7dae0aaaa8e3e5f":"60m\u00b2","d3fe1395534444b2a7f10dfabda530f5":"<i class=\"mcon-phone\">
    split($0,ar,"{")
    split(ar[3],arr,"<i")
    split(arr[1],arrr,"\"")
    #price count=1
    if (match(arrr[8],"mcon-phone")){
        val = cleanSQL(decode_hex(arrr[4]))
        gsub (" ", "", val)
        if (match(val,"/m2")){
            value[count, "ALL_PRICE"] = cleanSQL(decode_hex(arrr[4]))
            value[count, "ALL_SURFACE"] = "None"
        }
        else if (match(val,"m2")) {
            value[count, "ALL_PRICE"] = "None"
            value[count, "ALL_SURFACE"] = cleanSQL(decode_hex(arrr[4]))
        } 
        else {
            value[count, "ALL_PRICE"] = cleanSQL(decode_hex(arrr[4]))
            value[count, "ALL_SURFACE"] = "None"
        }
    }
    else {
        value[count, "ALL_PRICE"] = cleanSQL(decode_hex(arrr[4]))
        value[count, "ALL_SURFACE"] = cleanSQL(decode_hex(arrr[8]))
    }

    
    # if (match(arrr[4],"m\u00b2")){
    #     value[count, "ALL_PRICE"] = "None"
    # } else {
    #     value[count, "ALL_PRICE"] = cleanSQL(decode_hex(arrr[4]))
    # }
    
    #surface count=1
   
    # if (arrr[8]==""){
    #     value[count, "ALL_SURFACE"] = "None"
    # } else {
    #     value[count, "ALL_SURFACE"] = cleanSQL(decode_hex(arrr[8]))
    # }
    
    do {
        getline
        
        #<\/i>766080838"};var class1618565991=["bc92f472fc03cdef5f5bb8a111aaf91e","dd979fbbc587785ee7dae0aaaa8e3e5f"
        if (match($0,"</script>")){
            split($0,ar,"\"}")
            if (removeHtml(ar[1])==""){
                value[count, "DEALER_TEL"] = "None"
            } else{
                value[count, "DEALER_TEL"] = "0"cleanSQL(removeHtml(ar[1]))
            }
            break    
        }

        #<\/i>921976910","19f246b3f406b06cc425154d1d346260":"700 tri\u1ec7u","f9774b67344be8362cb9f2a953372239":"49m\u00b2","a4b0f9bceb9b7b1208942ffa9dc8a3e3":"<i class=\"mcon-phone\">
        #telephone count=1
        split($0,ar,":\"")
        split(ar[1],ar1,"\",\"")
        if (removeHtml(ar1[1])==""){
            value[count, "DEALER_TEL"] = "None"
        } else{
            value[count, "DEALER_TEL"] = "0"cleanSQL(removeHtml(ar1[1]))
        }

        split(ar[2],ar2,"\",\"")
        split(ar[3],ar3,"\",\"")

        count++
        # #price count+1=2
        # #surface count+1=2

        # dont have price or surface
        if (match(ar3[1],"mcon-phone")){
            val = cleanSQL(decode_hex(ar2[1]))
            gsub (" ", "", val)
            if (match(val,"/m2")){
                value[count, "ALL_PRICE"] = cleanSQL(decode_hex(ar2[1]))
                value[count, "ALL_SURFACE"] = "None"
            }
            else if (match(val,"m2")) {
                value[count, "ALL_PRICE"] = "None"
                value[count, "ALL_SURFACE"] = cleanSQL(decode_hex(ar2[1]))
            } 
            else {
                value[count, "ALL_PRICE"] = cleanSQL(decode_hex(ar2[1]))
                value[count, "ALL_SURFACE"] = "None"
            }
        }
        # full price and surface
        else {
            value[count, "ALL_PRICE"] = cleanSQL(decode_hex(ar2[1]))
            value[count, "ALL_SURFACE"] = cleanSQL(decode_hex(ar3[1]))
        }

        # if (ar2[1]==""){
        #     value[count, "ALL_PRICE"] = "None"
        # } else {
        #     value[count, "ALL_PRICE"] = cleanSQL(decode_hex(ar2[1]))
        # }
                
        
        # if (ar3[1]==""){
        #         value[count, "ALL_SURFACE"] = "None"
        # } else {
        #     value[count, "ALL_SURFACE"] = cleanSQL(decode_hex(ar3[1]))
        # }
    } while (match($0,"</script>")==0)
}

/<h1 class="name">/{
    t = removeHtml($0)
    split(t,ti,"tại")
    if ((match(t,"Bán")) || (match(t,"bán"))){
        type="can-ban"
        gsub("Bán","",ti[1])
        gsub("bán","",ti[1])
    }
    else if ((match(t,"Cho thuê")) || (match(t,"cho thuê"))){
        type="cho-thue"
        gsub("Cho thuê","",ti[1])
        gsub("cho thuê","",ti[1])
    } else {
        type="can-ban"
    }
    land=cleanSQL(ti[1])
}

/<div class="home_listting">/{
    if ( start_to_take == 0 ) {
        start_to_take = 1
    }
}

/<div class="info">/{
    if ( start_to_take == 1 ) {
        row++
        getline; getline
        split($0,ar,"href=\"")
        split(ar[2],arr,"\"")
        value[row, "ADS_LINK"] = "https://sosanhnha.com"arr[1]

        split(ar[2],a,"title=\"")
        split(a[2],aa,"\">")
        ss = removeHtml(aa[1])
        if (ss==""){
            value[row, "ADS_TITLE"]="None"
        } else {
            value[row, "ADS_TITLE"]=cleanSQL(ss)
        }

        split(arr[1],arrr,"-")
        value[row, "ID_CLIENT"]=arrr[length(arrr)]

        
        if (type==""){
            value[row, "TYPE"]="None"
            value[row, "LAND_TYPE"]="None"
        } else {
            value[row, "TYPE"] = type
            value[row, "LAND_TYPE"] = land
        }
    }
    
}

/class="date"/{
    getline
    t = removeHtml($0)
    if (match(t,"Hôm qua")){
        tt=strftime("%Y-%m-%d", systime() - 86400)
    } else if (match(t,"Hôm nay")){
        tt=strftime("%Y-%m-%d", systime()) 
    } else if (match(t,"giờ")){
        split(t,ti,"giờ")
        hour = int(ti[1])
        split(ti[2],tii,"phút")
        min = int(tii[1])
        tt=strftime("%Y-%m-%d", systime() - hour*3600 - min*60)
    } else if (match(t,"phút")){
        split(t,ti,"phút")
        number = int(ti[1])
        gsub(/[^0-9]/,"",number)
        number=int(number)
        tt=strftime("%Y-%m-%d", systime() - number*60)
    } 
    else {
        split(t,ti,"-")
        tii = cleanSQL(ti[1])
        split(tii,tiii,"/")
        tt=tiii[3]"-"tiii[2]"-"tiii[1]
    }
    if (tt==""){
        value[row, "ADS_DATE"]="None"
    } else {
        value[row, "ADS_DATE"]=tt
    }
}

/<div class="user_address">/{
    getline; getline; getline; getline
    t = removeHtml($0)
    if (cleanSQL(t)==""){
        value[row, "FULL_ADDRESS"] = "None"
    } else {
        value[row, "FULL_ADDRESS"] = cleanSQL(t)
    }
}

/<div class="avatar_name">/{
    getline
    t = removeHtml($0)
    if (cleanSQL(t)==""){
        value[row, "DEALER_NAME"] = "None"
    } else {
        value[row, "DEALER_NAME"] = cleanSQL(t)
    }
}

/class="user_mail"/{
    getline; getline; getline
    t = removeHtml($0)
    value[row, "DEALER_EMAIL"] = cleanSQL(t)
}

/<p class="teaser">/{
    if ( start_to_take == 1 ) {
        temp=$0
        do {
            getline
            temp = temp" "$0
        } while (match($0,"<div class=\"more_info\">")==0)
        t = removeHtml(temp)
        if (t==""){
            value[row, "BRIEF"]="None"
        } else {
            value[row, "BRIEF"]=cleanSQL(t)
        }
    }
}

END	{
    if (flag == 1){
        # print("No data")
    }
    else {
        max_row = row
        for(row = 1; row <= max_row; row++){
            #print(row)
            if (value[row, "ID_CLIENT"] !=""){
                for(col = 1; col <= max_col; col++){
                    if (value[row, "DEALER_EMAIL"]==""){
                        value[row, "DEALER_EMAIL"] = "None"
                    }
                    printf("%s\t", value[row, title[col]])
                }
                printf("\n")
            }
        }
    }
}
