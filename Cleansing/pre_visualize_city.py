import findspark
findspark.init()

import pyspark # only run after findspark.init()
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
from functools import reduce
from pyspark.sql import DataFrame

spark = SparkSession.builder.master('local[*]')\
    .config("spark.driver.memory", "10g")\
        .appName('my-cool-app').getOrCreate()

from tabulate import tabulate
import os
import sys
import importlib
import argparse
from datetime import date

from libs.or_prep_ import *

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("-u","--unit", type=str, default="")
parser.add_argument("-w","--write", type=str, default="csv")
args = parser.parse_args()

city = args.unit
write = args.write

city = re.sub(r'^Tỉnh','',city).strip()
city = re.sub(r'^Thành phố','',city).strip()
city_file = unidecode(city.lower()).strip()
city_file = re.sub(r' ','',city_file)
source_table = 'REAL_CLEAN_' + city_file.upper()

ls_city = []
for k in DIC_CITY:
    for x in DIC_CITY[k]:
        ls_city.append(DIC_PREFIX[k] + ' ' + str(x))

ls_district = []
for k in DIC_DISTRICT:
    for x in DIC_DISTRICT[k]:
        ls_district.append(DIC_PREFIX[k] + ' ' + str(x))

ls_ward = []
for k in DIC_WARD:
    for x in DIC_WARD[k]:
        ls_ward.append(DIC_PREFIX[k] + ' ' + str(x))

ls_street = []
for k in DIC_STREET:
    for x in DIC_STREET[k]:
        ls_street.append(DIC_PREFIX[k].lower() + ' ' + str(x).lower())

ls_land_type = []
ls_legal_status = []
ls_pro_direction = []

from config_old.alonhadat_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.batdongsan_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.batdongsancomvn_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.dothinet_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.diaoconline_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.homedy_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.mogivn_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.nhachotot_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.nhadatcafeland_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.propzyvn_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.revervn_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.rongbay_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.sosanhnha_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.tinbatdongsan_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config_old.youhomes_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))


# List Functions
def create_folder(folder_name):
    '''
        Create folder if not exist 

            Parameters:
                folder_name (str): name of folder

            Returns:
                path (str): path of folder
    '''
    path = 'visualize/' + folder_name + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def print_data(df,write,var="summary"):
    today = date.today().strftime('%Y%m%d')
    folder_name = city_file + '_' + today
    path = create_folder(folder_name)

    if (var != 'summary'):
        df = df.toPandas()
        n = 5
    else:
        n = len(df)
    table = tabulate(df[0:n],headers='keys',showindex=False,tablefmt='psql')
    print(table)
    file_name = path + "_" + var + ".txt"
    if (write == "view"):
        with open(file_name,'w') as file:
            file.write(table)
    elif (write == "csv"):
        df.to_csv(file_name,index=False,sep="\t")

def unionAll(*dfs):
    return reduce(DataFrame.unionAll, dfs)

