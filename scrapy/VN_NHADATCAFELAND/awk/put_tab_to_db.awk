BEGIN {
	FS = OFS = "\t"
	col=1;
	title[col]="ID_CLIENT"; col++
	title[col]="ADS_LINK"; col++
	#title[col]="TYPE"; col++
	title[col]="LAND_TYPE"; col++
	title[col]="PHOTOS"; col++
    title[col]="ADS_TITLE"; col++
	title[col]="BRIEF"; col++

	title[col]="FOR_SALE"; col++
	title[col]="FOR_LEASE"; col++
	title[col]="TO_BUY"; col++
	title[col]="TO_LEASE"; col++

	title[col]="DATE_ORIGINAL"; col++
	title[col]="CREATED_DATE"; col++

	TABLE=table
	max_col=col
	row=0
}

{
	row++
	value[row,"ID_CLIENT"] = $1
	value[row,"ADS_LINK"] = $2
	ads_type = $3
	value[row,"LAND_TYPE"] = $4
	value[row,"PHOTOS"] = $5
	value[row,"ADS_TITLE"] = $6
	value[row,"BRIEF"] = $7

	value[row,"CREATED_DATE"] = DATE
	value[row,"DATE_ORIGINAL"] = DATE

	if ( ads_type == "nha-dat-ban" ) {
		value[row,"FOR_SALE"] = 1
		value[row,"FOR_LEASE"] = 0
	} else if ( ads_type == "cho-thue" ) {
		value[row,"FOR_SALE"] = 0
		value[row,"FOR_LEASE"] = 1
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
			printf("INSERT IGNORE INTO %s SET %s SITE=\"nhadatcafeland\";", TABLE, data)
			printf("\n")
		}
		
	}
}