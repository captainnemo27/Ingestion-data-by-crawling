#!/bin/bash
set -x
hostname=$(hostname -s)
workDir=$(pwd)

# Back-up daily
if [ "X${1}" = "X" ]
then
        date=`date +"%Y%m%d" -d"1 days ago"`
else
        date=$1
        shift
fi

echo "Starting zip $date folder"
function compress() {
  local movedMark=""
  local statusOK=""
  local tarDateFile=""
  local backUpDir=""


  # Get all folders that have to compress
  for folder in "${workDir}"/*/"${date}"
  do
    [[ -e "${folder}" ]] || break  # handle the case of no folder
    siteName=$(echo "${folder}" | awk -F'\/' '{print $(NF-1)}')
    #projectName=$(echo "${folder}" | awk -F'\/' '{print $(NF-2)}')
    projectName="REAL_ESTATE_VN"
    cd "${workDir}/${siteName}" || exit
    movedMark="${workDir}/${siteName}/${date}/moved_mark"
    statusOK="${workDir}/${siteName}/${date}/DELTA/status_ok"
    tarDateFile="${siteName}_${projectName}_${hostname}_${date}.tgz"
    # If the mark file is empty and the statusOK file is not empty
    if [ ! -s "${movedMark}" ] && [ -s "${statusOK}"* ]; then
      # look for empty siteName directory
      if [ "$(ls -A "${date}")" ] && [ ! -s "${tarDateFile}" ]; then
        # The date folder is not empty and the tar file is empty.
        # Check logs
        if ! ls "log_${date}"* > /dev/null 2>&1
        then
          echo "NO LOGS" > log_"${date}"
        fi
        # Compress it
        if tar -zcf "${tarDateFile}" "${date}" 
        then
          # Tar successfully
          mkdir "${date}.NEW" # Create the folder that they are never deleted.
          cp -a "${date}/DELTA" "${date}.NEW" # Backup DELTA folder
          mv "${date}" "DELETE.${siteName}.${projectName}.${date}"
          mv "${date}.NEW" "${date}"
          rm -rf "DELETE.${siteName}.${projectName}.${date}" &
          rm -f log_"${date}"* &
        fi
      fi
      # Move files to backUpDir
      ## Define backUpDir
      if [ $hostname == "autobiz" ]; then
          # Server 184
          backUpDir="/mnt/backup_autobiz_data/${projectName}/${siteName}"
      else
          backUpDir="/home/itdev/backup_autobiz_data/${projectName}/${siteName}"
      fi
      if [ ! -d "${backUpDir}" ]; then
        mkdir -p "${backUpDir}"
      fi
      if [ ! -s "${backUpDir}/${tarDateFile}" ]; then
        mv "${tarDateFile}" "${backUpDir}"
      fi

      echo "ok" > "${movedMark}"
    fi
  done
}
compress 

echo "DONE BACK-UP !"