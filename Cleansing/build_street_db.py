import pyspark # only run after findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark.sql.functions import *
spark = SparkSession.builder.master('local[*]')\
    .config("spark.driver.memory", "10g")\
    .appName('my-cool-app').getOrCreate()

import os
import sys
import importlib
import argparse
from datetime import datetime

from libs.or_utils_ import *
from libs.or_prep_ import *

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("-t","--table", type=str, default="")
parser.add_argument("-init","--init", type=bool, default=False)
parser.add_argument("-f","--from_date", type=str, default="")
parser.add_argument("-e","--end_date", type=str, default="")
args = parser.parse_args()

table = args.table
init = args.init
from_date = args.from_date
end_date = args.end_date

# RENAME
if (table == "" and init == False):
    parser.print_help(sys.stderr)
    print()
    print("error: table format VN_REAL_CLEAN_YYYY_MM or VN_REAL")
    sys.exit(1)

if (table == "VN_REAL"):
    val = "07_2021"
    ls_site_167 = LS_167_OLD
    ls_site_227 = LS_227_OLD
else:    
    ar = table.split('_')
    month = ar[len(ar)-1]
    year = ar[len(ar)-2]
    val = month+"_"+year
    ls_site_167 = LS_167
    ls_site_227 = LS_227

source_mysql_db = table

# List of functions
def print_city(city_prefix,city_val):
    city = DIC_PREFIX[city_prefix] + " " + str(city_val)
    city = " ".join(city.split())
    return city

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
    source_table = "REAL_CLEAN_" + site.upper()
    if (site in ls_site_167):
        server = 167
    if (site in ls_site_227):
        server = 227
    dataframe = spark.read.format("jdbc").options(url="jdbc:mysql://172.16.0."+str(server)+"/"+source_mysql_db,\
        driver = "com.mysql.jdbc.Driver",\
        dbtable = source_table,\
        user="root",\
        password="123456789").load()
    dataframe.createOrReplaceTempView(source_table)
    sql_stm = gen_statement_address(source_table,'','',from_date,end_date)
    df_spark = spark.sql(sql_stm)
    return df_spark

def main():
    if (init):
        df = pd.read_csv("json/data_vn_tinh_duong.csv",sep=";")
        df['CITY'] = df.apply(lambda x:print_city(x['city_prefix'],x['city_val']),axis=1)
        df['DISTRICT'] = df.apply(lambda x:print_city(x['district_prefix'],x['district_val']),axis=1)
        df['WARD'] = None
        df['STREET'] = df.apply(lambda x:print_city(x['street_prefix'],x['street_val']),axis=1)
        df['MONTH'] = "_"

        for col in df.columns:
            df[col] = df[col].astype(str)

        df = df[['CITY','DISTRICT','WARD','STREET','MONTH']]
        data=spark.createDataFrame(df)

    else:
        # create empty dataframe
        sc = spark.sparkContext
        sqlContext = SQLContext(sc)
        dataframe = spark.read.format("jdbc").options(url="jdbc:mysql://172.16.0.167/"+source_mysql_db,\
            driver = "com.mysql.jdbc.Driver",\
            dbtable = "REAL_CLEAN_REVERVN",\
            user="root",\
            password="123456789").load()
        field = dataframe.schema
        schema = StructType(field)
        data = sqlContext.createDataFrame(sc.emptyRDD(), schema)
        data = data.select(["SPLIT_CITY","SPLIT_DISTRICT","SPLIT_WARD","FORMAT_STREET"])

        # import all sites
        for site in list(set(LS_SITE)):
            new_row = select_data(site,"",from_date,end_date)
            data = data.union(new_row)
            data = data.dropDuplicates(["SPLIT_CITY","SPLIT_DISTRICT","SPLIT_WARD","FORMAT_STREET"])
        
        data = data.withColumn("MONTH", lit(val))
        data = data.withColumnRenamed("SPLIT_CITY","CITY") \
            .withColumnRenamed("SPLIT_DISTRICT","DISTRICT") \
            .withColumnRenamed("SPLIT_WARD","WARD") \
            .withColumnRenamed("FORMAT_STREET","STREET") \

    data.write.format('jdbc').options(
        url="jdbc:mysql://172.16.0.227/REAL_ESTATE_VN",
        driver='com.mysql.jdbc.Driver',
        dbtable="STREET_DB",
        user='root',
        password='123456789').mode('append').save()

if __name__ == "__main__":
    main()