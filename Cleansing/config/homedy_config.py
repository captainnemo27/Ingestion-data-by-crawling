source_mysql_host="172.16.0.167"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="VN_REAL_RAW_"
source_mysql_table="HOMEDY"
des_mysql_host="172.16.0.167"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL_CLEAN_"
des_mysql_table="REAL_CLEAN_HOMEDY"

# List of dictionaries
LAND_TYPE_DIC = {
    "bất động sản khác" : "k",
    "căn hộ" : "cc",
    "căn hộ dịch vụ" : "chdv",
    "cửa hàng, mặt bằng bán lẻ": "vp",
    "nhà biệt thự, liền kề": "bt",
    "nhà mặt phố": "nmt",
    "nhà mặt phố, shophouse": "sh",
    "nhà phố thương mại shophouse": "sh",
    "nhà riêng": "nr",
    "nhà trọ, phòng trọ": "npt",
    "văn phòng": "vp",
    "đất": "d",
    "đất nền dự án": "dn",
    "đất, nhà xưởng, kho bãi": "kx"
}

LEGAL_STATUS_DIC = {
    "chưa xác định" : "k",
    "giấy chứng nhận quyền sở hữu" : "gt",
    "giấy phép kinh doanh" : "gt",
    "giấy phép xây dựng" : "gt",
    "giấy tờ hợp lệ": "gt",
    "giấy viết tay": "gt",
    "sổ hồng": "sh",
    "sổ trắng": "gt",
    "sổ đỏ": "sh",
    "đang hợp thức hóa": "gt"
}

PRO_DIRECTION_DIC = {
    "bắc" : "b",
    "nam" : "n",
    "tây": "t",
    "tây-bắc": "tb",
    "tây-nam" : "tn",
    "đông": "d",
    "đông-bắc": "db",
    "đông-nam": "dn"
}