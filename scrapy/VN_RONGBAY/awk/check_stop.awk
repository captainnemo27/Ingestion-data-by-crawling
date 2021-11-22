/subCateWork subCateBDS [^ subCateBDS_BGVIP| ad_sponsor]/ {
	# ADS_DATE
	do  {
		getline;
		if (match($0, "class=\"date_ad") != 0) {
			temp=trim(cleanSQL($0));
			split(temp, ar, "/");
			ads_date=year"-"ar[2]"-"ar[1];
		}
	}while (match($0, "class=\"date_ad") == 0);

	if(compare_date(ads_date, start)==-1) {
		print  "check_id=\""stop"\";"
		exit;
	}
}


