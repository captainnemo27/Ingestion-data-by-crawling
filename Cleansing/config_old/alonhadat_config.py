source_mysql_host="172.16.0.167"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="REAL_ESTATE_VN"
source_mysql_table="ALONHADAT"
des_mysql_host="172.16.0.167"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL"
des_mysql_table="REAL_CLEAN_ALONHADAT"

# List of dictionaries
LAND_TYPE_DIC = {
    "biệt thự, nhà liền kề":"bt",
    "các loại khác":"k",
    "căn hộ chung cư":"cc",           
    "kho, xưởng":"kx",
    "mặt bằng":"vp",
    "nhà hàng, khách sạn":"nhks",
    "nhà mặt tiền":"nmt",
    "nhà trong hẻm":"nh",         
    "phòng trọ, nhà trọ":"npt", 
    "shop, kiot, quán":"ch", 
    "trang trại":"ttnd",    
    "văn phòng":"vp",                 
    "đất nông, lâm nghiệp":"dnn",  
    "đất nền, liền kề, đất dự án":"dn",     
    "đất thổ cư, đất ở":"d"      
}

LEGAL_STATUS_DIC = {
    "giấy phép kd":"gt",         
    "giấy phép xd":"gt",         
    "giấy tờ hợp lệ":"gt",     
    "sổ hồng/ sổ đỏ":"sh"    
}

PRO_DIRECTION_DIC = {
    "bắc" : "b",
    "nam" : "n",
    "tây": "t",
    "tây bắc": "tb",
    "tây nam" : "tn",
    "đông": "d",
    "đông bắc": "db",
    "đông nam": "dn"
}
