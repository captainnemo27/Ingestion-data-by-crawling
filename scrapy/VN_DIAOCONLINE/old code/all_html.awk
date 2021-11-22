BEGIN {
   	i=1
	title[i]="SALE_TYPE"; i++;	
	title[i]="SQUARE"; i++;
	title[i]="UNIT_SQUARE"; i++;	
	title[i]="WIDTH"; i++;
	title[i]="LENGTH"; i++;		
	title[i]="FULL_ADDRESS"; i++;
	title[i]="DISTRICT"; i++;
	title[i]="CITY"; i++;
	title[i]="LAND_TYPE"; i++;
	title[i]="LEGAL_STATUS"; i++;
	title[i]="DIRECTION"; i++;
	title[i]="UTILITIES"; i++;
	title[i]="DETAILED_BRIEF"; i++;

	max_i=i   
}

# SALE_TYPE
/<div itemscope itemtype=/{
	dem++;
	if(dem==2) {
	getline
	a=cleanSQL($0)
	if(match(a, "Bán")!=0)
		val["SALE_TYPE"]="Bán"
	else
		val["SALE_TYPE"]="Cho thuê"
	}
}

# FULL_ADDRESS 
/<span class="location">/{
	getline
	temp=cleanSQL($0)
	val["FULL_ADDRESS"]=trim(temp);
}

# ID
/<div class="feat_item">/{
	getline;getline;getline
	
	gsub(/<[^>]+>/, "", $0);
	temp=trim($0);
	gsub(" ", "", temp);
	id=temp;
	
	getline;getline;getline
	split($0, ar, /^0-9/);
	val["SQUARE"]=ar[1];
	val["UNIT_SQUARE"]=ar[2];
	
	print val["UNIT_SQUARE"]
	print val["SQUARE"]
}

# LAND_TYPE 
/Loại địa ốc: <strong>/{
	getline
	val["LAND_TYPE"]=cleanSQL($0)
}

#LEGAL_STATUS
/Tình trạng pháp lý: <strong>/{
	getline
	val["LEGAL_STATUS"]=cleanSQL($0)
}

# DIRECTION
/ Hướng: <strong>/{
	getline
	val["DIRECTION"]=cleanSQL($0)
}

# UTILITIES
/<div class="block">/{
	str="";
	dem2++
	if(dem2==3)
	{	
		do {
			getline;
			temp=cleanSQL($0);
			if(length(temp)>1)
			{	
				split($0, arr, "<span class=\"");
				if(match(arr[2], "ico_16 ico_check_16")!=0)
				{
					str=str ", " removeHtml(arr[1]);
				}
			}		
		}while(match($0, "</tbody>")==0);
		sub(",","",str);
		val["UTILITIES"]=str;
	}

}

# DETAILED_BRIEF
/<span>MÔ TẢ CHI TIẾT/ {
	str="";	
	getline;getline;getline;
	do{
		getline;
		temp = cleanSQL($0);
    		if(length(temp)>0){
			str=str temp;
		}
	}while(match($0,"<div class=")==0);
	val["DETAILED_BRIEF"]=str;
}

# WIDTH
/Chiều ngang trước: <strong>/{
	dem3++;
	if(dem3==1)
	{
		getline
		val["WIDTH"]=cleanSQL($0)
 	}  
}


END {
	printf "update IGNORE "table" set "
	for (i=1; i<= max_i;i++) {
		str=cleanSQL(val[title[i]]);	
	        if (str != "") {
	            printf ("%s=\"%s\", ", title[i], str);
	        }
	}
	printf (" site=\"DIAOCONLINE\" where site=\"DIAOCONLINE\" and ID_CLIENT=\"%s\";\n", id)
}



