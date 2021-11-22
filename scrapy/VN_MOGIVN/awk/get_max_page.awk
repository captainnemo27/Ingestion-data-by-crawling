BEGIN{
    shown_count = 15;total_count = 0;
    max_page=0;
}

#################################
# GET MAX PAGE                  #
#################################
#<div class="property-list-result">
#<span><b>1 - 15</b> trong <b>396</b> kết quả</span>
/class="property-list-result"/{
    getline; getline;
    count=cleanSQL($0);
    split(count,arr_1," trong ");
    gsub(/[^0-9]/,"",arr_1[2]);
    total_count=arr_1[2];
}
END{
    if ( shown_count != 0 ) {
        max_page=int(total_count/shown_count);
        if(int(total_count%shown_count)>0)
            max_page++;
        print max_page;
    }
}