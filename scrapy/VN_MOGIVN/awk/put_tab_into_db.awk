BEGIN { FS="\t" }
{
	id++
	printf ("INSERT IGNORE INTO %s set ",  table)
	for(i=1; i<max_i; i++) {
		if($i != ""){
			gsub("^[ \t]+", "", $i)
			gsub("[ \t]+$", "", $i)
			printf ("%s=\"%s\",", title[i], $i)
		}
	}
	printf ("SITE=\"%s\" ;\n", site )
	# printf ("VO_ANNONCE_ID=\"%s\" ;\n", id )
}
