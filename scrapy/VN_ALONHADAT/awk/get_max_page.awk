BEGIN {
    max_page=0;
}
/div class="page"/{
    do {
        getline
        #print($0)
        if(match($0,"href='/")){
            temp=$0
        }
    } while (match($0,"class=\"recommend-properties\"")==0)
    #print(temp)
    max_page=int(removeHtml(temp))
}
END {
    printf("%.0f\n", max_page);
}