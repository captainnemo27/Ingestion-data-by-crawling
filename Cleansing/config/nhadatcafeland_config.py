source_mysql_host="172.16.0.227"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="VN_REAL_RAW_"
source_mysql_table="NHADATCAFELAND"
des_mysql_host="172.16.0.227"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL_CLEAN_"
des_mysql_table="REAL_CLEAN_NHADATCAFELAND"

# List of dictionaries
LAND_TYPE_DIC = {
    "biệt thự": "bt",
    "bán căn hộ cao cấp":"chcc",
    "bán căn hộ chung cư":"cc",
    "bán kho, nhà xưởng":"kx",           
    "bán nhà biệt thự, liền kề":"bt",
    "bán nhà hàng - khách sạn":"nhks",
    "bán nhà mặt bằng":"nmt",
    "bán nhà phố":"nmt",
    "bán nhà riêng":"nr",         
    "bán phòng trọ":"npt", 
    "căn hộ cao cấp":"chcc", 
    "căn hộ chung cư":"cc",    
    "mặt bằng":"vp",                 
    "nhà kho - xưởng":"kx",  
    "nhà hàng - khách sạn":"nhks",     
    "nhà phố":"nmt",
    "nhà riêng":"nr",         
    "phòng trọ":"npt", 
    "văn phòng":"vp", 
    "đất cho sản xuất":"dnn",    
    "đất dự án":"dn",                 
    "đất lâm nghiệp":"dnn",  
    "đất nông, lâm nghiệp":"dnn",     
    "đất nền - đất ở - đất thổ cư":"dn"      
}

LEGAL_STATUS_DIC = {
    "chủ quyền tư nhân":"gt",         
    "giấy tay":"gt",         
    "giấy tờ hợp lệ":"gt",     
    "giấy đỏ":"sh",
    "hợp đồng":"hd",         
    "không xác định":"k",         
    "sổ hồng":"sh",     
    "đang hợp thức hóa":"gt",   
}

PRO_DIRECTION_DIC = {
    "bắc" : "b",
    "nam" : "n",
    "tây": "t",
    "tây bắc": "tb",
    "tây nam" : "tn",
    "đông": "d",
    "đông bắc": "db",
    "đông nam": "dn",
    "không xác định": "k"
}