#!/bin/bash

# mysql -h 172.16.0.167 -u root -p123456789 VN_REAL_CLEAN_2021_11 -e "show tables"

mysql -h $1 -u root -p123456789 << EOF
GRANT ALL PRIVILEGES ON $2.* TO openreal@'%';
EOF

echo "Done script"