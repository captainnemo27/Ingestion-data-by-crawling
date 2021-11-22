BEGIN	{
	col=1;
	title[col]="ID_CLIENT"; col++
	#title[col]="ADS_LINK"; col++
	title[col]="MINI_SITE"; col++ #detail mode
	val["ID_CLIENT"]=id
	val["ADS_LINK"]=ads_url
	max_col=col
	row=0
}
# MINI_SITE
# <div class='view-more'><a href='/nha-moi-gioi/093-379600.html'>Xem thêm 17 tin khác của thành viên này</a></div>
/a href='\/nha-moi-gioi/{
	split($0,ar, "<a href='");
	split(ar[2],arr, "'>");
	val["MINI_SITE"]="https://alonhadat.com.vn"arr[1]
}

END	{
	for (i=1; i< max_col;i++) {
		printf("%s\t", val[title[i]])
	}
	printf("\n")
}
