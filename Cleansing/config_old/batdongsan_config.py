source_mysql_host="172.16.0.167"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="REAL_ESTATE_VN"
source_mysql_table="BATDONGSAN"
des_mysql_host="172.16.0.167"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL"
des_mysql_table="REAL_CLEAN_BATDONGSAN"

# List of dictionaries
LAND_TYPE_DIC =  {
        'Căn hộCao cấp': 'chcc',
        "Nhà trọ, ph��ng trọ":'npt', 
        'Căn hộ Caocấp': 'chcc',
        'Đ���t nền': 'dn',
        'V��n phòng': 'vp',
        'Biệt thự song lập': 'bt',
        'Co-working Space':'vp',
        'Biệt thự đơn lập':'bt',
        'TT Thương mại': 'sh',
        'Đất nghỉ dưỡng': 'ttnd',
        'Căn hộ Officetel': 'ot',
        'Căn hộ Penthouse':'ph',
        'Đất công nghiệp': 'dcn',
        'Mặt bằng bán lẻ': 'vp',
        'Khách sạn': 'nhks',
        'Căn hộ Condotel': 'chcd',
        'Căn hộ rẻ': 'ch',
        'Nhà xưởng kho bãi': 'kx',
        'Căn hộ Tập thể': 'cc',
        'Nhà xưởng':'kx',
        'Cửa hàng kiot': 'ch',
        "Nhà trọ, phòng trọ":'npt',
        'Căn hộ mini': 'ch',
        'Đất trang trại': 'ttnd',
        'Bất động sản khác':'k',
        'Văn phòng': 'vp',
        'Biệt thự liền kề':'bt',
        'Biệt thự nghỉ dưỡng': 'bt',
        'Nhà phố Shophouse':'sh',
        'Nhà rẻ':'nr',
        'Nhà biệt thự': 'bt',
        'Căn hộ trung cấp': 'ch',
        'Đất nông lâm nghiệp': 'dnn',
        'Căn hộ chung cư': 'cc',
        'Đất nền': 'dn', 
        'Căn hộ Cao cấp': 'chcc',
        'Đất nền dự án': 'dn', 
        'Đất nền khu dân cư':'dn', 
        'Nhà mặt phố': 'nmt',
        'Nhà riêng': 'nr',
}

PRO_DIRECTION_DIC = {
       'Đông-Nam' : 'dn', 'Đông-Bắc': 'db', 'Tây-Nam': 'tn', 'Tây': 't', 'Nam': 'n', 'Đông': 'd',
       'Tây-Bắc': 'tb', 'Bắc': 'b'
}

LEGAL_STATUS_DIC = {
       'Sổ đỏ': 'sh', 
       'Sổ hồng': 'sh', 
       'Giấy phép xây dựng': 'gt', 
       'S�� đỏ': 'sh',
       'Chưa rõ pháp lý': 'k',
       'Sổ hô��ng': 'sh',
       'Sổhồng': 'sh'
}
