/id="txt_total_records"/{
	split($0,ar,"value=\"")
	split(ar[2],ar,"\"")
	print int(ar[1])
}
