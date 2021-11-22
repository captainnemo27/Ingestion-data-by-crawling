BEGIN	{
	col=1;
	title[col]="ID_CLIENT"; col++
	title[col]="ADS_LINK"; col++
	title[col]="TYPE"; col++
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
	title[col]="CITY"; col++
	title[col]="PRICE_ORIGINAL"; col++
	title[col]="SURFACE_ORIGINAL"; col++

	max_col=col
	row=0
	count=0
	max_count = 50
}

#</div> <div class="col-md-3 col-padding"> <div class="item-listing listing-card view-as-grid item-compare "  
# data-listingtypeid="1" data-id="367260"  
# data-img="https://cdn.propzy.vn/listing/thumbnail/map/2021/05/17/listing_f2e36706854141cb8bf0d1353963f599df735f5504740ee99e67068c35d1f80a.jpg" 
# data-price="4,3 tỷ"  data-address="Đ. Xa Lộ Hà Nội, P.Thảo Điền, Q.2" 
# data-bathroom="2" data-bedroom="2" data-size="63.1 m²" data-projectname="Masteri An Phú" 
# data-projectlink="/du-an/hcm/quan-2/masteri-an-phu-id163" > <div class="bl-img"> <div class="owl-carousel owl-theme s-dots"> 
# <a href="/mua/can-ho/hcm/quan-2/id367260" class="img"> <img itemprop="image" class="owl-item active" 
# src="https://cdn.propzy.vn/listing/thumbnail/map/2021/05/17/listing_f2e36706854141cb8bf0d1353963f599df735f5504740ee99e67068c35d1f80a.jpg" alt="Bán căn hộ cao cấp Masteri An Phú 2 phòng ngủ, đầy đủ nội thất. - Hướng Đông Bắc." 
# onerror="this.src='/assets/images/Property_Default.jpg'"> </a> <a href="/mua/can-ho/hcm/quan-2/id367260" class="img"> 
# <img itemprop="image" class="owl-item " src="https://cdn.propzy.vn/listing/thumbnail/map/2021/05/17/listing_e0f2a129035049f3bfb606214460b37b7855cee31f50cc2d084380695513fbee.jpg" alt="Bán căn hộ cao cấp Masteri An Phú 2 phòng ngủ, đầy đủ nội thất. - Hướng Đông Bắc." onerror="this.src='/assets/images/Property_Default.jpg'"> </a> 
# <a href="/mua/can-ho/hcm/quan-2/id367260" class="img"> <img itemprop="image" class="owl-item " src="https://cdn.propzy.vn/listing/thumbnail/map/2021/05/17/listing_3d8644a646317429d76d868a30db76f35fdb0b099a7048b76dc40779f062c017.jpg" alt="Bán căn hộ cao cấp Masteri An Phú 2 phòng ngủ, đầy đủ nội thất. - Hướng Đông Bắc." onerror="this.src='/assets/images/Property_Default.jpg'"> 
# </a> <a href="/mua/can-ho/hcm/quan-2/id367260" class="img"> <img itemprop="image" class="owl-item " src="https://cdn.propzy.vn/listing/thumbnail/map/2021/05/17/listing_98aa4f70fc15cf85cfa72eb9c6c96778d80fba3781d73387f43912d82d671f0c.jpg" alt="Bán căn hộ cao cấp Masteri An Phú 2 phòng ngủ, đầy đủ nội thất. - Hướng Đông Bắc." onerror="this.src='/assets/images/Property_Default.jpg'"> 
# </a> <a href="/mua/can-ho/hcm/quan-2/id367260" class="img"> <img itemprop="image" class="owl-item " src="https://cdn.propzy.vn/listing/thumbnail/map/2021/05/17/listing_0795c50e10aee9d910dec6987fab70947a7bcb347434a71c55d3ac6dd17c2dfc.jpg" alt="Bán căn hộ cao cấp Masteri An Phú 2 phòng ngủ, đầy đủ nội thất. - Hướng Đông Bắc." onerror="this.src='/assets/images/Property_Default.jpg'"> </a> </div> 
# <div class="bl-floating-img"> <span class="span-liked"> <i link="/mua/can-ho/hcm/quan-2/id367260"  
# listingid="367260"  object='{"id":367260 }'  class="ic ic-like  save-listing save-listing-367260">
/item-listing listing-card/{
	row++
	photos = 0
	split($0,ar,"<i link=\"")
	split(ar[2],arr,"\"")
	if (arr[1]!=""){
		value[row, "ADS_LINK"] = "https://propzy.vn/"arr[1]
	}
	split(arr[1],arrr,"/")
	value[row, "TYPE"] = arrr[2]
	value[row, "LAND_TYPE"] = arrr[3]
	value[row, "CITY"] = arrr[4]
	gsub("id","",arrr[length(arrr)])
	value[row, "ID_CLIENT"] = arrr[length(arrr)]

	split($0,ar1,"data-price=\"")
	split(ar1[2],arr1,"\"")
	pr = cleanSQL(removeHtml(arr1[1]))
	if (match(pr,/[0-9]+/)){
		# value[row,"PRICE"]=pr
		value[row,"PRICE_ORIGINAL"]=pr
	}
	

	split($0,ar2,"data-size=\"")
	split(ar2[2],arr2,"\"")
	sf = cleanSQL(removeHtml(arr2[1]))
	value[row,"SURFACE_ORIGINAL"]=sf
	# if (match(sf,"m")){
	# 	split(sf,sf1," ")
	# 	value[row, "SURFACE"] = sf1[1]
	# 	value[row, "SURFACE_UNIT"] = sf1[2]
	# }

	split($0,ar3,"data-address=\"")
	split(ar3[2],arr3,"\"")
	value[row, "FULL_ADDRESS"] = cleanSQL(removeHtml(arr3[1]))

	split($0,ar4,"data-bathroom=\"")
	split(ar4[2],arr4,"\"")
	bath = cleanSQL(removeHtml(arr4[1]))
	if (!match(bath,"--")){
		value[row, "BATHROOM"] = bath
	}
	
	split($0,ar5,"data-bedroom=\"")
	split(ar5[2],arr5,"\"")
	bed = cleanSQL(removeHtml(arr5[1]))
	if (!match(bed,"--")){
		value[row, "BEDROOM"] = bed
	}
	
	split($0,ar6," data-projectname=\"")
	split(ar6[2],arr6,"\"")
	project = cleanSQL(removeHtml(arr6[1]))
	if (!match(project,"--")){
		value[row, "PROJECT_NAME"] = project
	}
	
	do {
		getline
		count++
		if (match($0,"p-info-listing")){
			split($0,t,"p-info-listing\">")
			value[row, "ADS_TITLE"] = cleanSQL(removeHtml(t[2]))
			break
		}
	} while ((!match($0,"class=\"bl-info-listing\"")) && (count<=max_count))
}

/class="ic ic-compass"/{
	getline
	split($0,ar,"</span>")
	value[row, "PRO_DIRECTION"] = cleanSQL(removeHtml(ar[1]))
	if (value[row, "PRO_DIRECTION"] == "--"){
		value[row, "PRO_DIRECTION"] = ""
	}
}

/class="breadcrumbs"/{
	split($0,ar,"class=\"item\">")
	split(ar[2],arr,"</span>")
	type = cleanSQL(arr[1])
}

END	{
	max_row = row
	for(row = 1; row <=  max_row; row++){
		if (value[row, "ID_CLIENT"] !=""){
			for(col = 1; col < max_col; col++){
				printf("%s\t", value[row, title[col]])
			}
			print("\n")
		}
	}
}