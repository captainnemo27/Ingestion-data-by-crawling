source_mysql_host="172.16.0.227"
source_mysql_db="VN_REAL_RAW_"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_table="BATDONGSANCOMVN"
des_mysql_host="172.16.0.227"
des_mysql_db="VN_REAL_CLEAN_"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_table="REAL_CLEAN_BATDONGSANCOMVN"

# List of dictionaries
LAND_TYPE_DIC = {
    'Mua loại bất động sản khác': 'k',
    "Mua kho, nhà xưởng": 'kx',
    "Mua nhà biệt thự, liền kề (nhà trong dự án quy hoạch)":'bt',
    'Mua nhà mặt phố (nhà mặt tiền trên các tuyến phố)': 'nmt',
    'Cho thuê loại bất động sản khác': 'k',
    'Mua căn hộ chung cư': 'cc',
    'Mua nhà riêng': 'nr',
    'Mua đất': 'd',
    'loại bất động sản khác': 'k',
    'Mua đất nền dự án (đất trong dự án quy hoạch)': 'dn',
    "Bán trang trại, khu nghỉ dưỡng":'ttnd',
    "Cho thuê cửa hàng, ki ốt": 'ch',
    "Bán kho, nhà xưởng": 'kx',
    "Cho thuê kho, nhà xưởng, đất": 'kx',
    'Bán loại bất động sản khác': 'k',
    "cửa hàng, ki ốt": 'ch',
    "kho, nhà xưởng, đất": 'kx',
    'Cho thuê văn phòng': 'vp',
    "nhà trọ, phòng trọ": 'npt',
    "Cho thuê nhà trọ, phòng trọ": 'npt',
    'Cho thuê nhà riêng': 'nr',
    'văn phòng': 'vp',
    'Cho thuê nhà mặt phố': 'nmt',
    'nhà riêng': 'nr',
    'nhà mặt phố': 'nmt',
    'Cho thuê căn hộ chung cư': 'cc',
    "Bán nhà biệt thự, liền kề (nhà trong dự án quy hoạch)":'bt',
    'căn hộ chung cư': 'cc',
    'Bán đất nền dự án (đất trong dự án quy hoạch)': 'dn',
    'Bán nhà mặt phố (nhà mặt tiền trên các tuyến phố)': 'nmt',
    'Bán căn hộ chung cư': 'cc',
    'Bán nhà riêng': 'nr',
    'Bán đất': 'd',
    'đất':'d',
}

LEGAL_STATUS_DIC = {
    'SHR': 'sh',
    'Hợp đồng mua bán': 'hd',
    'SĐCC': 'sh',
    'Sổ đỏ': 'sh',
    'Có sổ': 'sh',
    'Có sổ đỏ': 'sh',
    'Sổ hồng': 'sh',
    'Sổ hồng chính chủ': 'sh',
    'Sổ hồng riêng': 'sh',
    'Đã có sổ hồng': 'sh',
    'Đã có sổ đỏ': 'sh',
    'Đã có sổ': 'sh',
    'Sổ đỏ chính chủ': 'sh',
    'Sổ sẵn':'sh',
    'Sổ Hồng Riêng':'sh',
    'Đã có sổ riêng':'sh',
    'Giấy tờ hợp lệ':'gt',
    'SH':'sh',
    'SĐ':'sh',
    'HĐMB': 'hd',
    'Sổ vĩnh viễn':'sh',
    'Sổ đỏ chung':'shc',
    'Sổ hồng chung':'shc',
    'Sổ vuông đẹp':'sh',
    'SHCC':'sh',
    'Bìa hồng':'sh',
    'Sổ': 'sh',
    'Rõ ràng': 'da',
    'Đầy đủ': 'sh',
    'Có': 'sh',
    'chính chủ': 'gt',
    'sổ riêng': 'sh',
}

PRO_DIRECTION_DIC = {
    'Tây': 't',
    'Bắc': 'b',
    'Đông': 'd',
    'Nam': 'n',
    'Tây-Nam': 'tn',
    'Đông-Bắc': 'db',
    'Tây-Bắc': 'tb',
    'Đông-Nam': 'dn',
}
