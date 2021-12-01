import os
import sys
import importlib
import argparse
import logging
import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()
from datetime import datetime

from libs.or_utils_ import *
from libs.or_address_ import *
from libs.or_prep_ import *

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("-s","--site", type=str, default="")
parser.add_argument("-t","--table", type=str, default="")
parser.add_argument("-test","--test_mode", type=bool, default=False)
parser.add_argument("-pf","--pro_flag", type=int, default=0)
parser.add_argument("-i","--index", type=int, default=0)
args = parser.parse_args()

SITENAME = args.site.lower()
table = args.table
test_mode = args.test_mode
pro_flag = args.pro_flag
index = args.index

if (SITENAME not in LS_SITE) or (pro_flag not in [0,5,12]):
    parser.print_help(sys.stderr)
    print()
    print("error: SITE must in list")
    print("List sites: ",LS_SITE)
    print("List pro_flag: ",[0,5,12])
    sys.exit(1)

if (table == ""):
    parser.print_help(sys.stderr)
    print()
    print("error: table format VN_REAL_RAW_YYYY_MM")
    sys.exit(1)
    
ar = table.split('_')
month = ar[len(ar)-1]
year = ar[len(ar)-2]

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
source_mysql_db = module.source_mysql_db + year + '_' + month
source_mysql_table = module.source_mysql_table

des_mysql_host = module.des_mysql_host
des_mysql_user = module.des_mysql_user
des_mysql_password = module.des_mysql_password
des_mysql_db = module.des_mysql_db + year + '_' + month
des_mysql_table = module.des_mysql_table

LAND_TYPE_DIC = module.LAND_TYPE_DIC
LEGAL_STATUS_DIC = module.LEGAL_STATUS_DIC 
PRO_DIRECTION_DIC = module.PRO_DIRECTION_DIC

LAND_TYPE_DIC =  {normalize_land_type(k.lower()): v for k, v in LAND_TYPE_DIC.items() if (k)}
PRO_DIRECTION_DIC =  {k.lower(): v for k, v in PRO_DIRECTION_DIC.items() if (k)}
LEGAL_STATUS_DIC =  {k.lower(): v for k, v in LEGAL_STATUS_DIC.items() if (k)}

os.chdir("..")

# DECLARES
mysql_clean_table = "TEMP_CLEAN_" + SITENAME.upper() 
today = datetime.date.today()
date = today.strftime("%Y%m%d")

if (not test_mode):
    log_file = LOG_FOLDER + "/log_" + SITENAME.lower() + "_" + date + ".txt"
    idx = 0
    pf = 5
else:
    log_file = "log_" + SITENAME.lower() + "_" + date + ".txt"
    idx = index
    pf = pro_flag

