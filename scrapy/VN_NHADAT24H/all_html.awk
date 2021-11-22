BEGIN {
   	i=1;

	title[i]="DISTRICT"; i++;
	title[i]="CITY"; i++;
	title[i]="SALE_TYPE"; i++;
	title[i]="DIRECTION"; i++;
	title[i]="DETAILED_BRIEF"; i++;
	title[i]="DEALER_NAME"; i++;
	title[i]="DEALER_ID"; i++;
	title[i]="DELAER_TYPE"; i++;
	title[i]="DEALER_ADDRESS"; i++;
	title[i]="MINI_SITE"; i++;
	title[i]="STREET"; i++;
	title[i]="TELEPHONE"; i++;
	title[i]="LAND_TYPE"; i++;
	title[i]="LON"; i++;
	title[i]="LAT"; i++;
	title[i]="PHOTOS"; i++;
	title[i]="ADS_DATE"; i++;
	title[i]="RESTAURANT"; i++;
	title[i]="BANK"; i++;
	title[i]="COFFEESHOP"; i++;
	title[i]="PARK"; i++;
	title[i]="STADIUM"; i++;
	title[i]="SHOPPING"; i++;
	title[i]="SUPERMARKET"; i++;
	title[i]="GYM"; i++;
	title[i]="SCHOOL"; i++;
	title[i]="CINEMA"; i++;
	title[i]="HOSPITAL"; i++;
	title[i]="AIRPORT"; i++;
	title[i]="ZOO"; i++;
	title[i]="ANIMAL_STORE"; i++;
	title[i]="CLOTH_STORE"; i++;
	title[i]="SPA"; i++;
	title[i]="PARKING"; i++;
	title[i]="NIGHT_CLUB"; i++;
	title[i]="ENTERTAINMENT_PARK"; i++;
	title[i]="BAKERY_STORE"; i++;
	title[i]="GROCERIES"; i++;
	title[i]="POST_OFFICE"; i++;
	title[i]="ATM"; i++;
	title[i]="BAR"; i++;
	title[i]="FOR_LEASE"; i++;
	title[i]="FOR_SALE"; i++;
	title[i]="TO_BUY"; i++;
	title[i]="TO_LEASE"; i++;

	max_i=i   
	val["PHOTOS"]=0;
}

# CITY
/id="ContentPlaceHolder2_lbTinhThanh"/{
	c++;
	val["CITY"]=cleanSQL($0);
}

/"near_by_places"/{
	count_restaurant=0;
	count_bank=0;
	count_cafe=0;
	count_park=0;
	count_stadium=0;
	count_shopping_mall=0;
	count_gym=0;
	count_school=0;
	count_movie_theater=0;
	count_hospital=0;
	count_airport=0;
	count_zoo=0;
	count_pet_store=0;
	count_clothing_store=0;
	count_spa=0;
	count_parking=0;
	count_bakery=0;
	count_post_office=0;
	count_amusement_park=0;
	count_grocery_or_supermarket=0;
	count_atm=0;
	count_bar=0;
	count_supermarket=0;
	count_night_club=0;
	count_restaurant=0;
	
	while (match($0, "</div>") == 0){
		getline;
		if (match($0, "ulcl-restaurant") > 0){
			count_restaurant++;
		}
		if (match($0, "ulcl-bank") > 0){
			count_bank++;
		}
		if (match($0, "ulcl-cafe") > 0){
			count_cafe++;
		}
		if (match($0, "ulcl-park") > 0){
			count_park++;
		}
		if (match($0, "ulcl-stadium") > 0){
			count_stadium++;
		}
		if (match($0, "ulcl-shopping_mall") > 0){
			count_shopping_mall++;
		}
		if (match($0, "ulcl-supermarket") > 0){
			count_supermarket++;
		}
		if (match($0, "ulcl-gym") > 0){
			count_gym++;
		}
		if (match($0, "ulcl-school") > 0 || match($0, "ulcl-university") > 0){
			count_school++;
		}
		if (match($0, "ulcl-movie_theater") > 0){
			count_movie_theater++;
		}
		if (match($0, "ulcl-hospital") > 0){
			count_hospital++;
		}
		if (match($0, "ulcl-airport") > 0){
			count_airport++;	
		}
		if (match($0, "ulcl-zoo") > 0){
			count_zoo++;
		}
		if (match($0, "ulcl-pet_store") > 0){
			count_pet_store++;
		}
		if (match($0, "ulcl-clothing_store") > 0){
			count_clothing_store++;
		}
		if (match($0, "ulcl-spa") > 0){
			count_spa++;
		}
		if (match($0, "ulcl-parking") > 0){
			count_parking++;
		}
		if (match($0, "ulcl-night_club") > 0){
			count_night_club++;
		}
		if (match($0, "ulcl-bakery") > 0){
			count_bakery++;
		}
		if (match($0, "ulcl-post_office") > 0){
			count_post_office++;	
		}
		if (match($0, "ulcl-amusement_park") > 0){
			count_amusement_park++;
		}
		if (match($0, "ulcl-grocery_or_supermarket") > 0){
			count_grocery_or_supermarket++;
		}
		if (match($0, "ulcl-atm") > 0){
			count_atm++;
		}
		if (match($0, "ulcl-bar") > 0){
			count_bar++;
		}
	}	
	val["RESTAURANT"]=count_restaurant;
	val["BANK"]=count_bank;
	val["COFFEESHOP"]=count_cafe;
	val["PARK"]=count_park;
	val["STADIUM"]=count_stadium;
	val["SHOPPING"]=count_shopping_mall;
	val["SUPERMARKET"]=count_supermarket;
	val["GYM"]=count_gym;
	val["SCHOOL"]=count_school;
	val["CINEMA"]=count_movie_theater;
	val["HOSPITAL"]=count_hospital;
	val["AIRPORT"]=count_airport;
	val["ZOO"]=count_zoo;
	val["ANIMAL_STORE"]=count_pet_store;
	val["CLOTH_STORE"]=count_clothing_store;
	val["SPA"]=count_spa;
	val["PARKING"]=count_parking;
	val["NIGHT_CLUB"]=count_night_club;
	val["BAKERY_STORE"]=count_bakery;
	val["POST_OFFICE"]=count_post_office;
	val["ENTERTAINMENT_PARK"]=count_amusement_park;
	val["GROCERIES"]=count_grocery_or_supermarket;
	val["ATM"]=count_atm;
	val["BAR"]=count_bar;
}

