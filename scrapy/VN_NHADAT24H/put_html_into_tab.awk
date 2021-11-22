BEGIN {
    c=0;
}

/class="dv-breadcrumb"/{
	getline;getline;getline;
	city=cleanSQL($0);
	sub("»","",city);

	getline;getline;
	temp=cleanSQL($0);
	if (match(temp, "cho thuê") > 0) {
		for_lease=1;
	} 
	if (match(temp, "Cần thuê") > 0)  {
		to_lease=1;
	} 
	if (match(temp, "Nhà đất bán") > 0) {
		for_sale=1;
	}
	if (match(temp, "Cần mua") > 0) {
		to_buy=1;
	}
}

#ID_CLIENT & NAME
/preAlink/ {
	c++;
	split($0, ar,"preAlink-");
	split(ar[2], arr, "\"");
	val["ID_CLIENT",c]=arr[1];

	split($0, arr, "href=\"")
	split(arr[2], arr2, "\"")
	val["ADS_LINK",c]="https://nhadat24h.net"arr2[1]

	val["NAME",c]=cleanSQL($0)
	val["CITY",c]=city;
	val["FOR_LEASE",c]=for_lease;
	val["FOR_SALE",c]=for_sale;
	val["TO_BUY",c]=to_buy;
	val["TO_LEASE",c]=to_lease;
}

#</i> <a class="btnlocationdetail">Pháo Đài Láng, Quận Đống Đa</a>
/class="btnlocationdetail"/{
	val["FULL_ADDRESS",c]=cleanSQL($0);
}

#<label class="lbhowfar" data-lat="21.0433693498362" data-lng="105.820807134363">
/class="lbhowfar"/{
	split($0,ar,"data-lat=\"");
	split(ar[2],arr, "\"");
	val["LAT",c]=arr[1];

	split($0, ar_2, "data-lng=\"");
	split(ar_2[2], ar_1, "\"");
	val["LON",c]=ar_1[1];
}

/class="reviewproperty1"/ {
	utilities="";
	while(match($0, "class=\"a-txt-cl1\"") == 0){
		getline;
		if(match($0, "class=\"fa fa-road\"") > 0){
			getline;
			temp=cleanSQL($0);
			utilities=utilities", "temp;
		}
		if(match($0, "class=\"fa fa-arrows-alt\"") > 0){
			getline;
			temp=cleanSQL($0);
			utilities=utilities", "temp;
		}
		if(match($0, "class=\"fa fa-compass\"") > 0){
			getline;
			temp=cleanSQL($0);
			utilities=utilities", "temp;
		}
		if(match($0, "class=\"fa fa-building\"") > 0){
			getline;
			temp=cleanSQL($0);
			utilities=utilities", "temp;
		}
		if(match($0, "class=\"fa fa-bed\"") > 0){
			getline;
			temp=cleanSQL($0);
			utilities=utilities", "temp;
		}
		if(match($0, "class=\"fa fa-bath\"") > 0){
			getline;
			temp=cleanSQL($0);
			utilities=utilities", "temp;
		}
	}
	sub(", ", "", utilities);
	val["UTILITIES",c]=utilities;
}

# PRICE & UNIT_PRICE
#<lable class="a-txt-cl1">
#<strong>4.3</strong> Tỷ</lable> </span>
/class="a-txt-cl1">/{
	getline;
	if(match($0, "lable") > 0){
		temp=cleanSQL($0);
		split(temp, ar, " ");
		val["PRICE",c]=ar[1];
		val["PRICE_UNIT",c]=ar[2];
	} else {
		val["PRICE",c]=cleanSQL($0);
	}
}

# SQUARE & UNIT_SQUARE
#<lable class="a-txt-cl2">
#<strong>85</strong> m²</lable>
/<lable class="a-txt-cl2">/{
	getline;
	temp=cleanSQL($0);
	split(temp, ar, " ");
	val["SQUARE",c]=ar[1];
	val["AREA_UNIT",c]=ar[2];
}

/class="lb-des">/{
	str="";
	while(match($0, "</label>") == 0){
		temp=cleanSQL($0);
		if(length(temp) > 0){
			str=str", "temp;
		}
		getline;
	}
	sub(", ", "", str);
	sub("Xem tiếp", "", str);
	
	val["BRIEF",c]=str;
}

/class="a-txt-cl1" href="javascript:LoadlinkSearch/{
	val["LAND_TYPE",c]=cleanSQL($0);
}

END {
	 max_c=c
    for(c=1;c<=max_c;c++) {	
#	if (start == "--" || end =="--") {	# when do not use -f and -t arguments
		if (val["ID_CLIENT",c] != "") {
			for (i=1; i<max_i;i++) {
				gsub("\r|\t", "", val[title[i], c])
				gsub("\"", "", val[title[i], c])
					printf("%s\t", cleanSQL(val[title[i], c])) 	
			}
			printf ("\n" )
		}
		
#	}else{ # use -f and -t arguments
#		if(compare_date(start, end)==1) { # if start afer end -> swap
#			temp=start;
#			start=end;
#			end=temp;
#		}
#		if ((compare_date(start, val["ADS_DATE",c])==1) || (compare_date(end, val["ADS_DATE",c])==-1)) # skip ads outside from start to end
#			continue;
#		else{
#			if (val["ID_CLIENT",c] != "") {
#				for (i=1; i<max_i;i++) {
#					gsub("\r|\t", "", val[title[i], c])
#					gsub("\"", "", val[title[i], c])
#						printf("%s\t", cleanSQL(val[title[i], c])) 	
#				}
#				printf ("\n" )
#			}
#		}
#	}
   }
}




