source_mysql_host="172.16.0.227"
source_mysql_db="REAL_ESTATE_VN"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_table="NHACHOTOT"
des_mysql_host="172.16.0.227"
des_mysql_db="VN_REAL"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_table="REAL_CLEAN_NHACHOTOT"

# List of dictionaries
LAND_TYPE_DIC = {
    'Dịch vụ':'k',
    'Căn hộ/Chung cư': 'cc',
    'Mặt bằng kinh doanh': 'vp',
    'Nhà ở': 'nr',
    'Tập thể':'cc',
    'Đất': 'd',
    'Penthouse': 'ph',
    'Tập thể, cư xá': 'cc',
    'Duplex': 'chcc',
    'Officetel': 'ot',
    'Đất công nghiệp': 'dcn',
    'Căn hộ dịch vụ':'chdv',
    'Nhà biệt thự': 'bt',
    'Văn phòng': 'vp',
    'Nhà phố liền kề': 'nmt',
    'Căn hộ dịch vụ, mini':'chdv',
    'Nhà mặt phố':'nmt',
    'Đất nông nghiệp': 'dnn',
    'Đất nền dự án': 'dn',
    'Nhà ngõ': 'nr',
    'Phòng trọ': 'npt',
    'Văn phòng, Mặt bằng kinh doanh': 'vp',
    'Chung cư': 'cc',
    'Nhà mặt phố, mặt tiền': 'nmt',
    'Đất thổ cư' : 'd',
    'Nhà ngõ, hẻm': 'nr'
}


LEGAL_STATUS_DIC = {
    'Giấy tờ khác': 'gt',
    'Đang chờ sổ': 'gt',
    'Đã có sổ': 'sh'
}

PRO_DIRECTION_DIC = {
    'Bắc': 'b',
    'Tây': 't',
    'Nam': 'n',
    'Tây Nam': 'tn',
    'Tây Bắc': 'tb',
    'Đông': 'd',
    'Đông Bắc': 'db',
    'Đông Nam': 'dn'
}