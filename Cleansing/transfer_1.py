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
parser.add_argument("-f","--from_date", type=str, default="")
parser.add_argument("-e","--end_date", type=str, default="")
parser.add_argument("-t","--test_mode", type=bool, default=False)
args = parser.parse_args()

SITENAME = args.site.lower()
unit = args.unit
from_date = args.from_date
end_date = args.end_date
test_mode = args.test_mode
year = end_date[0:4]
month = end_date[4:6]
source_db = "CLEAN_" + year + "_" + month
if (SITENAME != "") and (SITENAME not in LS_SITE):
    parser.print_help(sys.stderr)
    print()
    print("error: SITE must in list sites and mode must in list modes")
    print("List sites: ",LS_SITE)
    sys.exit(1)

# DECLARES
# Full mode
select_all = True
if (SITENAME != ""):
    select_all = False
# List of functions
def select_data(site,city,from_date,end_date):
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
    if (test_mode):
        source_table = "CLEAN_" + site.upper()
    else:
        source_table = "REAL_CLEAN_" + site.upper()

    sql_s ='SELECT * FROM ' + source_db + '.'+ source_table + '_' + year + '_' + month
    dataframe = spark.sql(sql_s)
    dataframe.createOrReplaceTempView(source_table)
    if (test_mode):
        sql_stm = gen_statement(source_table,'','',from_date,end_date)
    else:
        sql_stm = gen_statement(source_table,'SPLIT_CITY',unit,from_date,end_date)
    df_spark = spark.sql(sql_stm)
    return df_spark
def main():
    # create empty dataframe
    sc = spark.sparkContext
    sqlContext = SQLContext(sc)
    dataframe = spark.sql('SELECT * FROM CLEAN_2021_08.REAL_CLEAN_ALONHADAT_2021_08')
#     dataframe = spark.read.format("jdbc").options(url="jdbc:mysql://172.16.0.167/VN_REAL",\
#         driver = "com.mysql.jdbc.Driver",\
#         dbtable = "REAL_CLEAN_REVERVN",\
#         user="root",\
#         password="123456789").load()
    field = dataframe.schema
    schema = StructType(field)
    data = sqlContext.createDataFrame(sc.emptyRDD(), schema)

    # import all sites
    if (select_all):
        for site in list(set(LS_SITE)):
            new_row = select_data(site,unit,from_date,end_date)
            data = data.union(new_row)
            data = data.dropDuplicates(LS_DUPLICATE)
    # import each site
    else:
        new_row = select_data(SITENAME,unit,from_date,end_date)
        data = data.union(new_row)
        data = data.dropDuplicates(LS_DUPLICATE)

    # save to dataframe
    if (test_mode):
        data.write.format("hive").saveAsTable("REAL_CLEAN_TEST")
        # data.write.format('jdbc').options(
        #     # url="jdbc:mysql://172.16.0.227/VN_REAL_CITY",
        #     # driver='com.mysql.jdbc.Driver',
        #     # dbtable="REAL_CLEAN_TEST",
        #     # user='root',
        #     # password='123456789').mode('append').save()
    else:
        if (unit != ""):
            save_table = unidecode(unit.lower()).strip()
            save_table = re.sub(r'^tinh','',save_table)
            save_table = re.sub(r'^thanh pho','',save_table)
            save_table = source_db + '.REAL_CLEAN_' + save_table.replace(" ","").upper() + '_' + year + '_' + month
        else:
            save_table = source_db + ".REAL_CLEAN_ALL" + '_' + year + '_' + month
            
        data.write.format("hive").saveAsTable(save_table)
if __name__ == "__main__":
    main()