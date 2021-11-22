BEGIN {
    nb_pages=0
}
/webparttitlecount/{
    getline 
    temp = cleanSQL($0)
    gsub(/[^0-9]/,"",temp)
    nb_pages=int(temp/25) + 1
}
END {
    print nb_pages
}
