BEGIN {
	i=1
	# DEFINE
	title[i]="ID_CLIENT";		i++;
	title[i]="ADS_LINK";		i++;

	#########################################
	# LIST									#
	# Only list have this title				#
	#########################################
	title[i]="FOR_SALE";		i++;
	title[i]="FOR_LEASE";		i++;
	title[i]="CITY";			i++;
	title[i]="DISTRICT";		i++;
	title[i]="LAND_TYPE";		i++;
	title[i]="ADS_TITLE";		i++;
	title[i]="ADS_DATE";		i++;
	title[i]="ADS_DATE_ORIGINAL";		i++;
	title[i]="PRICE";			i++;
	title[i]="PRICE_UNIT";		i++;
	title[i]="PRICE_ORIGINAL";		i++;	
	title[i]="PRICE_M2";		i++;
	title[i]="SURFACE";			i++;
	title[i]="SURFACE_UNIT";		i++;
	title[i]="SURFACE_ORIGINAL";		i++;	
	title[i]="CREATED_DATE";	i++;
	title[i]="DATE_ORIGINAL";	i++;

	#############################################
	# LIST + DETAIL								#
	# Both list and detail have all this title	#
	#############################################
	title[i]="FULL_ADDRESS";	i++;
	title[i]="BEDROOM";			i++;
	title[i]="BATHROOM";		i++;
	title[i]="NB_ROOMS";		i++; 
	title[i]="NB_FLOORS";		i++; 	
	title[i]="KITCHEN";			i++;
	title[i]="ALLEY_ACCESS";			i++;
	title[i]="FRONTAGE";			i++;
	

	#############################################
	# DETAIL									#
	# Only detail have this title				#
	#############################################

	title[i]="DETAILED_BRIEF";	i++;
	title[i]="LEGAL_STATUS";	i++;
	title[i]="PRO_DIRECTION";		i++;
	title[i]="DEALER_NAME";		i++;
	title[i]="PHOTOS";			i++;
	title[i]="DEALER_ID";		i++;
	title[i]="DEALER_EMAIL";           i++;
	title[i]="DEALER_ADDRESS";           i++;
	title[i]="LAT";				i++;
	title[i]="LON";				i++;
	title[i]="WARD";			i++;
	title[i]="USED_SURFACE";		i++;
	title[i]="USED_SURFACE_UNIT";	i++;
	title[i]="USED_SURFACE_ORIGINAL";	i++;
	title[i]="DEALER_TEL";		i++;
	title[i]="CHECK_CONVERT"; i++; 
	title[i]="PRO_FLAG"; i++; 

	#############################################
	# LET THIS FIELD AT THE END					#
	#############################################
	# title[i]="SITE";			i++;

	max_i=i;
}
