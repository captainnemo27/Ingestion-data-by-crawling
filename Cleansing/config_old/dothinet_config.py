source_mysql_host="172.16.0.167"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="REAL_ESTATE_VN"
source_mysql_table="DOTHINET"
des_mysql_host="172.16.0.167"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL"
des_mysql_table="REAL_CLEAN_DOTHINET"

# List of dictionaries
LAND_TYPE_DIC = {
    'căn hộ chung cư' : 'cc',
    'cửa hàng, ki ốt': 'ch',
    'kho, nhà xưởng': 'kx',
    'kho, nhà xưởng, đất': 'kx',
    'loại bất động sản khác': 'k',
    'nhà biệt thự, liền kề': 'bt',
    'nhà mặt phố': 'nmt',
    'nhà mặt tiền': 'nmt',
    'nhà riêng': 'nr',
    'nhà trọ, phòng trọ': 'npt',
    'trang trại, khu nghỉ dưỡng': 'ttnd',
    'văn phòng': 'vp',
    'đất': 'd',
    'đất nền dự án': 'dn'
}

PRO_DIRECTION_DIC = {
     'KXĐ': 'k',
     'Đông': 'd',
     'Tây-Bắc': 'tb',
     'Đông-Nam': 'dn',
     'Tây': 't',
     'Nam': 'n',
     'Đông-Bắc': 'db',
     'Bắc': 'b',
     'Tây-Nam': 'tn',
     'đông': 'đ',
     'nam': 'n',
     'đông bắc': 'đb',
     'bắc': 'b',
     'đông-nam': 'đn',
     'tây nam': 'tn',
     'tây': 't',
     'tây-bắc': 'tb',
     '': 'k'
}

LEGAL_STATUS_DIC = {
    None: None
}