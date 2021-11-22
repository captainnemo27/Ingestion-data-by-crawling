BEGIN {
    nb_pages=1
    i=0
}

/class="pager"/ {
    getline; getline; getline; getline
    if (i == 0 && $0 ~ /LoadPagging/ ) {
        split($0, arr, "LoadPagging")
        split(arr[2], arr_1, ",")
        nb_pages=trim(arr_1[2])
    }
    i++
}
END {
    print nb_pages
}
