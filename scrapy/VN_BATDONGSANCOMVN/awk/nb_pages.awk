BEGIN {
    nb_pages=1
}

/class="pagination"|class="re__pagination-group"/ {
    max_loop=25
    loop=0
    do {
        if ($0 ~ /pid=/) {
            split($0, arr, "pid=\"")
            split(arr[2], arr_1, "\"")
            if(arr_1[1] > nb_pages){
                nb_pages=arr_1[1]
            }
        }
        getline
        loop++
    } while(loop < max_loop)
    exit
}
END {
    print nb_pages
}
