/id="txtnumketquatimkiem"/ {
	split($0, arr, " ");
	nb=arr[5];
}
END {
	print  "nb_annonces=\""nb"\";"
	}

