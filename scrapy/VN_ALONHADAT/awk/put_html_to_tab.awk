BEGIN	{
	col=1;
	title[col]="ID_CLIENT"; col++
	title[col]="ADS_LINK"; col++
	title[col]="TYPE"; col++
	title[col]="BRIEF"; col++
	max_col=col
	row=0
}

/class='title' href='/{
	split($0, ar, "nha-dat/")
	split(ar[2],arr,".html")
	type=arr[1]
}

/<div class='ct_title'>/{
	row++
	getline
	value[row, "TYPE"] = type
	#$0: <a href='/cho-thue-phong-ky-tuc-xa-moi-xay-sach-se-thoang-mat-50m2-gia-1tr2-thang-2647518.html' class='vip'>Cho thuê phòng ký túc xá nam mới xây, sạch sẽ, thoáng mát, 50m2 giá 1tr2/tháng</a>
	split($0, arr, "<a href='")
	split(arr[2], arr1, ".html'")
	value[row, "ADS_LINK"] = domain""arr1[1]".html"

	split(arr[2],arr2,"\.html")
	split(arr2[1],arrr,"-")
	value[row, "ID_CLIENT"] = arrr[length(arrr)]
}

#Brief description
/<div class='ct_brief'>/{
	str="";
	do {
		temp=cleanSQL($0)
		if(length(temp) > 0){
			str=str" "temp;
		}
		getline;
	    } while (match($0, "</a>")==0);
	sub("... >", "", str);
	gsub(/\*/," ",str);
	value[row, "BRIEF"]=cleanSQL(decodeHTML(str))
}
END	{
	max_row = row
	for(row = 1; row <= max_row; row++){
		for(col = 1; col <= max_col; col++){
			printf("%s\t", value[row, title[col]])	
		}
		printf("\n")
	}
}