def main():
    # Create the logging instance for logging to file only
    logger = logging.getLogger()
    file_logger = logging.FileHandler(log_file, mode='w')
    file_logger_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%d/%m/%Y %H:%M')
    file_logger.setFormatter(file_logger_format)
    logger.addHandler(file_logger)
    logger.setLevel(logging.DEBUG)

    # Add the console logging
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    logging.getLogger().addHandler(console)

    # Connect database
    db_connection = sqlalchemy.create_engine("mysql://{}:{}@{}/{}?charset=utf8mb4".format(source_mysql_user,source_mysql_password,source_mysql_host,source_mysql_db),connect_args={'connect_timeout': 600000})
    logger.info("Connect database successfully") 
    clean_db_connection = sqlalchemy.create_engine("mysql://{}:{}@{}/{}?charset=utf8mb4".format(des_mysql_user,des_mysql_password,des_mysql_host,des_mysql_db),connect_args={'connect_timeout': 600000}) 
    logger.info("Connect clean database successfully")

    start = time()

    if (not test_mode):
        # Update PRO_FLAG = 5 to avoid conflict when importing 
        try:
            sql = "UPDATE " + source_mysql_table + " SET PRO_FLAG = 5 WHERE PRO_FLAG = 0"
            with db_connection.begin() as conn:
                conn.execute(sql)
            conn.close()
        except ValueError as vx:
            logger.exception('Error occurred ' + str(vx))
            return
        except Exception as ex:   
            logger.exception('Error occurred ' + str(ex))
            return
        else:
            logger.info("Set PRO_FLAG = 5 successfully")

    # Create CLEAN_DATA_COPY empty
    try:
        sql_drop_exists = "DROP TABLE IF EXISTS " + mysql_clean_table
        sql = "CREATE TABLE " + mysql_clean_table + " AS (SELECT * FROM " + des_mysql_table + " WHERE 1=2)"
        sql_alter = "ALTER TABLE " + mysql_clean_table + " CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        with clean_db_connection.begin() as clean_conn:
            clean_conn.execute(sql_drop_exists)
            clean_conn.execute(sql)
            clean_conn.execute(sql_alter)
        clean_conn.close()
    except ValueError as vx:
        logger.exception('Error occurred ' + str(vx))
        return
    except Exception as ex:   
        logger.exception('Error occurred ' + str(ex))
        return
    
    # Set chunk file
    limit = 1000
    i = idx
    count = 0

    dict_report_raw = []
    dict_report_cleaned = []

    while True:
        try:
            count = count + 1
            
            df = pd.read_sql('SELECT * FROM '+ source_mysql_table + " WHERE PRO_FLAG = " + str(pf) + " limit " + str(limit) + " offset " + str(i), con=db_connection)
            dict_chunk_raw = dict(Counter(df['CREATED_DATE'].values))

            if (test_mode) and (count == 5):
                break

            # Stopping Condition
            if df.empty == True:            
                logger.info("Read all database")
                break         

            logger.info("Cleansing index " + str(i) + " to " + str(i+limit)) 
            i = i + limit

            # Data Cleaning

            # # ### 1. ID_CLIENT
            # df['ID_CLIENT'] = df['ID_CLIENT'].apply(lambda x: SITENAME+"_"+x)

            # ### 2. LAND_TYPE
            df['LAND_TYPE'] = df.apply(lambda x: get_value_advance(LAND_TYPE_DIC,LAND_TYPE_DIC_SHORT,normalize_land_type(x['LAND_TYPE'])) if (pd.notnull(x['LAND_TYPE'])) else get_value_from_str(ADS_LINK_DIC,x['ADS_LINK']),axis=1)

            # ### 3. LEGAL_STATUS
            df['LEGAL_STATUS'] = df['LEGAL_STATUS'].apply(lambda x: get_value_advance(LEGAL_STATUS_DIC,LEGAL_STATUS_DIC_SHORT,x))
            if (SITENAME == "batdongsancomvn"):
                df['LEGAL_STATUS'] = df['LEGAL_STATUS'].apply(lambda x:'k' if str(x).count(' ') > 0 else x)

            # ### 4. PRO_DIRECTION
            df['PRO_DIRECTION'] = df['PRO_DIRECTION'].apply(lambda x: get_value_advance(PRO_DIRECTION_DIC,PRO_DIRECTION_DIC_SHORT,x))
            
            logger.info("...Done LAND_TYPE, LEGAL_STATUS, PRO_DIRECTION")

            # ### 5. PRO_LENGTH - 6. PRO_WIDTH
            df['PRO_LENGTH'] = df['PRO_LENGTH'].apply(lambda x: get_val_with_m(str(x)) if (pd.notnull(x)) else 0)

            df['PRO_WIDTH'] = df['PRO_WIDTH'].apply(lambda x: get_val_with_m(str(x)) if (pd.notnull(x)) else 0)

            logger.info("...Done PRO_LENGTH, PRO_WIDTH")

            # ### 7. USED_SURFACE - 8. SURFACE
            df["USED_SURFACE_X"] = df.apply(lambda row: get_surface_original_in_m2(row['USED_SURFACE_ORIGINAL']), axis=1)
            df['USED_SURFACE'] = df.apply(lambda row: row["USED_SURFACE_X"] if (row["USED_SURFACE_X"] !=0) else get_surface_in_m2(row['USED_SURFACE'], row['USED_SURFACE_UNIT']),axis=1)

            df["SURFACE_X"] = df.apply(lambda row: get_surface_original_in_m2(row['SURFACE_ORIGINAL']), axis=1)
            df['SURFACE'] = df.apply(lambda row: row["SURFACE_X"] if (row["SURFACE_X"] !=0) else get_surface_in_m2(row['SURFACE'], row['SURFACE_UNIT']),axis=1)
            df['SURFACE'] = df.apply(lambda row: row['SURFACE'] if (row['SURFACE']!=0) else row['USED_SURFACE'], axis=1)
            
            logger.info("...Done USED_SURFACE, SURFACE")

            # ### 9. PRICE, 10. PRICE_M2
            df['PRICE_X'] = df.apply(lambda row: get_price(row['PRICE_ORIGINAL'],'', row['SURFACE']), axis=1)            
            df['PRICE'] = df.apply(lambda row: row["PRICE_X"] if (row["PRICE_X"] != 0) else get_price(row['PRICE'], row['PRICE_UNIT'], row['SURFACE']),axis=1)

            df['PRICE_M2'] = df.apply(lambda row: round(float(row['PRICE'])/float(row['SURFACE']),2) if (row['SURFACE']!=0) else 0, axis=1)

            logger.info("...Done PRICE, PRICE_M2")

            # ### 11. STREET - 12. WARD - 13. DISTRICT - 14. CITY - 15. FULL_ADDRESS
            if (SITENAME == "propzyvn"):
                df['FULL_ADDRESS_X'] = df['FULL_ADDRESS'].fillna('') + " , " + df['CITY'].fillna('')
            else:
                df['FULL_ADDRESS_X'] = df['FULL_ADDRESS']
            df['SPLIT_ADDRESS'] = df.apply(lambda row: standardize_address(check_empty(row["FULL_ADDRESS_X"]),check_empty(row["CITY"]),check_empty(row["DISTRICT"]),check_empty(row["WARD"]),check_empty(row["STREET"])),axis=1)
            df['SPLIT_CITY'] = df.apply(lambda row: row['SPLIT_ADDRESS'][0],axis=1)
            df['SPLIT_DISTRICT'] = df.apply(lambda row: row['SPLIT_ADDRESS'][1],axis=1)
            df['SPLIT_WARD'] = df.apply(lambda row: row['SPLIT_ADDRESS'][2],axis=1)
            df['SPLIT_STREET'] = df.apply(lambda row: row['SPLIT_ADDRESS'][3],axis=1)
            df['SPLIT_HS'] = df.apply(lambda row: row['SPLIT_ADDRESS'][4],axis=1)

            df['FULL_ADDRESS'] = df['FULL_ADDRESS'].apply(lambda x: limit_characters(x,255) if (pd.notnull(x)) else x)
            df['CITY'] = df['CITY'].apply(lambda x: limit_characters(x,100) if (pd.notnull(x)) else x)
            df['DISTRICT'] = df['DISTRICT'].apply(lambda x: limit_characters(x,100) if (pd.notnull(x)) else x)
            df['WARD'] = df['WARD'].apply(lambda x: limit_characters(x,100) if (pd.notnull(x)) else x)

            logger.info("...Done FULL_ADDRESS")

            # ### 16. CHECK COMMA LAT LON
            df['LAT'] = df['LAT'].apply(lambda x: x if (not re.search("[a-zA-Z]", str(check_empty(x)))) else None)
            df['LAT'] = df['LAT'].apply(lambda x: x.replace(',','.') if ((pd.notnull(x)) and (',' in x)) else x)
            df['LON'] = df['LON'].apply(lambda x: x if (not re.search("[a-zA-Z]", str(check_empty(x)))) else None)
            df['LON'] = df['LON'].apply(lambda x: x.replace(',','.') if ((pd.notnull(x)) and (',' in x)) else x)

            logger.info("...Done LAT, LON")

            # # ### 17. ALLEY_ACCESS - 18. FRONTAGE
            df['ALLEY_ACCESS'] = df['ALLEY_ACCESS'].apply(lambda x: get_val_with_m(str(x)) if (pd.notnull(x)) else 0)

            df['FRONTAGE'] = df['FRONTAGE'].apply(lambda x: get_val_with_m(str(x)) if (pd.notnull(x)) else 0)

            logger.info("...Done ALLEY_ACCESS, FRONTAGE")

            # ### 19. NB_ROOMS
            df['NB_ROOMS'] = df['NB_ROOMS'].apply(lambda x: float(x) if (not re.search("[a-zA-Z]", str(check_empty(x)))) else 0)

            # ### 20. NB_FLOORS
            df['NB_FLOORS'] = df['NB_FLOORS'].apply(lambda x: x if (pd.notnull(check_empty(x))) else 0)
            df['NB_FLOORS'] = df['NB_FLOORS'].apply(lambda x: get_nb_floors(x) if (str(x).isdigit() == False) else x)

            # ### 21. BEDROOM
            df['BEDROOM'] = df['BEDROOM'].apply(lambda x: float(x) if (pd.notnull(check_empty(x))) else 0)

            # ### 22. BATHROOM
            df['BATHROOM'] = df['BATHROOM'].apply(lambda x: int(x) if (pd.notnull(check_empty(x))) else 0)

            logger.info("...Done NB_ROOMS, NB_FLOORS, BEDROOM, BATHROOM")

            # ### 23. CREATED_DATE
            df['CREATED_DATE'] = df['CREATED_DATE'].apply(lambda x: convert_date(x) if (pd.notnull(check_empty(x))) else None)

            # ### 24. DATE_ORIGINAL
            df['DATE_ORIGINAL'] = df.apply(lambda x: convert_date(x['DATE_ORIGINAL']) if (pd.notnull(check_empty(x['DATE_ORIGINAL']))) else x['CREATED_DATE'],axis=1)

            # ### 25. ADS_DATE
            df['ADS_DATE_X'] = df.apply(lambda x: convert_date_str(x['ADS_DATE_ORIGINAL'],x['DATE_ORIGINAL']) if (pd.notnull(check_empty(x['ADS_DATE_ORIGINAL']))) else None,axis=1)
            df['ADS_DATE'] = df.apply(lambda x: x["ADS_DATE_X"] if (pd.notnull(check_empty(x["ADS_DATE_X"]))) else convert_date_str(x["ADS_DATE"],x['CREATED_DATE']),axis=1)

            logger.info("...Done CREATED_DATE, DATE_ORIGINAL, ADS_DATE")

            # ### 26. DEALER_ADDRESS
            df['DEALER_ADDRESS'] = df['DEALER_ADDRESS'].apply(lambda x: limit_characters(x,255) if (pd.notnull(x)) else x)

            # ### 27. DEALER_TEL
            df['DEALER_TEL'] = df['DEALER_TEL'].apply(lambda x: split_tel(x))

            # ### 28. DEALER_JOINED_DATE
            df['DEALER_JOINED_DATE'] = df.apply(lambda x: solve_dealer_joined_date(x['DATE_ORIGINAL'], x['DEALER_JOINED_DATE'] if (pd.notnull(check_empty(x['DEALER_JOINED_DATE']))) else None), axis = 1)
            df['DEALER_JOINED_DATE'] = df['DEALER_JOINED_DATE'].apply(lambda x: convert_date(x) if (pd.notnull(check_empty(x))) else None)

            # ### 29. PROJECT_NAME
            df['PROJECT_NAME'] = df['PROJECT_NAME'].apply(lambda x: limit_characters(x,255) if (pd.notnull(x)) else x)

            logger.info("...Done DEALER_ADDRESS, DEALER_TEL, DEALER_JOINED_DATE, PROJECT_NAME")

            # Data Pre-process

            # PRO_WIDTH_TEXT, PRO_LENGTH_TEXT
            df['PRO_WIDTH_TEXT'] = df.apply(lambda x: get_width_length(x['DETAILED_BRIEF'])[0], axis=1)
            df['PRO_LENGTH_TEXT'] = df.apply(lambda x: get_width_length(x['DETAILED_BRIEF'])[1], axis=1)

            logger.info("...Done PRO_WIDTH_TEXT, PRO_LENGTH_TEXT")

            # ALLEY_TEXT, FRONTAGE_TEXT
            df['ALLEY_TEXT'] = df.apply(lambda x: get_road_width(x['DETAILED_BRIEF'])[0], axis=1)
            df['FRONTAGE_TEXT'] = df.apply(lambda x: get_road_width(x['DETAILED_BRIEF'])[1], axis=1)

            logger.info("...Done ALLEY_TEXT, FRONTAGE_TEXT")

            # SURFACE_TEXT, PRICE_TEXT
            df['SURFACE_TEXT'] = df.apply(lambda x: get_surface_from_text(x['DETAILED_BRIEF']), axis=1)
            df['PRICE_TEXT'] = df.apply(lambda x: get_price_from_text(x['DETAILED_BRIEF'],x['SURFACE_TEXT']), axis=1)

            logger.info("...Done SURFACE_TEXT, PRICE_TEXT")

            # FORMAT_STREET, FORMAT_HS
            df['STREET_HS'] = df.apply(lambda x: standardize_street_hs(x['SPLIT_STREET'],x['SPLIT_HS']),axis=1)
            df['FORMAT_STREET'], df['FORMAT_HS'] = zip(*df.STREET_HS)

            logger.info("...Done FORMAT_STREET, FORMAT_HS")

            # # # LAT_OS, LON_OS
            df['LON_OS'] = None
            df['LAT_OS'] = None
            # df['FULL_ADDRESS_ALL'] = df['FORMAT_HS'].fillna('') + " , " + df['FORMAT_STREET'].fillna('') + " , " + df['SPLIT_WARD'].fillna('') + " , " + df['SPLIT_DISTRICT'].fillna('') + " , " + df['SPLIT_CITY'].fillna('')
            # df['LON_LAT'] = df.apply(lambda x: convert_latlon(x['FULL_ADDRESS_ALL']),axis=1)
            # df['LON_OS'], df['LAT_OS'] = zip(*df.LON_LAT)
            
            logger.info("...Done LON_OS, LAT_OS")

            # ### PRO_FLAG
            df['PRO_FLAG'] = 12

            logger.info("...Done PRO_FLAG")

            select_columns = ['ID_CLIENT','SITE','ADS_LINK','FOR_SALE','FOR_LEASE','TO_BUY','TO_LEASE',\
                'LAND_TYPE','ADS_DATE','PRICE','PRICE_M2','SURFACE','USED_SURFACE','PRO_WIDTH','PRO_LENGTH',\
                'LEGAL_STATUS','PRO_CURRENT_STATUS','PRO_DIRECTION','FRONTAGE','ALLEY_ACCESS','NB_LOTS',\
                'PRO_UTILITIES','NB_ROOMS','NB_FLOORS','KITCHEN','BEDROOM','BATHROOM','GARAGE','TOILET',\
                'FULL_ADDRESS','STREET','WARD','DISTRICT','CITY','LAT','LON','LAT_OS','LON_OS','PHOTOS',\
                'SPLIT_HS','SPLIT_STREET','SPLIT_WARD','SPLIT_DISTRICT','SPLIT_CITY',\
                'PRO_WIDTH_TEXT','PRO_LENGTH_TEXT','ALLEY_TEXT','FRONTAGE_TEXT','SURFACE_TEXT','PRICE_TEXT','FORMAT_STREET','FORMAT_HS',\
                'ADS_TITLE','BRIEF','DETAILED_BRIEF','DEALER_NAME','DEALER_TYPE','DEALER_ADDRESS','DEALER_EMAIL','DEALER_TEL','DEALER_JOINED_DATE',\
                'PROJECT_NAME','AGENCY_NAME','AGENCY_ADDRESS','AGENCY_CITY','AGENCY_TEL','AGENCY_WEBSITE',\
                'CHECK_CONVERT','PRO_FLAG','CREATED_DATE','DATE_ORIGINAL']

            data = df[select_columns]
            
            
            try:
                # ## Push data to server
                data.to_sql(mysql_clean_table, clean_db_connection, if_exists='append',index=False)
                dict_chunk_cleaned = dict(Counter(data['CREATED_DATE'].values))
            except Exception as ex: 
                logger.exception('Error occurred ' + str(ex))
                return
            else:
                logger.info("...Done PUSH DATA TO SERVER")

        except ValueError as vx:
            logger.exception('Error occurred ' + str(vx))
            return
        except Exception as ex:   
            logger.exception('Error occurred ' + str(ex))
            return

        dict_report_raw = dict(Counter(dict_report_raw) + Counter(dict_chunk_raw))

        try:
            dict_report_cleaned = dict(Counter(dict_report_cleaned) + Counter(dict_chunk_cleaned))
        except:
            pass

    if (not test_mode):
        # Copy to CLEAN_TABLE and drop CLEAN_TABLE_COPY
        try:
            sql_copy = "INSERT INTO " + des_mysql_table + " SELECT * FROM " + mysql_clean_table + " WHERE 1 = 1"
            sql_drop = "DROP TABLE " + mysql_clean_table
            with clean_db_connection.begin() as clean_conn:
                clean_conn.execute(sql_copy)
                clean_conn.execute(sql_drop)
            clean_conn.close()
        except ValueError as vx:
            logger.exception('Error occurred ' + str(vx))
            return
        except Exception as ex:   
            logger.exception('Error occurred ' + str(ex))
            return
        else:
            logger.info("Move TEMP table to REAL_CLEAN table")

        # Update PRO_FLAG = 12
        try:
            sql = "UPDATE " + source_mysql_table + " SET PRO_FLAG = 12 WHERE PRO_FLAG = 5"
            with db_connection.begin() as conn:
                conn.execute(sql)
            conn.close()
        except ValueError as vx:
            logger.exception('Error occurred ' + str(vx))
            return
        except Exception as ex:   
            logger.exception('Error occurred ' + str(ex))
            return
        else:
            logger.info("Update PRO_FLAG = 12 successfully")

    finish = time()

    total_time = str(round(((finish - start)/60),5)) + " mins"

    logger.info(SITENAME + " has been cleaned successfully")

    report(dict_report_raw,dict_report_cleaned,SITENAME,source_mysql_host,source_mysql_db,des_mysql_host,des_mysql_db,total_time)
   
if __name__ == "__main__":
    main()

