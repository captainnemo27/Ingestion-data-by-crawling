from datetime import datetime
import argparse
import sys
import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()

# Requirements
#$ pip3 install -r requirements.txt
# HOW TO USE
# python3 gen_script_db.py -m MODE -s SERVER -d DATE
### MODE: crawl for REAL_ESTATE_VN, clean for VN_REAL
### SERVER: 172.16.0.167
### DATE: format YYYYMMDD, if null is today
# EXAMPLE
# gen script for crawl db on server 167 in August 
#$ gen_script.py -m crawl -s 172.16.0.167 -d 20210801
# gen script for clean db on server 167 in August
#$ gen_script.py -m clean -s 172.16.0.167 -d 20210801

# DELARES
LS_TABLE = ["dothinet","batdongsancomvn","diaoconline","homedy","mogivn",\
      "nhachotot","nhadatcafeland","propzyvn","revervn",\
      "sosanhnha","tinbatdongsan","batdongsan","youhomes","alonhadat","rongbay"]
LS_CRAWL_TABLE = [x.upper() for x in LS_TABLE]
LS_CLEAN_TABLE = ["REAL_CLEAN_" + x.upper() for x in LS_TABLE]

today = datetime.today().strftime('%Y%m%d')

ls_mode = ["crawl","clean"]

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("-m","--mode", type=str, default="")
parser.add_argument("-s","--server", type=str, default="")
parser.add_argument("-d","--date", type=str, default="")
args = parser.parse_args()

mode = args.mode
server = args.server
date = args.date

if mode not in ls_mode:
  parser.print_help(sys.stderr)
  print()
  print("error: mode must in list modes and server must in list servers")
  print("List modes: ",ls_mode)
  sys.exit(1)

if (date == ""):
  date = today

month = date[4:6]
year = date[0:4]
crawl_db = "VN_REAL_RAW" + "_" + year + "_" + month
clean_db = "VN_REAL_CLEAN" + "_" + year + "_" + month
crawl_script = "crawl.sql"
clean_script = "clean.sql"

if (mode == "crawl"):
  db = crawl_db
  script = crawl_script
  ls_table = LS_CRAWL_TABLE
  rp = 'CRAWL_TABLE_NAME'
elif (mode == "clean"):
  db = clean_db
  script = clean_script
  ls_table = LS_CLEAN_TABLE
  rp = 'CLEAN_TABLE_NAME'

def main():
  # CONNECT SERVER
  db_connection = sqlalchemy.create_engine("mysql://{}:{}@{}".format("root","123456789",server))
  print("Connect server " + server + " successfully")

  # CREATE DATABASE
  try:
    create_db_sql = "CREATE DATABASE IF NOT EXISTS " + db + " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    use_db_sql = "USE " + db
    with db_connection.begin() as conn:
      conn.execute(create_db_sql)
      conn.execute(use_db_sql)
    conn.close()
  except Exception as ex:
    print(ex)
    return
  else:
    print("Create database " + db + " successfully")

  # CREATE TABLES
  for table in ls_table:
    try:
      create_table_sql = open(script).read().replace(rp,table)
      with db_connection.begin() as conn:
        conn.execute(create_table_sql)
      conn.close()
    except Exception as ex:
      print(ex)
      return
    else:
      print("Create table " + table + " successfully")

if __name__ == "__main__":
    main()