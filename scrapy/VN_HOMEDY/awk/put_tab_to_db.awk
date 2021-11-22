BEGIN {
    FS="\t" 
	col=1;
	title[col]="ID_CLIENT"; col++
	title[col]="ADS_LINK"; col++
    title[col]="ADS_TITLE"; col++
    title[col]="FOR_LEASE"; col++
    title[col]="FOR_SALE"; col++
    title[col]="PRICE"; col++
    title[col]="PRICE_UNIT"; col++
    title[col]="PRICE_ORIGINAL"; col++
	title[col]="SURFACE"; col++
    title[col]="SURFACE_UNIT"; col++
    title[col]="SURFACE_ORIGINAL"; col++
    title[col]="FULL_ADDRESS"; col++
    title[col]="TYPE"; col++
    title[col]="CREATED_DATE"; col++
    title[col]="DATE_ORIGINAL"; col++
	max_col=col
	row=0
}
{
    if ( $0 == "" ){ next }
    #gsub("\"", "\\\"", $0)
    gsub("\"", " ", $0)
    gsub("\\\\", " ", $0) # \\\\ means \
    #gsub("\\\\\\\\\"", "\\\"", $0)

    printf ("INSERT IGNORE INTO %s set ",  table)
    for(i=1; i<=max_col; i++) {
        gsub("^[ \t]+", "", $i)
        gsub("[ \t]+$", "", $i)
        if ( $i != "" ) {
            printf ("%s=\"%s\",", title[i], $i);
        }
    }
    printf (" site=\"homedy\";\n")
}
