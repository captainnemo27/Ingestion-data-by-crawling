source_mysql_host="172.16.0.227"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="REAL_ESTATE_VN"
source_mysql_table="RONGBAY"
des_mysql_host="172.16.0.227"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL"
des_mysql_table="REAL_CLEAN_RONGBAY"

# List of dictionaries
LAND_TYPE_DIC = {
    "Dịch vụ sửa chữa, lắp đặt":'dvld',
    'Nhà loại khác':'k',
    'Nhà tập thể':'cc',
    'Ở ghép':'npt',
    'Mặt bằng/ Đất trống':'d',
    'Biệt thự/ Liền kề/ Phân lô':'bt',
    'Xưởng/ Kho/Trang trại':'kx',
    'Cửa hàng/ Ki ốt/ Mặt bằng':'ch',
    'Sang nhượng':'vp',
    'Du lịch nghỉ dưỡng':'chcd',
    "Kho, Xưởng":'kx',
    'Khác':'k',
    'Nhà mặt phố/ ngõ':'nmt',
    "MB kinh doanh,Cửa hàng,Kios":'vp',
    'Cao ốc văn phòng':'vp',
    'Tập thể/ Chung cư/ CC mini':'cc',
    'Nhà trọ/ Phòng trọ':'npt',
    'Căn hộ/ Chung cư cao cấp':'chcc',
    'Nhà riêng/ nguyên căn':'nr',
    'Nhà mặt phố':'nmt',
    'Căn hộ chung cư':'cc',
    'Biệt thự/Liền kề/Đất nền':'bt',
    'Nhà riêng':'nr',
    'Đất ở/ Đất thổ cư':'d',
}

LEGAL_STATUS_DIC = {
    'Sổ đỏ chính chủ':'sh',
    'Văn bản chuyển nhượng':'gt',
    'Chưa có sổ':'gt',
    'Khác':'k',
    'Hợp đồng mua bán':'hd',
    'Có sổ hồng':'sh',
    'Có sổ đỏ/ hồng':'sh',  
}

PRO_DIRECTION_DIC = {
    'Đông Bắc': "db",
    'Tây Bắc': "tb",
    'Đông Nam': "dn",
    'Tây Nam': "tn",
    'Tây': "t",
    'Bắc': "b",
    'Nam' : "n",
    'Đông': "d",
}