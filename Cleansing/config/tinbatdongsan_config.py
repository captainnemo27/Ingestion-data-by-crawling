source_mysql_host="172.16.0.167"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="VN_REAL_RAW_"
source_mysql_table="TINBATDONGSAN"
des_mysql_host="172.16.0.167"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL_CLEAN_"
des_mysql_table="REAL_CLEAN_TINBATDONGSAN"

# List of dictionaries
LAND_TYPE_DIC = {
    'cho thuê nhà trọ, phòng trọ':'npt',
    'cho thuê căn hộ chung cư':'chcc',
    'căn hộ chung cư':'chcc',
    'cho thuê nhà mặt phố':'nmt',
    'cho thuê nhà riêng':'nr',
    'nhà mặt phố':'nmt',
    'cho thuê văn phòng':'vp',
    'đất':'d',
    'nhà biệt thự, liền kề':'bt',
    'nhà riêng':'nr',
    'nhà mặt tiền':'nmt',
    'cho thuê kho, nhà xưởng, đất':'kx',
    'đất nền dự án':'dn',
    'trang trại, khu nghỉ dưỡng':'ttnd',
    'kho, nhà xưởng':'kx',
    'loại bất động sản khác':'k',
    'cho thuê nhà mặt tiền':'nmt',
    'cho thuê cửa hàng, ki ốt':'ch',
    'đất':'d',
    'cho thuê loại bất động sản khác':'k',
    'đ':'d',
    'nhà':'nr',
    '':'k'
}

PRO_DIRECTION_DIC = {
    'Tây-Bắc':'tb',
    'Nam':'n',
    'KXĐ': 'k',
    'Tây':'t',
    'Bắc': 'b',
    'Nam':'n',
    'Đông':'d',
    'Tây-Bắc':'tb',
    'Tây-Nam':'tn',
    'Đông-Bắc':'db',
    'Đông-Nam':'dn'
}

LEGAL_STATUS_DIC = {
    None: None
}