def main():
    # CONNECT DATABASE
    dataframe = spark.read.format("jdbc").options(
        url="jdbc:mysql://172.16.0.227/VN_REAL_CITY",
        driver = "com.mysql.jdbc.Driver",
        dbtable = source_table,
        user="root",
        password="123456789").load()

    dataframe.createOrReplaceTempView(source_table)
    sql_stm = "SELECT * FROM " + source_table
    df = spark.sql(sql_stm)
    length = df.count()
    dic = {}

    # # CHECK LAND_TYPE, PRO_DIRECTION, LEGAL_STATUS
    # d = df.filter(~F.col("LEGAL_STATUS").isin(ls_legal_status))
    # cols = ['ID_CLIENT','SITE','LEGAL_STATUS','CREATED_DATE']
    # dd = d.select(*cols)
    # print_data(dd,write,'LEGAL_STATUS')
    # dic['LEGAL_STATUS'] = [round(dd.count()/length*100)]

    # d = df.filter(~F.col("PRO_DIRECTION").isin(ls_pro_direction))
    # cols = ['ID_CLIENT','SITE','PRO_DIRECTION','CREATED_DATE']
    # dd = d.select(*cols)
    # print_data(dd,write,'PRO_DIRECTION')
    # dic['PRO_DIRECTION'] = [round(dd.count()/length*100)]

    # d = df.filter(~F.col("LAND_TYPE").isin(ls_land_type))
    # cols = ['ID_CLIENT','SITE','LAND_TYPE','CREATED_DATE']
    # dd = d.select(*cols)
    # print_data(dd,write,'LAND_TYPE')
    # dic['LAND_TYPE'] = [round(dd.count()/length*100)]

    # # CITY, DISTRICT, WARD, STREET, HOUSE_NUMBER
    # d = df.filter(~F.col("SPLIT_CITY").isin(ls_city))
    # cols = ['ID_CLIENT','SITE','SPLIT_CITY','CREATED_DATE']
    # d = d.select(*cols)
    # print_data(d,write,'SPLIT_CITY')
    # dic['SPLIT_CITY'] = [round(d.count()/length*100)]

    # d = df.filter(~F.col("SPLIT_DISTRICT").isin(ls_district))
    # cols = ['ID_CLIENT','SITE','SPLIT_DISTRICT','CREATED_DATE']
    # d = d.select(*cols)
    # print_data(d,write,'SPLIT_DISTRICT')
    # dic['SPLIT_DISTRICT'] = [round(d.count()/length*100)]

    # d = df.filter(~F.col("SPLIT_WARD").isin(ls_ward))
    # cols = ['ID_CLIENT','SITE','SPLIT_WARD','CREATED_DATE']
    # d = d.select(*cols)
    # print_data(d,write,'SPLIT_WARD')
    # dic['SPLIT_WARD'] = [round(d.count()/length*100)]

    # df = df.withColumn("FORMAT_STREET_LOWER",F.lower(F.col("FORMAT_STREET")))
    # d1 = df.filter(~F.lower(F.col("FORMAT_STREET_LOWER")).isin(ls_street))
    # d2 = df.where(F.length(F.col("FORMAT_STREET_LOWER")) > 50)
    # d = unionAll(d1, d2).distinct()
    # d = d.filter(~F.col("FORMAT_STREET").rlike('^Đường số[ ]?\d+[/0-9]*[a-zA-Z]*$'))
    # d = d.filter(~F.col("FORMAT_STREET").rlike('^Hương lộ[ ]?\d+$'))
    # cols = ['ID_CLIENT','SITE','FORMAT_STREET','CREATED_DATE']
    # d = d.select(*cols)
    # print_data(d,write,'FORMAT_STREET')
    # dic['FORMAT_STREET'] = [round(d.count()/length*100)]

    # d = df.filter(~F.col("FORMAT_HS").rlike('^\d+[/0-9]*[a-zA-Z]*$'))
    # d = d.filter(~F.col("FORMAT_HS").rlike('^Hẻm[ ]?\d+[/0-9]*[a-zA-Z]*$'))
    # d = d.filter(~F.col("FORMAT_HS").rlike('^Số[:]?[ ]?\d+[/0-9]*[a-zA-Z]*$'))
    # d = d.filter(~F.col("FORMAT_HS").rlike('^Ngõ[ ]?\d+[/0-9]*[a-zA-Z]*$'))
    # cols = ['ID_CLIENT','SITE','FORMAT_HS','CREATED_DATE']
    # d = d.select(*cols)
    # print_data(d,write,'FORMAT_HS')
    # dic['FORMAT_HS'] = [round(d.count()/length*100)]

    # CHECK PRICE, SURFACE, PRICE_TEXT, SURFACE_TEXT
    d1 = df.where((F.col("PRICE") != 0))
    d2 = df.where((F.col("PRICE") == 0) & (F.col("PRICE_TEXT") != 0))
    d = unionAll(d1, d2).distinct()
    d = d.withColumn('CHECK', F.when(((F.col("PRICE") != F.col("PRICE_TEXT")) & (F.col("PRICE") != 0)), 0).otherwise(1))
    dd = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','PRICE','PRICE_TEXT','CHECK','ADS_LINK','DETAILED_BRIEF']
    d = d.select(*cols)
    print_data(d,write,'PRICE')
    dic['PRICE'] = [round(dd.count()/length*100)]

    d1 = df.where((F.col("SURFACE") != 0))
    d2 = df.where((F.col("SURFACE") == 0) & (F.col("SURFACE_TEXT") != 0))
    d = unionAll(d1, d2).distinct()
    d = d.withColumn('CHECK', F.when(((F.col("SURFACE") != F.col("SURFACE_TEXT")) & (F.col("SURFACE") != 0)), 0).otherwise(1))
    dd = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','SURFACE','SURFACE_TEXT','CHECK','ADS_LINK','DETAILED_BRIEF']
    d = d.select(*cols)
    print_data(d,write,'SURFACE')
    dic['SURFACE'] = [round(dd.count()/length*100)]

    # CHECK ALLEY_ACCESS, FRONTAGE, ALLEY_TEXT, FRONTAGE_TEXT
    d1 = df.where((F.col("ALLEY_ACCESS") != 0))
    d2 = df.where((F.col("ALLEY_ACCESS") == 0) & (F.col("ALLEY_TEXT") != 0))
    d = unionAll(d1, d2).distinct()
    d = d.withColumn('CHECK', F.when(((F.col("ALLEY_ACCESS") != F.col("ALLEY_TEXT")) & (F.col("ALLEY_ACCESS") != 0)), 0).otherwise(1))
    dd = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','ALLEY_ACCESS','ALLEY_TEXT','CHECK','ADS_LINK','DETAILED_BRIEF']
    d = d.select(*cols)
    print_data(d,write,'ALLEY_ACCESS')
    dic['ALLEY_ACCESS'] = [round(dd.count()/length*100)]

    d1 = df.where((F.col("FRONTAGE") != 0))
    d2 = df.where((F.col("FRONTAGE") == 0) & (F.col("FRONTAGE_TEXT") != 0))
    d = unionAll(d1, d2).distinct()
    d = d.withColumn('CHECK', F.when(((F.col("FRONTAGE") != F.col("FRONTAGE_TEXT")) & (F.col("FRONTAGE") != 0)), 0).otherwise(1))
    dd = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','FRONTAGE','FRONTAGE_TEXT','CHECK','ADS_LINK','DETAILED_BRIEF']
    d = d.select(*cols)
    print_data(d,write,'FRONTAGE')
    dic['FRONTAGE'] = [round(dd.count()/length*100)]

    # PRO_WIDTH, PRO_WIDTH_TEXT, PRO_LENGTH, PRO_LENGTH_TEXT
    d1 = df.where((F.col("PRO_WIDTH") != 0))
    d2 = df.where((F.col("PRO_WIDTH") == 0) & (F.col("PRO_WIDTH_TEXT") != 0))
    d = unionAll(d1, d2).distinct()
    d = d.withColumn('CHECK', F.when(((F.col("PRO_WIDTH") != F.col("PRO_WIDTH_TEXT")) & (F.col("PRO_WIDTH") != 0)), 0).otherwise(1))
    dd = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','PRO_WIDTH','PRO_WIDTH_TEXT','CHECK','ADS_LINK','DETAILED_BRIEF']
    d = d.select(*cols)
    print_data(d,write,'PRO_WIDTH')
    dic['PRO_WIDTH'] = [round(dd.count()/length*100)]

    d1 = df.where((F.col("PRO_LENGTH") != 0))
    d2 = df.where((F.col("PRO_LENGTH") == 0) & (F.col("PRO_LENGTH_TEXT") != 0))
    d = unionAll(d1, d2).distinct()
    d = d.withColumn('CHECK', F.when(((F.col("PRO_LENGTH") != F.col("PRO_LENGTH_TEXT")) & (F.col("PRO_LENGTH") != 0)), 0).otherwise(1))
    dd = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','PRO_LENGTH','PRO_LENGTH_TEXT','CHECK','ADS_LINK','DETAILED_BRIEF']
    d = d.select(*cols)
    print_data(d,write,'PRO_LENGTH')
    dic['PRO_LENGTH'] = [round(dd.count()/length*100)]

    df = pd.DataFrame.from_dict(dic, orient='index',columns=['Different(%)'])
    df.reset_index(level=0, inplace=True)
    print_data(df,write)

if __name__ == "__main__":
    main()

