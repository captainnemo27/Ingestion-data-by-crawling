/<span class="property_code">/ {
	split($0, arr_id, "<strong>");
	getline;
	if(match($0, "trước")>0)
		ads_date=date;
	else {
		temp=removeHtml($0);
		split(temp, arr, " ");
		split(arr[3], arr_2,"/");
		ads_date=arr_2[3]"-"arr_2[2]"-"arr_2[1]
	}
	if(compare_date(ads_date, start)==-1) {
		temp=trim(removeHtml(arr_id[2]));
		print  "check_id=\""temp"\";"
		exit;
	}
	
}



