/LoadPagging/ {
	dem++
	if(dem==1){	
		split($0, arr, ", ");
		nb=arr[2];
	}
}
END {
	print  "nb_pages=\""nb"\";"
}

