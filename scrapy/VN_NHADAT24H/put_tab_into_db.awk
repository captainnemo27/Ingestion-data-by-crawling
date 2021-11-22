BEGIN {
    FS="\t" 
}

{
    if ( $0 == "" ){ next }
    gsub("\"", " ", $0)
    gsub("\\", " ", $0)

    printf ("INSERT IGNORE INTO %s set ",  table)
    for(i=1; i<max_i; i++) {
        gsub("^[ \t]+", "", $i)
        gsub("[ \t]+$", "", $i)
	if(length(trim($i)) > 0){
	        printf ("%s=\"%s\",", title[i], $i)
	}
    }
    printf (" site=\"NHADAT24H\", CREATED_DATE=\"%s\" ;\n", DATE );
}
