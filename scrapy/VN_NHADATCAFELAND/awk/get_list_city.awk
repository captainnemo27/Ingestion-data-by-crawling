BEGIN {
	total_count = 0;
    max_page=0;
    ads_page=25;
    col=1;
	title[col]="NUMBER"; col++
	title[col]="ADS_LINK"; col++
    title[col]="LOCATION"; col++
    title[col]="TYPE"; col++
    max_col=col
	row=0
}

/class="seller-box tin-khu-vuc-dang cityFilterReal"/{
    getline; getline; getline;

    do {
        getline

        if (match($0, "<a href=")){
            #<a href="https://nhadat.cafeland.vn/nha-dat-ban-tai-tp-ho-chi-minh/" title="Mua bán nhà đất TP. Hồ Chí Minh"> TP. Hồ Chí Minh
            row++
            split($0,ar,"\"")
            value[row,"ADS_LINK"]=ar[2]
            split(ar[2],arr,"-tai-")
            split(arr[1],a,"nhadat.cafeland.vn/")
            value[row,"TYPE"]=a[2]
            split(arr[2],arrr,"/")
            #gsub("-","_",arrr[1])
            value[row,"LOCATION"]=arrr[1]
            getline; getline
            #(286237)</a>
            t=cleanSQL(removeHtml($0))
            gsub(/[()]/,"",t)
            value[row,"NUMBER"]=t
        }
    } while (match($0, "</aside>")==0);
}

END	{
	max_row = row
	for(row = 1; row <= max_row; row++){
		#print(row)
		for(col = 1; col <= max_col; col++){
			printf("%s\t", value[row, title[col]])	
		}
		printf("\n")
	}
}