source_mysql_host="172.16.0.167"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="REAL_ESTATE_VN"
source_mysql_table="PROPZYVN"
des_mysql_host="172.16.0.167"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL"
des_mysql_table="REAL_CLEAN_PROPZYVN"

# List of dictionaries
LAND_TYPE_DIC = {
    "đất nền" : "dn",
    "căn hộ" : "cc",
    "đất nền dự án" : "dn",
    "nhà riêng": "nr"
}

LEGAL_STATUS_DIC = {
    "khác" : "k",
    "sổ hồng" : "sh",
    "sổ đỏ" : "sh",
    "giấy chứng nhận phường quận" : "gt",
    "--": "k"
}

PRO_DIRECTION_DIC = {
    "nam" : "n",
    "bắc" : "b",
    "đông": "d",
    "tây": "t",
    "đ.nam" : "dn",
    "đ.bắc": "db",
    "t.bắc": "tb",
    "t.nam": "tn",
    "không xác định": "k",
    "--": "k"
}