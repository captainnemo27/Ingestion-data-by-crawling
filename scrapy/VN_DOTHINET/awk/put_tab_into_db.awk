BEGIN {
    FS="\t" 
}

{
    if ( $0 == "" ){ next }
    gsub("\"", " ", $0)
    gsub("\\\\", " ", $0) # \\\\ means \
    #gsub("\\\\\\\\\"", "\\\"", $0)

    printf ("INSERT IGNORE INTO %s set ",  table)
    for(i=1; i<=max_i; i++) {
        gsub("^[ \t]+", "", $i)
        gsub("[ \t]+$", "", $i)
        if ( $i != "" ) {
            printf ("%s=\"%s\",", title[i], $i);
        }
    }
    printf (" site=\"%s\";\n", site)
}
