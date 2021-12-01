source_mysql_host="172.16.0.167"
source_mysql_db="VN_REAL_RAW_"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_table="YOUHOMES"
des_mysql_host="172.16.0.167"
des_mysql_db="VN_REAL_CLEAN_"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_table="REAL_CLEAN_YOUHOMES"

# List of dictionaries
LAND_TYPE_DIC = {
    'Căn hộ Duplex': 'chcc',
    'Căn hộ Penthouse': 'ph',
    'OfficeTel': 'ot',
    'Căn hộ Studio': 'chst',
    'Nhà mặt phố': 'nmt',
    'Nhà riêng': 'nr',
    'Căn hộ chung cư': 'cc'
}

LEGAL_STATUS_DIC = {
    'Chưa có HĐMB': 'hd',
    'Hợp đồng 50 năm': 'hd50',
    'Chưa có sổ': 'gt',
    'Sổ hồng 50 năm': 'sh50',
    'Giấy tờ khác': 'k',
    'Sổ hồng': 'sh',
    'Hợp đồng mua bán': 'hd',
    'Sổ đỏ': 'sh',
}

PRO_DIRECTION_DIC = {
    'Đông Bắc - Đông Nam': 'db-dn',
    'Tây Bắc - Tây Nam': 'tb-tn',
    'Tây Bắc - Đông Bắc': 'tb-db',
    'Tây Nam - Đông Nam': 'tn-dn',
    'Tây': 't',
    'Bắc': 'b',
    'Nam': 'n',
    'Đông': 'd',
    '---': 'k',
    'Tây Nam': 'tn',
    'Tây Bắc': 'tb',
    'Đông Bắc': 'db',
    'Đông Nam': 'dn',
    'KXĐ': 'k',
    '': 'k'
}