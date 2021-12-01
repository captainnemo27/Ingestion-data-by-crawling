source_mysql_host="172.16.0.167"
source_mysql_db="VN_REAL_RAW_"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_table="REVERVN"
des_mysql_host="172.16.0.167"
des_mysql_db="VN_REAL_CLEAN_"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_table="REAL_CLEAN_REVERVN"

# List of dictionaries
LAND_TYPE_DIC = {
    'Đất công nghiệp': 'dcn',
    'Tòa nhà kinh doanh': 'ot',
    'Nhà xưởng kho bãi': 'kx',
    'Lofthouse': 'lh',
    'Loại khác': 'k',
    'Văn phòng': 'vp',
    'Penthouse': 'ph',
    'Căn hộ dịch vụ': 'chdv',
    'Biệt thự': 'bt',
    'Mặt bằng kinh doanh': 'vp',
    'Shophouse': 'sh',
    'Đất nền': 'dn',
    'Office-tel': 'ot',
    'Nhà phố': 'nmt',
    'Căn hộ': 'cc',

}

LEGAL_STATUS_DIC = {
    'Giấy tay': 'gt',
    'Sổ đỏ': 'sh',
    '-': 'k',
    'Sổ hồng': 'sh',
    'HĐ mua bán' : 'hd',
}

PRO_DIRECTION_DIC = {
    '-': 'k',
    'Tây': 't',
    'Bắc': 'b',
    'Nam': 'n',
    'Đông': 'd',
    'Tây Nam': 'tn',
    'Đông Bắc': 'db',
    'Đông Nam': 'dn',
    'Tây Bắc': 'tb',
}