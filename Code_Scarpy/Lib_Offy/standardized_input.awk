# This file supports to standardized input text 
# Avoiding one line has more two tags script
# ex: standard syntax
#	awk -f standardized_input.awk $list_file/${fn} > tmp.txt #standardized input text 
#	awk NF tmp.txt > input.txt #remove multi break new line
{
	gsub(">",">\n",$0);
	gsub("<","\n<",$0);		
	print $0;
}
