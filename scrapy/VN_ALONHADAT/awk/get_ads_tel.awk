BEGIN {
   	col=1
	title[col]="DEALER_TEL"; col++
	title[col]="DEALER_NAME"; col++
	title[col]="DEALER_ADDRESS"; col++
	title[col]="CREATED_DATE"; col++
	title[col]="PRO_FLAG"; col++

	max_col=col
	id=ADS_ID

	#Input
	val["CREATED_DATE"]=DATE
	val["PRO_FLAG"]=0
}

/class='fullname'/{
	getline
	gsub(/<[^>]+>/,"",$0)
	val["DEALER_NAME"]=cleanSQL($0)
}

# DEALER_TEL
# <a href='tel:0909026586'>0909.026.586</a>
# <a href='tel:0911388728'>0911.388.728</a> / <a href='tel:0906796876'>0906.796.876</a>
/<a href='tel/{
	value="";
	for(i=1; i<=NF; i++) {
		tmp=match($i,"tel:")
		if(tmp) {
			split($i,ar, "tel:");
			split(ar[2],arr, "'");
			value=value" "arr[1]
		}	
	}
	val["DEALER_TEL"]= cleanSQL(value)
}

/class='address'/{
	split($0, ar, "'address'>");
	split(ar[2],arr,"</div>")
	gsub(/<[^>]+>/,"",arr[1])
	val["DEALER_ADDRESS"]=cleanSQL(arr[1])
}


END {
	if (id != "*"){
		printf "UPDATE IGNORE "table" SET "
		for (i=1; i< max_col;i++) {
			str=cleanSQL(val[title[i]]);	
			if (str != "") {
				printf ("%s=\"%s\", ", title[i], str);
				}
		}
		printf (" SITE=\"alonhadat\" WHERE SITE=\"alonhadat\" AND ID_CLIENT=\"%s\";\n", id)		
	}   
}