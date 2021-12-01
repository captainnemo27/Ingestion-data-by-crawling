source_mysql_host="172.16.0.167"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="REAL_ESTATE_VN"
source_mysql_table="DIAOCONLINE"
des_mysql_host="172.16.0.167"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL"
des_mysql_table="REAL_CLEAN_DIAOCONLINE"

# List of dictionaries
LAND_TYPE_DIC = {
    'Đất cho sản xuất':'dnn',
    'Đất lâm nghiệp':'dnn',
    'Nhà hàng - Khách sạn':'nhks',
    'Đất nông nghiệp':'dnn',
    'Đất vườn':'dnn',
    'Nhà tạm':'nr',
    'Nhà Kho - Xưởng':'kx',
    'Đường nội bộ':'nr',
    'Văn phòng':'vp',
    'Căn hộ dich vụ':'chdv',
    'Mặt bằng - Cửa hàng':'vp',
    'Đất dự án - Quy hoạch':'dn',
    'Khách Sạn - Nhà Phố':'nhks',
    'Phòng trọ':'npt',
    'Villa - Biệt thự':'bt',
    'Căn hộ chung cư': 'cc',
    'Căn hộ cao cấp': 'chcc',
    'Đất ở - Đất thổ cư': 'd',
    'Nhà phố':'nmt',
}

PRO_DIRECTION_DIC = {
    'Đông Nam' :'dn', 
    'Nam': 'n', 
    'Tây': 't', 
    'Ðông': 'd', 
    'Bắc': 'b', 
    'Đông Bắc': 'db',
    'Tây Nam': 'tn', 
    'Không xác định':'k', 
    'Tây Bắc':'tb'
}

LEGAL_STATUS_DIC = {
    'Sổ hồng': 'sh', 
    'Hợp đồng': 'hd', 
    'Giấy tờ hợp lệ': 'gt', 
    'Giấy đỏ': 'sh',
    'Giấy tay': 'gt', 
    'Chủ quyền tư nhân': 'gt', 
    'Đang hợp thức hóa': 'gt',
    'Không xác định': 'k'
}