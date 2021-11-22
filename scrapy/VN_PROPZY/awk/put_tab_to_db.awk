BEGIN {
	FS = OFS = "\t"
	col=1;
	title[col]="ID_CLIENT"; col++
	title[col]="ADS_LINK"; col++
	#title[col]="TYPE"; col++
	title[col]="LAND_TYPE"; col++
	title[col]="PHOTOS"; col++
	title[col]="ADS_TITLE"; col++
	title[col]="FULL_ADDRESS"; col++
	title[col]="PRO_DIRECTION"; col++
	title[col]="BEDROOM"; col++
	title[col]="BATHROOM"; col++
	title[col]="PROJECT_NAME"; col++
	title[col]="PRICE"; col++
	title[col]="PRICE_UNIT"; col++
	title[col]="SURFACE"; col++
	title[col]="SURFACE_UNIT"; col++

	title[col]="FOR_SALE"; col++
	title[col]="FOR_LEASE"; col++

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
	land = $4
	value[row,"PHOTOS"] = $5
	value[row,"ADS_TITLE"] = $6
	value[row,"FULL_ADDRESS"] = $7
	value[row,"PRO_DIRECTION"] = $8
	value[row,"BEDROOM"] = $9
	value[row,"BATHROOM"] = $10
	value[row,"PROJECT_NAME"] = $11
	value[row,"PRICE"] = $12
	value[row,"PRICE_UNIT"] = $13
	value[row,"SURFACE"] = $14
	value[row,"SURFACE_UNIT"] = $15
	value[row,"CITY"] = $16
	value[row,"CREATED_DATE"] = DATE
	value[row,"DATE_ORIGINAL"] = DATE

	if ( ads_type == "mua" ) {
		value[row,"FOR_SALE"] = 1
		value[row,"FOR_LEASE"] = 0
	} else if ( ads_type == "thue" ) {
		value[row,"FOR_SALE"] = 0
		value[row,"FOR_LEASE"] = 1
	}

	if ( land == "can-ho" ) {
		value[row,"LAND_TYPE"] = "Căn hộ"
	} else if ( land == "dat-nen" ) {
		value[row,"LAND_TYPE"] = "Đất nền"
	} else if ( land == "nha" ) {
		value[row,"LAND_TYPE"] = "Nhà riêng"
	} else if ( land == "dat-nen-du-an" ) {
		value[row,"LAND_TYPE"] = "Đất nền dự án"
	}
}

END {
	max_row = row
	for(row = 1; row <= max_row; row++){
		data=""
		for (col=1; col < max_col; col++) {
			if (( value[row,title[col]] != "None" ) && ( value[row,title[col]] != "" ) && ( value[row,title[1]] != "" )) {
				data = data""sprintf("%s = \"%s\", ", title[col], value[row,title[col]])
			}
		}
		if ( data != "" && TABLE != "" ) {
			printf("INSERT IGNORE INTO %s SET %s SITE=\"propzyvn\";", TABLE, data)
			printf("\n")
		}
		
	}
}