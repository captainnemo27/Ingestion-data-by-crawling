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
parser.add_argument("-s","--site", type=str, default="")
parser.add_argument("-m","--mode", type=str, default="")
parser.add_argument("-c","--column", type=str, default="")
parser.add_argument("-v","--value", type=str, default="")
parser.add_argument("-f","--from_date", type=str, default="")
parser.add_argument("-e","--end_date", type=str, default="")
parser.add_argument("-w","--write", type=str, default="csv")
args = parser.parse_args()

SITENAME = args.site.lower()
mode = args.mode.lower()
column = args.column.upper()
value = args.value.lower()
from_date = args.from_date
end_date = args.end_date
write = args.write

ls_mode = ["clean","clean_test"]

ls_write = ["csv","view"]

ls_site = LS_SITE

if (SITENAME not in ls_site) or (mode not in ls_mode) or (write not in ls_write):
    parser.print_help(sys.stderr)
    print()
    print("error: SITE must in list sites and mode must in list modes")
    print("List sites: ",ls_site)
    print("List modes: ",ls_mode)
    print("List write: ",ls_write)
    sys.exit(1)

if ("crawl" in mode) and (column != "") and (column not in LS_ROOT):
    print("error: column must in list")
    print("List crawl columns: ",LS_ROOT)
    sys.exit(1)

if ("clean" in mode) and (column != "") and (column not in LS_CLEAN):
    print("error: column must in list")
    print("List clean columns: ",LS_CLEAN)
    sys.exit(1)

# IMPORT FILES
os.getcwd()
os.chdir("config/")
config_path = os.getcwd()
sys.path.insert(1,config_path)

file_config = SITENAME.lower() + '_config'
module = importlib.import_module(file_config)

source_mysql_host = module.source_mysql_host
source_mysql_user = module.source_mysql_user
source_mysql_password = module.source_mysql_password
source_mysql_db = module.source_mysql_db
source_mysql_table = module.source_mysql_table

des_mysql_host = module.des_mysql_host
des_mysql_user = module.des_mysql_user
des_mysql_password = module.des_mysql_password
des_mysql_db = module.des_mysql_db
des_mysql_table = module.des_mysql_table

os.chdir("..")

# DECLARES
# Configure DB
if (mode == "clean_test"):
    data_table = "CLEAN_" + SITENAME.upper()
else: 
    data_table = des_mysql_table
data_host = des_mysql_host
data_user = des_mysql_user
data_password = des_mysql_password
data_db = des_mysql_db
ls_search = LS_CLEAN

if (column==""):
    ls_var = ls_search 
else:
    ls_var = [column]

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

from config.alonhadat_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.batdongsan_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.batdongsancomvn_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.dothinet_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.diaoconline_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.homedy_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.mogivn_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.nhachotot_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.nhadatcafeland_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.propzyvn_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.revervn_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.rongbay_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.sosanhnha_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.tinbatdongsan_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
l = [LAND_TYPE_DIC[x] for x in list(LAND_TYPE_DIC.keys())]
ls_land_type = set(ls_land_type).union(set(l))
l = [PRO_DIRECTION_DIC[x] for x in list(PRO_DIRECTION_DIC.keys())]
ls_legal_status = set(ls_legal_status).union(set(l))
l = [LEGAL_STATUS_DIC[x] for x in list(LEGAL_STATUS_DIC.keys())]
ls_pro_direction = set(ls_pro_direction).union(set(l))

