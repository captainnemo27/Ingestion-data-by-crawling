import pyspark # only run after findspark.init()
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import *

spark = SparkSession.builder.master('local[*]').appName('my-cool-app').getOrCreate()

from tabulate import tabulate
import os
import sys
import importlib
import argparse
from dateutil.relativedelta import relativedelta

from libs.or_prep_ import *

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("-s","--site", type=str, default="")
parser.add_argument("-t","--table", type=str, default="")
parser.add_argument("-f","--from_date", type=str, default="")
parser.add_argument("-e","--end_date", type=str, default="")
args = parser.parse_args()

SITENAME = args.site.lower()
table = args.table
from_date = args.from_date
end_date = args.end_date

ls_site = LS_SITE

if (SITENAME not in ls_site):
    parser.print_help(sys.stderr)
    print()
    print("error: SITE must in list sites and mode must in list modes")
    print("List sites: ",ls_site)
    sys.exit(1)

if (table == ""):
    parser.print_help(sys.stderr)
    print()
    print("error: table format VN_REAL_RAW_YYYY_MM")
    sys.exit(1)

monthly = True
if (from_date != "" or end_date != ""):
    monthly = False
else:
    # SELECT PREVIOUS MONTH
    ar = table.split('_')
    month = ar[len(ar)-1]
    year = ar[len(ar)-2]
    now = '01/'+month+'/'+year
    datetimeobj=datetime.datetime.strptime(now,"%d/%m/%Y")
    last = datetimeobj - relativedelta(months=1)
    last = last.strftime('%d-%m-%Y')
    ar = last.split('-')
    last_month = ar[1]
    last_year = ar[2]
    last_data_db = 'VN_REAL_RAW_' + last_year + '_' + last_month

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

os.chdir("..")

# DECLARES
# Configure DB
data_table = source_mysql_table
data_host = source_mysql_host
data_user = source_mysql_user
data_password = source_mysql_password
data_db = table
ls_search = LS_ROOT
ls_num = ['USED_SURFACE','USED_SURFACE_UNIT','SURFACE','SURFACE_UNIT','PRICE','PRICE_UNIT',\
           'PRO_LENGTH','PRO_WIDTH','ALLEY_ACCESS', 'FRONTAGE',\
            'PRICE_ORIGINAL','SURFACE_ORIGINAL','USED_SURFACE_ORIGINAL']
ls_none = ['đang cập nhật','liên hệ','đã bán','thương lượng','thỏa thuận','kxđ']

# List Functions
def count_null(df,cols):
    '''
    Count number and percent missing data in column

        Parameters:
            df (dataframe)
            cols (array): list of col

        Returns:
            dic (dictionary): dic key: percent missing
    '''
    length = df.count()
    dic = {}
    for x in cols:
        null = df.filter(df[x].isNull()).count()
        percent = round(null/length*100,2)
        dic[x] = percent
    return dic

# FILTER LS_EXIST
site_anaylise = pd.read_csv('libs/SITE_ANALYSE.csv',index_col=None)
site_anaylise = site_anaylise[['FIELD_NAME',SITENAME.upper()]]
site_anaylise = site_anaylise.fillna('')
dic_exist = dict(site_anaylise.values)
ls_exist = [x for x in dic_exist if dic_exist[x] == '']

def main():
    start = time()

    # CONNECT DATABASE
    previous = True
    if (monthly):
        try:
            dataframe = spark.read.format("jdbc").options(
            url="jdbc:mysql://"+data_host+"/"+last_data_db,
            driver = "com.mysql.jdbc.Driver",
            dbtable = data_table,
            user=data_user,
            password=data_password).load()
        except:
            previous = False
            pass
        else:
            dataframe.createOrReplaceTempView(data_table)
            sql_stm = gen_statement(data_table,"","",from_date,end_date)
            last_df = spark.sql(sql_stm)

    try:
        dataframe = spark.read.format("jdbc").options(
            url="jdbc:mysql://"+data_host+"/"+data_db,
            driver = "com.mysql.jdbc.Driver",
            dbtable = data_table,
            user=data_user,
            password=data_password).load()
    except:
        return

    dataframe.createOrReplaceTempView(data_table)
    sql_stm = gen_statement(data_table,"","",from_date,end_date)
    df = spark.sql(sql_stm)
    
    length = df.count()

    if (length > 0):
        dic_irregular = {}

        # Check data
        for column in ls_search:
            if column not in ls_num:
                if (column == 'FULL_ADDRESS'):
                    max_length = 155
                elif (column == 'DETAILED_BRIEF'):
                    max_length = float('inf')
                else:
                    max_length = 50
                d = df.where(F.length(F.col(column)) > max_length)
            else:
                d = df.filter(~F.col(column).rlike('[0-9]+'))
            percent = d.count()
            if (percent > 0):
                if column not in ls_num:
                    dic_irregular[column] = str(percent) + '/' + str(length) + ' > ' + str(max_length)
                else:
                    dic_irregular[column] = str(percent) + '/' + str(length) + ' <> nb '
            else:
                dic_irregular[column] = ''

        # Check missing
        dic_missing = count_null(df,ls_search)
        
        # Merge data
        d_comb = {key: (dic_missing[key],dic_irregular[key]) for key in dic_missing}
        current_data = pd.DataFrame.from_dict(d_comb, orient='index',columns=['% CURRENT MISSING','CURRENT WRONG VALUES'])
        if (previous) and (monthly):
            dic_last_missing = count_null(last_df,ls_search)
            last_data = pd.DataFrame.from_dict(dic_last_missing, orient='index',columns=['% PREVIOUS MISSING'])
            data = pd.concat([last_data, current_data], axis=1)
        else:
            data = current_data
        data = data.rename_axis('FIELD_NAME').reset_index()

        # Filter data
        #data = data[data['FIELD_NAME'].isin(ls_exist)]
        data = data[(data['% CURRENT MISSING'] > 30) | (data['CURRENT WRONG VALUES'] != '')] 

        # Print data
        table = tabulate(data,headers='keys',showindex=False,tablefmt='psql')

    finish = time()
    total_time = str(round(((finish - start)/60),5)) + " mins"

    # Print report
    print("*** REPORT ***")
    
    print("source_mysql_host = ",source_mysql_host)
    print("source_mysql_db = ",data_db)

    print("Site name = " + SITENAME)
    print("Site volume = " + str(length))
    print("Total time = " + total_time)

    if (length > 0):
        print(table)
    else:
        print("Nothing to report")


if __name__ == "__main__":
    main()

