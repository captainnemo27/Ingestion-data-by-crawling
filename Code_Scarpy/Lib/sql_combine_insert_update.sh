#!/bin/bash
# Get insert fil
if [[ $1 != "" ]]; then
  insertSqlFile=$1
else
  echo "Missed input"
  exit
fi
# Get update file
if [[ $2 != "" ]]; then
  updateSqlFile=$2
else
  echo "Missed input"
  exit
fi
# Get the path to save file
if [[ $3 != "" ]]; then
  sqlFile=$3
else
  echo "Missed input"
  exit
fi
if [ ! -s "${insertSqlFile}" ] || [ ! -s "${updateSqlFile}" ]; then
  echo "The ${insertSqlFile} or ${updateSqlFile} is empty!"
  exit
fi
# Exit if the file is not empty
if [ -s "${sqlFile}" ]; then
  echo "The store file is not empty"
  exit
fi

# Loop insertSqlFile
while read -r insertLine
do

  # get Client ID from the insertLine
  clientId=$(echo "${insertLine}" | grep -Eo "ID_CLIENT[\s]*=\"[^\"]+\"" | grep -Eo "\".+\"" | grep -Eo "[^\"]+")

  # If clientId is not empty
  if [ ${#clientId} -ne 0 ]; then

    # Take only 1 line
    updateData=$(grep ID_CLIENT=\"${clientId}\" ${updateSqlFile} | tail -1)

    # if it has data
    if [ ${#updateData} -ne 0 ]; then

      # Remove ";" at the end of the line
      currentInsertLine=$(echo "${insertLine}" | awk '//{gsub(/\s*;$/, ",",$0); print $0;}')

      # Remove update query and where condition
      currentUpdateLine=$(echo ${updateData} | awk '//{
          split($0,arr, /[ ]+set[ ]+|[ ]+SET[ ]+/);
          split(arr[2],arr_1,/[ ]+where[ ]+|[ ]+WHERE[ ]+/);
          print arr_1[1];
        }')

      # Add it to the new file
      echo "${currentInsertLine}${currentUpdateLine} ;" >> "${sqlFile}"

    fi
  fi

done < "${insertSqlFile}"