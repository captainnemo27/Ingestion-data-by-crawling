BEGIN {
	FS = OFS = "\t"
	col=1;
	title[col]="ID_CLIENT"; col++
	title[col]="ADS_LINK"; col++
	#title[col]="TYPE"; col++
    title[col]="ADS_TITLE"; col++
	title[col]="BRIEF"; col++
    title[col]="LAND_TYPE"; col++
	title[col]="ADS_DATE"; col++
	title[col]="ALL_SURFACE"; col++
	title[col]="ALL_PRICE"; col++
    title[col]="DEALER_NAME"; col++
	title[col]="DEALER_TEL"; col++
	title[col]="DEALER_EMAIL"; col++
    title[col]="FULL_ADDRESS"; col++

	title[col]="FOR_SALE"; col++
	title[col]="FOR_LEASE"; col++
	title[col]="TO_BUY"; col++
	title[col]="TO_LEASE"; col++

	title[col]="SURFACE"; col++
	title[col]="SURFACE_UNIT"; col++
	title[col]="PRICE"; col++
	title[col]="PRICE_UNIT"; col++

	title[col]="STREET"; col++
	title[col]="WARD"; col++
	title[col]="DISTRICT"; col++
	title[col]="CITY"; col++

	title[col]="CREATED_DATE"; col++
	title[col]="DATE_ORIGINAL"; col++

	TABLE=table
	max_col=col
	row=0
}

{
	row++
	value[row,"ID_CLIENT"] = $1
	value[row,"ADS_LINK"] = $2
	ads_type = $3
	value[row,"ADS_TITLE"] = $4
	value[row,"BRIEF"] = $5
	value[row,"LAND_TYPE"] = $6
	value[row,"ADS_DATE"] = $7
	surface = $8
	price = $9
	value[row,"DEALER_NAME"] = $10
	value[row,"DEALER_TEL"] = $11
	value[row,"DEALER_EMAIL"] = $12
	value[row,"FULL_ADDRESS"] = $13
	value[row,"CREATED_DATE"] = DATE
	value[row,"DATE_ORIGINAL"] = DATE

	if ( ads_type == "can-ban" ) {
		value[row,"FOR_SALE"] = 1
		value[row,"FOR_LEASE"] = 0
	} else if ( ads_type == "cho-thue" ) {
		value[row,"FOR_SALE"] = 0
		value[row,"FOR_LEASE"] = 1
	}

	if ( surface == "None" ) {
		#value[row,"SURFACE"] = ""
	} else {
		if (surface ~ /[0-9]/){
			split(surface,arr,"m")
			value[row,"SURFACE"] = arr[1]
			value[row,"SURFACE_UNIT"] =  "m2"
		}
	}

	if ( price == "None" ) {
		#value[row,"PRICE"] = ""
	} else {
		if (price ~ /[0-9]/){
			split(price,ar," ")
			value[row,"PRICE"] = ar[1]
			gsub(/[.,]/,"",ar[2])
			value[row,"PRICE_UNIT"] =  ar[2]
		}
	}
	
}

END {
	max_row = row
	for(row = 1; row <= max_row; row++){
		data=""
		for (col=1; col < max_col; col++) {
			if (( value[row,title[col]] != "None" ) && ( value[row,title[col]] != "" )) {
				data = data""sprintf("%s = \"%s\", ", title[col], value[row,title[col]])
			}
		}
		if ( data != "" && TABLE != "" ) {
			printf("INSERT IGNORE INTO %s SET %s SITE=\"sosanhnha\";", TABLE, data)
			printf("\n")
		}
		
	}
}