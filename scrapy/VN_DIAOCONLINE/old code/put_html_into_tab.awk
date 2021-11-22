BEGIN {
    c=0;
}

#get PHOTOS
/class="hightlight_type_1 margin_bottom"/ {
	c++;
	val["PHOTOS",c]="0";
	getline;getline;getline;getline;getline
	
	if (match($0,"<span>") > 0){
		temp=cleanSQL($0);
		if (length(temp) > 0){
			split(temp, arr," ")
			val["PHOTOS",c]=arr[1];
		}		
	}	
}

# NAME
/<div class="info margin_left">/ {
	getline;getline;
	val["NAME",c]=cleanSQL($0)
	
}

# CITY & DISTRICT
/<span class="location">/ {
	getline
	temp=removeHtml($0)
	split(temp, arr, " ,")
	val["DISTRICT",c]=arr[1]
	getline
	val["CITY",c]=cleanSQL($0)
	
}

# BRIEF
/<div class="features">/ {
	str="";	
	do{
		getline;
		temp = cleanSQL($0);
    		if(length(temp)>0){
			str=str temp;
		}
	}while(match($0,"</div>")==0);

	sub(",","",str);
	val["BRIEF",c]=str;
}

# get LINK
/class="ico_16 ico_arrow_16"/ {
	split($0, arr, "href=\"")
	split(arr[2], arr2, "\">")
	val["ADS_LINK",c]="http://diaoconline.vn"arr2[1]
	
}

#get ID_CLIENT
/div class="right margin_left"/ {
	getline;getline
	split($0, arr, "<strong>")
	val["ID_CLIENT",c]=cleanSQL(arr[2]) ; 
	getline;
	if(match($0, "trước")>0)
		val["ADS_DATE",c]=date;
	else {
		temp=cleanSQL($0);
		split(temp, arr, " ");
		split(arr[3], arr_2,"/");
		
		val["ADS_DATE",c]=arr_2[3]"-"arr_2[2]"-"arr_2[1]
	}
	getline;getline;
	split($0, arr, "<strong>")
	#val["PRICE",c]=cleanSQL(arr[2])

	temp_price = cleanSQL(arr[2])
	if(match(temp_price,/[T|t][ỷ|ỉ]/) > 0) {
		val["UNIT_PRICE", c]="Tỷ";
		if(match(temp_price, /[T|t]riệu/) > 0) {
			sub(/[T|t][ỷ|ỉ]/,".",temp_price);
			gsub(/[^0-9|^.]/, "", temp_price);
			val["PRICE",c]=temp_price;
		}
		else {
			split(temp_price, ar, /[T|t][ỷ|ỉ]/);
			val["PRICE",c]=trim(ar[1]);
		}
		
	} 
	else if (match(temp_price,/[T|t]riệu/) > 0) {
		val["UNIT_PRICE", c]="Triệu";
		split(temp_price, arr, /[T|t]riệu/);
		val["PRICE",c]=trim(arr[1]);
	}

	getline;getline;getline;getline
	split($0, arr, "<strong>")
	val["DEALER_NAME",c]=cleanSQL(arr[2])
	getline
	val["TELEPHONE",c]=cleanSQL($0)
}

END {
    max_c=c
    for(c=1;c<=max_c;c++) {	
	if (start == "--" || end =="--") {	# when do not use -f and -t arguments
		if (val["ID_CLIENT",c] != "") {
			for (i=1; i<max_i;i++) {
				gsub("\r|\t", "", val[title[i], c])
				gsub("\"", "", val[title[i], c])
					printf("%s\t", cleanSQL(val[title[i], c])) 	
			}
			printf ("\n" )
		}
		
	}else{ # use -f and -t arguments
		if(compare_date(start, end)==1) { # if start afer end -> swap
			temp=start;
			start=end;
			end=temp;
		}
		if ((compare_date(start, val["ADS_DATE",c])==1) || (compare_date(end, val["ADS_DATE",c])==-1)) # skip ads outside from start to end
			continue;
		else{
			if (val["ID_CLIENT",c] != "") {
				for (i=1; i<max_i;i++) {
					gsub("\r|\t", "", val[title[i], c])
					gsub("\"", "", val[title[i], c])
						printf("%s\t", cleanSQL(val[title[i], c])) 	
				}
				printf ("\n" )
			}
		}
	}
    }
}




