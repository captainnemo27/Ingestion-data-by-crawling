# Import libraries
import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from time import time
import re
import os
import sys

# Import files
from libs.config import *

#Configure database
path_current = os.getcwd()
path_config = path_current + CONFIG_FOLDER + '/backup_config.txt'

f = open(path_config, 'r')
lines = []
for line in f:
    lines.append(line)
f.close()

mysql_user = lines[0].replace('mysql_user=','').rstrip()
mysql_password = lines[1].replace('mysql_password=','').rstrip()

mysql_inter_tb = "INTER_BACKUP_TABLE"

def main():
    check = sys.argv
    mysql_host = ''
    mysql_db = ''
    site_tb = ''
    backup_tb = ''

    if (len(check) != 5):
        print("Format input example: python3 cleaning_backup.py host=172.16.0.227 db=REAL_ESTATE_VN site=PROPZYVN backup=RAW_DATA")
        return

    for i in range(1,len(check)):
        if (re.search("host",check[i])):
            mysql_host = check[i].split("=")[1]
        elif (re.search("db",check[i])):
            mysql_db = check[i].split("=")[1]
        elif (re.search("site",check[i])):
            site_tb = check[i].split("=")[1]
        elif (re.search("backup",check[i])):
            backup_tb = check[i].split("=")[1]

    print("mysql_host=",mysql_host)
    print("mysql_db=",mysql_db)
    print("site_tb=",site_tb)
    print("backup_tb=",backup_tb)
    
    if (mysql_host == '' or mysql_db == '' or site_tb == '' or backup_tb == ''):
        print("Format input example: python3 cleaning_backup.py host=172.16.0.227 db=REAL_ESTATE_VN site=PROPZYVN backup=RAW_DATA")
        return

    try:
        db_connection = sqlalchemy.create_engine("mysql://{}:{}@{}/{}?charset=utf8mb4".format(mysql_user,mysql_password,mysql_host,mysql_db))
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    else:
        print("Connect database successfully") 

    # Update PRO_FLAG = 15 to avoid conflict when importing 
    try:
        sql = "UPDATE " + site_tb + " SET PRO_FLAG = 15 WHERE PRO_FLAG = 12"
        with db_connection.begin() as conn:
            conn.execute(sql)
        conn.close()
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    else:
        print("Set PRO_FLAG = 15 successfully")

    # Create RAW_DATA_COPY empty
    try:
        sql_drop_exists = "DROP TABLE IF EXISTS " + mysql_inter_tb
        sql_create = "CREATE TABLE " + mysql_inter_tb + " AS (SELECT * FROM " + backup_tb + " WHERE 1=2)"
        with db_connection.begin() as conn:
            conn.execute(sql_drop_exists)
            conn.execute(sql_create)
        conn.close()
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    else:
        print("Create INTER_BACKUP_TABLE successfully")
    
    start = time()

    # Set chunk file
    limit = 5000
    i = 0
    count = 0

    while True:
        count = count + 1
        
        df = pd.read_sql('SELECT * FROM '+ site_tb + " WHERE PRO_FLAG=15 limit " + str(limit) + " offset " + str(i), con=db_connection)

        # if (count == 3):
        #     break

        # Stopping Condition
        if df.empty == True:            
            print("Read all database")
            break        
        print(i)       

        i = i + limit
        # df.head()
        print(df.shape)

        # Move to RAW_DATA
        try:
            df.to_sql(mysql_inter_tb, db_connection, if_exists='append',index=False)
        except ValueError as vx:
            print(vx)
            return
        except Exception as ex:   
            print(ex)
            return
        else:
            print("Table %s inserted successfully."%mysql_inter_tb)  

    # Copy to RAW_DATA
    try:
        sql_copy = "INSERT INTO " + backup_tb + " SELECT * FROM " + mysql_inter_tb + " WHERE 1 = 1"
        with db_connection.begin() as conn:
            conn.execute(sql_copy)
        conn.close()
    except ValueError as vx:
        print(vx)
    except Exception as ex:   
        print(ex)
    else:
        print("Insert data to backup table successfully")

        # Delete from site_name where PRO_FLAG = 15
        try:
            sql_delete = "DELETE FROM " + site_tb + " WHERE PRO_FLAG = 15"
            sql_drop = "DROP TABLE " + mysql_inter_tb
            with db_connection.begin() as conn:
                conn.execute(sql_delete)
                conn.execute(sql_drop)
            conn.close()
        except ValueError as vx:
            print(vx)
        except Exception as ex:   
            print(ex)
        else:
            print("Delete data cleaning successfully")
            print("Drop INTER_BACKUP_TABLE successfully")    

    finish = time()

    # Print total time
    print ("DONE")
    print ("Total time = " + str(round(((finish - start)/60),5)) + " mins")
   
if __name__ == "__main__":
    main()