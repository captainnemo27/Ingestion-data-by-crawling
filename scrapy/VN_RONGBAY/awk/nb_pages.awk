#<div class="breackcum_bds ">
#                            <h1 class="no1_title roboto_bold">Mua Bán nhà đất - mua bán tại  Hà Nội</h1>                <p class="no2_title">Có 19.186 tin tại <span id="chooseCityPhone" class="cl_2570a8 roboto_bold font_13">Hà Nội</span></p>

BEGIN {
    nb_ads=0
}

/class="no2_title"/ {
	getline;
    temp = cleanSQL($0)
	gsub(/[^0-9]/, "", temp)
    nb_ads = int(temp/57) + 1
}

END {
    print nb_ads
}
