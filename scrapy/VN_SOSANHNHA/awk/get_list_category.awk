BEGIN {
    col=1;
	title[col]="NUMBER"; col++
	title[col]="CATEGORY"; col++
    max_col=col
	row=0
}

/class="form-control select_2" name="iCat"/{
    getline
    do {
        getline;
        if (match($0,"</select>")==0){
            row++
            split($0,ar,"value=\"")
            split(ar[2],arr,"\">")
            value[row,"NUMBER"]=arr[1]
            value[row,"CATEGORY"]=removeHtml($0)
        }
    } while (match($0, "</select>")==0);
    
}

END	{
	max_row = row
	for(row = 1; row <= max_row; row++){
		#print(row)
		for(col = 1; col <= max_col; col++){
			printf("%s\t", value[row, title[col]])	
		}
		printf("\n")
	}
}