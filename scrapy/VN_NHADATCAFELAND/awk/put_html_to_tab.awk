BEGIN	{
	col=1;
	title[col]="ID_CLIENT"; col++
	title[col]="ADS_LINK"; col++
	title[col]="TYPE"; col++
	title[col]="LAND_TYPE"; col++
	title[col]="PHOTOS"; col++ 
    title[col]="ADS_TITLE"; col++
	title[col]="BRIEF"; col++
	max_col=col
	row=0

	start_to_take = 0
	stop_to_take = 0

	start_to_take_brief = 0
	stop_to_take_brief = 0
}

/<link rel="canonical"/{
    split($0,ar,"nhadat.cafeland.vn/")
    split(ar[2],arr,"/\"")
    if (match(arr[1],"nha-dat-ban")){
        type="nha-dat-ban"
    } else if (match(arr[1],"cho-thue")){
        type="cho-thue"
    }
}

# <section id="properties-search" class="display-lines">
/<section/{
    if ( start_to_take == 0 ) {
        start_to_take = 1
    }
}
/<\/section>/{
    if ( start_to_take == 1 ) {
        stop_to_take = 1
    }
}

# https:\/\/nhadat\.cafeland\.vn\/[a-z-A-Z0-9]+[0-9]+\.html
/<figure class="tag status"/{
    if ( start_to_take == 1 && stop_to_take == 0 ) {
        row++
        #<figure class="tag status">1 <i class="fa fa-camera">
        split($0, ar, "tag status\">")
        split(ar[2], arr, " <i class=")
        value[row, "PHOTOS"] = cleanSQL(arr[1])
        
        # Set type
        value[row, "TYPE"] = type
    }
}

/<header/{
    if ( start_to_take == 1 && stop_to_take == 0 ) {
        getline
        #<a rel="nofollow" href="https://nhadat.cafeland.vn/hot-duy-nhat-100-nen-lien-ke-san-bay-long-thanh-shr-gia-chi-750trnen-1445077.html" title="HOT: DUY NHẤT 100 NỀN- LIỀN KỀ SÂN BAY LONG THÀNH- SHR- GIÁ CHỈ: &quot;750TR/NỀN&quot;">
        split($0, href, "href=\"")
        if (match(href[2],"https://nhadat.cafeland.vn/")){
            split(href[2], href, "\"")
            value[row, "ADS_LINK"] = cleanSQL(href[1])
            match(href[1],/[0-9]+\.html/,ads_id)
            split(ads_id[0], ads_id, ".html")
            value[row, "ID_CLIENT"] = ads_id[1]

            #ads_title
            getline
            #<h3>HOT: DUY NHẤT 100 NỀN- LIỀN KỀ SÂN BAY LONG THÀNH- SHR- GIÁ CHỈ: &quot;750TR/NỀN&quot;</h3>
            tit=removeHtml($0)
            value[row, "ADS_TITLE"]=cleanSQL(tit)
        } else {
            split(href[2], href, "\"")
            value[row, "ADS_LINK"] = "https://nhadat.cafeland.vn/"cleanSQL(href[1])
            match(href[1],/[0-9]+\.html/,ads_id)
            split(ads_id[0], ads_id, ".html")
            value[row, "ID_CLIENT"] = ads_id[1]
            getline
            tit=removeHtml($0)
            value[row, "ADS_TITLE"]=cleanSQL(tit)
        }
        
    }
}

/<aside>/{	
    start_to_take_brief = 1
    brief = ""
}
/<\/aside>/{
    if ( start_to_take_brief == 1 ){
        stop_to_take_brief = 1
    }
}
//{
    if ( start_to_take_brief == 1 && stop_to_take_brief == 0 ) {
		if (match($0,"<b>Diện tích:</b>")){
			#print("DT")
		}
		else if (match($0,"<b>Liên hệ:</b>")){
			#print("LH")
		}
		else if (match($0,"<b>Quận huyện:</b>")){
			#print("QH")
		}
        else if ( brief != "" ) {
            if ( cleanSQL($0) != "" ) {
                brief = brief" "cleanSQL($0)
            }
        } else {
            brief = cleanSQL($0)
        }
        value[row, "BRIEF"] = brief
    }
    if (value[row, "BRIEF"]==""){
        value[row, "BRIEF"]="None"
    }
}
# Reset the condition about taking brief
/class="post-status"/{
  start_to_take_brief = 0
  stop_to_take_brief = 0
}
END	{
	max_row = row
	for(row = 1; row <= max_row; row++){
		#print(row)
        if (value[row, "ID_CLIENT"] !=""){
            for(col = 1; col <= max_col; col++){
                printf("%s\t", value[row, title[col]])
            }
            printf("\n")
        }
	}
}
