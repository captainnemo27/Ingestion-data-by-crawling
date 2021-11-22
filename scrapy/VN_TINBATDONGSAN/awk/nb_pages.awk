BEGIN {
    nb_pages=1
    i=0
}
/class='style-pager-button-next-first-last'/ {
    if (i == 0) {
        getline; getline; getline; getline

        split($0, arr, "title=\'")
        split(arr[2], arr_1, "\'>")
        gsub(/P/,"",arr_1[1])
        nb_pages=trim(arr_1[1])
    }
    i++
}
END {
    print nb_pages
}
