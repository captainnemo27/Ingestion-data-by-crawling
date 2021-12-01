import findspark
findspark.init()

import pyspark # only run after findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
spark = SparkSession.builder \
    .master('spark://172.12.0.2:7077') \
    .config("spark.driver.memory", "6g")\
    .config('spark.cores.max', '4')\
    .appName('myapp1') \
    .enableHiveSupport() \
    .getOrCreate()

import os
import sys
import importlib
import argparse

from libs.or_utils_ import *
from libs.or_prep_ import *

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("-s","--site", type=str, default="")
parser.add_argument("-u","--unit", type=str, default="")
parser.add_argument("-sdb","--source_db", type=str, default="")
parser.add_argument("-ddb","--des_db", type=str, default="")
parser.add_argument("-stb","--source_tb", type=str, default="")
parser.add_argument("-dtb","--des_tb", type=str, default="")
parser.add_argument("-ss","--source_server", type=str, default="")
parser.add_argument("-ds","--des_server", type=str, default="")
parser.add_argument("-f","--from_date", type=str, default="")
parser.add_argument("-e","--end_date", type=str, default="")
parser.add_argument("-m","--mode", type=str, default="")
args = parser.parse_args()

SITENAME = args.site.lower()
unit = args.unit
source_db = args.source_db
des_db = args.des_db
source_tb = args.source_tb
des_tb = args.des_tb
source_server = args.source_server
des_server = args.des_server
from_date = args.from_date
end_date = args.end_date
mode = args.mode
year = end_date[0:4]
from_month = int(from_date[4:6])
end_month = int(end_date[4:6])
ls_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
LS_MONTH = ls_month[from_month-1:end_month:1]
#LS_MONTH = ls_month[6:end_month:1]
ls_mode = ["","test","append"]
if (unit != ""):
        UNIT = unidecode(unit.lower()).strip()
        UNIT  = re.sub(r'^tinh','',UNIT)
        UNIT  = re.sub(r'^thanh pho','',UNIT)
        UNIT  = UNIT .replace(" ","").upper()

# if (SITENAME != "") and (SITENAME not in LS_SITE):
#     parser.print_help(sys.stderr)
#     print()
#     print("error: SITE must in list sites")
#     print("List sites: ",LS_SITE)
#     sys.exit(1)

# if (mode not in ls_mode):
#     parser.print_help(sys.stderr)
#     print()
#     print("error: mode must in list modes")
#     print("List mode: ",ls_mode)
#     sys.exit(1)

# if (source_db == "") or (des_db == "") or (source_tb == "") or (des_tb == "") or (source_server == "") or (des_server == ""):
#     parser.print_help(sys.stderr)
#     print()
#     print("error: db, table and server must not empty")
#     sys.exit(1)

# DECLARES
# Full mode
select_all = True
if (SITENAME != ""):
    select_all = False

# List of functions
# DECLARES
# Full mode
select_all = True
if (SITENAME != ""):
    select_all = False

# List of functions
def select_data(month,city,from_date,end_date):
    '''
        Select data from dataframe 

            Parameters:
                site (str): site name
                city (str): city name
                from_date (str): date begin. Ex: 20210401
                end_date (str): date end. Ex: 20210401

            Returns:
                s (str): list of string from flat dataframe
    '''
    if (mode == "test"):
        source_table = "CLEAN_" + UNIT + '_' + year + '_' + month
    else: 
        source_table = "REAL_CLEAN_" + UNIT + '_' + year + '_' + month
    # if (site in LS_167):
    #     server = 167
    # if (site in LS_227):
    #     server = 227
    # dataframe = spark.read.format("jdbc").options(url="jdbc:mysql://172.16.0."+str(server)+"/VN_REAL",\
    #     driver = "com.mysql.jdbc.Driver",\
    #     dbtable = source_table,\
    #     user="root",\
    #     password="123456789").load()
    sql_s ='SELECT * FROM ' + 'clean' + '_' + year + '_' + month + '.'+ source_table 
    dataframe = spark.sql(sql_s)
    dataframe.createOrReplaceTempView(source_table)
    if (mode == "test"):
        sql_stm = gen_statement(source_table,'','',from_date,end_date)
    else:
        sql_stm = gen_statement(source_table,'SPLIT_CITY',unit,from_date,end_date)
    df_spark = spark.sql(sql_stm)
    return df_spark

def main():
    if (unit != ""):
            save_table = unidecode(unit.lower()).strip()
            save_table = re.sub(r'^tinh','',save_table)
            save_table = re.sub(r'^thanh pho','',save_table)
            save_table = 'REAL_CLEAN_' + save_table.replace(" ","").upper() + '_' + year
    else:
            save_table = "REAL_CLEAN_ALL" + '_' + year + '_' + month
    # create dataframe
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    dataframe = spark.sql('SELECT * FROM CLEAN_2021_08.REAL_CLEAN_ALONHADAT_2021_08')
    dataframe.createOrReplaceTempView(save_table)
    if (mode == "append"):
        data = spark.sql("SELECT * FROM " + save_table)
    else:
        data = sqlContext.createDataFrame(sc.emptyRDD(), StructType(dataframe.schema))

    # import all sites
    if (select_all):
        for month in list(set(LS_MONTH)):
            new_row = select_data(month,unit,from_date,end_date)
            data = data.union(new_row)
            data = data.dropDuplicates(LS_DUPLICATE)
    # import each site
    else:
        new_row = select_data(SITENAME,unit,from_date,end_date)
        data = data.union(new_row)
        data = data.dropDuplicates(LS_DUPLICATE)
    data.write.format("hive").saveAsTable(save_table)
    
if __name__ == "__main__":
    main()
