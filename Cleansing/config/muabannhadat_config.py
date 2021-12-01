source_mysql_host="172.16.0.167"
source_mysql_db="VN_REAL_RAW_"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_table="MUABANNHADAT"
des_mysql_host="172.16.0.167"
des_mysql_db="VN_REAL_CLEAN_"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_table="REAL_CLEAN_MUABANNHADAT"

# List of dictionaries
LAND_TYPE_DIC = {
    'Đất thổ cư': 'd', 	
    'Biệt thự': 'bt',
    'Nhà phố': 'nmt',
    'Townhouses':'nmt',
    'Nhà': 'nr',
    'Nhà riêng': 'nr',
    'Đất nông nghiệp': 'dnn',
    'Căn hộ': 'cc',
    'Đất nền': 'dn',
    'Other Houses':'k',
    'Mặt bằng văn phòng': 'vp',
    'Residential Land':'d',
    'Other Apartments':'k',
    'Kho xưởng': 'kx',
    'Mặt bằng bán lẻ': 'vp',
    'Other Land':'k',
    'Factories & Warehouses':'kx',
    'Villas':'bt',
    'Mặt bằng': 'vp', 	
    'Đất công nghiệp': 'dcn',
    'Shops':'ch',
    'Offices': 'vp', 	
    'Farm Land': 'dnn',
    'Commercial Land': 'dcn',
    'Other Commercial Spaces':'sh' 	
}

LEGAL_STATUS_DIC = {
    'Sổ hồng': 'sh',
    'Sổ đỏ': 'sh',
    'Red book': 'sh',
    'Pink book': 'sh',
    'Hợp đồng mua bán': 'hd',
    'Sales purchase contract': 'hd',
    'Không rõ': 'k',
    'Khác': 'k',
    'Giấy tay': 'gt',
    'Other': 'k',
    'Handwriting': 'gt',
    'Unknown': 'k',
    'data_properties.legal_document.': 'k'
}

PRO_DIRECTION_DIC = {
    'Đông Nam': 'dn',
    'Đông Bắc': 'db',
    'Nam': 'n',
    'Đông': 'd',
    'Tây Nam': 'tn',
    'Bắc': 'b',
    'Tây Bắc': 'tb',
    'South East': 'dn',
    'North East': 'db',
    'South': 'n',
    'Tây': 't',
    'East': 'd',
    'North': 'b', 	
    'North West': 'tb',
    'South West': 'db',
    'West': 't',
    'data_properties.direction.':'k'
}