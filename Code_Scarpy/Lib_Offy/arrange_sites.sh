####################################
# ARRANGEMENT ALL FILES BACKUP     #
# Run this script on server Backup #
####################################

# Get list folder
for site in `ls -R | sort | grep ".tgz" `
do
	# get name site from DK_BILBASEN_ALL_20161101.tgz
	name=`echo $site| awk '{
				 	split($0,arr,"_");
					 printf("%s",arr[1]"_"arr[2]);
				}'`;
	
	 echo $name >> list_folder;
done

# remove duplicate line
awk '!seen[$0]++' list_folder >  folders.txt


# make folder for each site 
for name in `cat folders.txt`
do 
       if [ ! -d $name ] # Don't exist folder (which contains zip files)
        then
          	mkdir $name # create folder
        fi 

   	mv "$name"_*.tgz  $name
done

# remove tempory file 
rm -rf folders.txt list_folder