from config.youhomes_config import LAND_TYPE_DIC, PRO_DIRECTION_DIC, LEGAL_STATUS_DIC
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
    folder_name = SITENAME + '_' + today
    path = create_folder(folder_name)

    if (var != 'summary'):
        df = df.toPandas()
        n = 5
    else:
        n = len(df)
    table = tabulate(df[0:n],headers='keys',showindex=False,tablefmt='psql')
    print(table)
    file_name = path + mode + "_" + var + ".txt"
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
        url="jdbc:mysql://"+data_host+"/"+data_db,
        driver = "com.mysql.jdbc.Driver",
        dbtable = data_table,
        user=data_user,
        password=data_password).load()

    dataframe.createOrReplaceTempView(data_table)
    sql_stm = gen_statement(data_table,column,value,from_date,end_date)
    df = spark.sql(sql_stm)
    length = df.count()
    dic = {}

    # CHECK LAND_TYPE, PRO_DIRECTION, LEGAL_STATUS
    d = df.filter(~F.col("LEGAL_STATUS").isin(ls_legal_status))
    cols = ['ID_CLIENT','SITE','LEGAL_STATUS','CREATED_DATE']
    dd = d.select(*cols)
    print_data(dd,write,'LEGAL_STATUS')
    dic['LEGAL_STATUS'] = [round(dd.count()/length*100)]

    d = df.filter(~F.col("PRO_DIRECTION").isin(ls_pro_direction))
    cols = ['ID_CLIENT','SITE','PRO_DIRECTION','CREATED_DATE']
    dd = d.select(*cols)
    print_data(dd,write,'PRO_DIRECTION')
    dic['PRO_DIRECTION'] = [round(dd.count()/length*100)]

    d = df.filter(~F.col("LAND_TYPE").isin(ls_land_type))
    cols = ['ID_CLIENT','SITE','LAND_TYPE','CREATED_DATE']
    dd = d.select(*cols)
    print_data(dd,write,'LAND_TYPE')
    dic['LAND_TYPE'] = [round(dd.count()/length*100)]

    # CITY, DISTRICT, WARD, STREET, HOUSE_NUMBER
    d = df.filter(~F.col("SPLIT_CITY").isin(ls_city))
    cols = ['ID_CLIENT','SITE','SPLIT_CITY','CREATED_DATE']
    d = d.select(*cols)
    print_data(d,write,'SPLIT_CITY')
    dic['SPLIT_CITY'] = [round(d.count()/length*100)]

    d = df.filter(~F.col("SPLIT_DISTRICT").isin(ls_district))
    cols = ['ID_CLIENT','SITE','SPLIT_DISTRICT','CREATED_DATE']
    d = d.select(*cols)
    print_data(d,write,'SPLIT_DISTRICT')
    dic['SPLIT_DISTRICT'] = [round(d.count()/length*100)]

    d = df.filter(~F.col("SPLIT_WARD").isin(ls_ward))
    cols = ['ID_CLIENT','SITE','SPLIT_WARD','CREATED_DATE']
    d = d.select(*cols)
    print_data(d,write,'SPLIT_WARD')
    dic['SPLIT_WARD'] = [round(d.count()/length*100)]

    df = df.withColumn("FORMAT_STREET_LOWER",F.lower(F.col("FORMAT_STREET")))
    d1 = df.filter(~F.lower(F.col("FORMAT_STREET_LOWER")).isin(ls_street))
    d2 = df.where(F.length(F.col("FORMAT_STREET_LOWER")) > 50)
    d = unionAll(d1, d2).distinct()
    d = d.filter(~F.col("FORMAT_STREET").rlike('^Đường số[ ]?\d+[/0-9]*[a-zA-Z]*$'))
    cols = ['ID_CLIENT','SITE','FORMAT_STREET','CREATED_DATE']
    d = d.select(*cols)
    print_data(d,write,'FORMAT_STREET')
    dic['FORMAT_STREET'] = [round(d.count()/length*100)]

    d = df.filter(~F.col("FORMAT_HS").rlike('^\d+[/0-9]*[a-zA-Z]*$'))
    d = d.filter(~F.col("FORMAT_HS").rlike('^Hẻm[ ]?\d+[/0-9]*[a-zA-Z]*$'))
    d = d.filter(~F.col("FORMAT_HS").rlike('^Số[:]?[ ]?\d+[/0-9]*[a-zA-Z]*$'))
    d = d.filter(~F.col("FORMAT_HS").rlike('^Ngõ[ ]?\d+[/0-9]*[a-zA-Z]*$'))
    cols = ['ID_CLIENT','SITE','FORMAT_HS','CREATED_DATE']
    d = d.select(*cols)
    print_data(d,write,'FORMAT_HS')
    dic['FORMAT_HS'] = [round(d.count()/length*100)]

    # CHECK PRICE, SURFACE, PRICE_TEXT, SURFACE_TEXT
    d = df.where((F.col("PRICE") != 0) & (F.col("PRICE_TEXT") != 0))
    d = d.withColumn('CHECK', F.when(((F.col("PRICE") == F.col("PRICE_TEXT"))), 1).otherwise(0))
    d = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','PRICE','PRICE_TEXT','CHECK']
    d = d.select(*cols)
    print_data(d,write,'PRICE')
    dic['PRICE'] = [round(d.count()/length*100)]

    d = df.where((F.col("SURFACE") != 0) & (F.col("SURFACE_TEXT") != 0))
    d = d.withColumn('CHECK', F.when(((F.col("SURFACE") == F.col("SURFACE_TEXT"))), 1).otherwise(0))
    d = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','SURFACE','SURFACE_TEXT','CHECK']
    d = d.select(*cols)
    print_data(d,write,'SURFACE')
    dic['SURFACE'] = [round(d.count()/length*100)]

    # CHECK ALLEY_ACCESS, FRONTAGE, ALLEY_TEXT, FRONTAGE_TEXT
    d = df.where((F.col("ALLEY_ACCESS") != 0) & (F.col("ALLEY_TEXT") != 0))
    d = d.withColumn('CHECK', F.when(((F.col("ALLEY_ACCESS") == F.col("ALLEY_TEXT"))), 1).otherwise(0))
    d = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','ALLEY_ACCESS','ALLEY_TEXT','CHECK']
    d = d.select(*cols)
    print_data(d,write,'ALLEY_ACCESS')
    dic['ALLEY_ACCESS'] = [round(d.count()/length*100)]

    d = df.where((F.col("FRONTAGE") != 0) & (F.col("FRONTAGE_TEXT") != 0))
    d = d.withColumn('CHECK', F.when(((F.col("FRONTAGE") == F.col("FRONTAGE_TEXT"))), 1).otherwise(0))
    d = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','FRONTAGE','FRONTAGE_TEXT','CHECK']
    d = d.select(*cols)
    print_data(d,write,'FRONTAGE')
    dic['FRONTAGE'] = [round(d.count()/length*100)]

    # PRO_WIDTH, PRO_WIDTH_TEXT, PRO_LENGTH, PRO_LENGTH_TEXT
    d = df.where((F.col("PRO_WIDTH") != 0) & (F.col("PRO_WIDTH_TEXT") != 0))
    d = d.withColumn('CHECK', F.when(((F.col("PRO_WIDTH") == F.col("PRO_WIDTH_TEXT"))), 1).otherwise(0))
    d = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','PRO_WIDTH','PRO_WIDTH_TEXT','CHECK']
    d = d.select(*cols)
    print_data(d,write,'PRO_WIDTH')
    dic['PRO_WIDTH'] = [round(d.count()/length*100)]

    d = df.where((F.col("PRO_LENGTH") != 0) & (F.col("PRO_LENGTH_TEXT") != 0))
    d = d.withColumn('CHECK', F.when(((F.col("PRO_LENGTH") == F.col("PRO_LENGTH_TEXT"))), 1).otherwise(0))
    d = d.where((F.col("CHECK") == 0))
    cols = ['ID_CLIENT','SITE','PRO_LENGTH','PRO_LENGTH_TEXT','CHECK']
    d = d.select(*cols)
    print_data(d,write,'PRO_LENGTH')
    dic['PRO_LENGTH'] = [round(d.count()/length*100)]

    df = pd.DataFrame.from_dict(dic, orient='index',columns=['Different(%)'])
    df.reset_index(level=0, inplace=True)
    print_data(df,write)

if __name__ == "__main__":
    main()