/id="ContentPlaceHolder2_lbLoaiTin"/{
	temp = cleanSQL($0);
	if (match(temp, "Cho thuê") > 0) {
		val["FOR_LEASE"]="1";
	} 
	if (match(temp, "Cần thuê") > 0)  {
		val["TO_LEASE"]="1";
	} 
	if (match(temp, "Cần bán") > 0) {
		val["FOR_SALE"]="1";
	}
	if (match(temp, "Cần mua") > 0) {
		val["TO_BUY"]="1";
	}
}

/id="ContentPlaceHolder2_viewInfo1_lbHoTen"/{
	getline;
	val["DEALER_NAME"]=cleanSQL($0);
	split($0, ar, "href=\"");
	split(ar[2], arr, "\"");
	val["MINI_SITE"]="https://nhadat24h.net"arr[1];
	sub("/tv/","",arr[1])
	val["DEALER_ID"]=arr[1];
}

/class="popup-gmaps"/ {
	val["DEALER_ADDRESS"]=cleanSQL($0);
}

# DETAILED_BRIEF
/id="li-des"/{
	str="";
	while(match($0, "</div>") == 0){
		temp=cleanSQL($0);
		if(length(temp) > 0){
			str=str", "temp;
		}
		getline;
	}
	sub(", ", "", str);
	val["DETAILED_BRIEF"]=str;
}


# DISTRICT
/id="ContentPlaceHolder2_lbDiaChi"/{
	getline;
	val["DISTRICT"]=cleanSQL($0);
}

# STREET 
/id="ContentPlaceHolder2_lbVitri"/{
	getline;getline;
	val["STREET"]=cleanSQL($0);
}

#DIRECTION
/id="ContentPlaceHolder2_lbHuong"/{
	val["DIRECTION"]=cleanSQL($0);
}

/imageThumb/{
	photo++;
	val["PHOTOS"]=photo;
}

# TELEPHONE
/title="Mobile"/{
	split(cleanSQL($0), arr, "-")
	val["TELEPHONE"]=cleanSQL(arr[1])
}

# LAND_TYPE
/selected="selected"/{
	count++;
	if(count == 1){
		val["LAND_TYPE"]=cleanSQL($0);
	}
}

#LAT
/id="txtLAT"/{
	split($0, arr, "value=")
	split(arr[2], arr1, "\"")
	val["LAT"]=cleanSQL(arr1[2])
}

#LON
/id="txtLON"/{
	split($0, arr, "value=")
	split(arr[2], arr1, "\"")
	val["LON"]=cleanSQL(arr1[2])
}

# <label id="ContentPlaceHolder2_lbDate">Hôm nay, lúc: 13 giờ 57 phút.</label>
# <label id="ContentPlaceHolder2_lbDate">19/11/2018, lúc: 10 giờ 35 phút</label>
/id="ContentPlaceHolder2_lbDate"/{
	temp=cleanSQL($0);
	if(match(temp, "Hôm nay") > 0){
		val["ADS_DATE"]=DATE;
	} else {
		split(temp, ar, ",");
		split(ar[1], arr, "/");
		val["ADS_DATE"]=arr[3]"-"arr[2]"-"arr[1]
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
	printf (" site=\"NHADAT24H\" where site=\"NHADAT24H\" and ID_CLIENT=\"%s\";\n", id)
}



