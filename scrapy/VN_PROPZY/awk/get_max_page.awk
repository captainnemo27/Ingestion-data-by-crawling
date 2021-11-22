BEGIN {
	total_count = 0;
    max_page=0;
    ads_page=12;
}
/class="p-number"/{
    split($0, ar, "class=\"p-number\"")
    split(ar[2],arr,"</strong>")
    gsub(/[^0-9]/,"",arr[1])
    total_count=arr[1]
    max_page=int(total_count/ads_page) + 1
}
END {
    printf("%.0f\n", max_page);
}