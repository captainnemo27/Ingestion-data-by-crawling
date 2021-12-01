source_mysql_host="172.16.0.227"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="REAL_ESTATE_VN"
source_mysql_table="SOSANHNHA"
des_mysql_host="172.16.0.227"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL"
des_mysql_table="REAL_CLEAN_SOSANHNHA"

# List of dictionaries
LAND_TYPE_DIC = {
  'bán nhà riêng': 'nr',
  'cho thuê nhà trọ, phòng trọ':'npt',
  'nhà biệt thự, liền kề':'bt',
  'loại bất động sản khác':'k',
  'bán đất nền dự án':'dn',
  'cho thuê nhà riêng':'nr',
  'bán trang trại, khu nghỉ dưỡng':'ttnd',
  'nhà đất cho thuê':'d',
  'cho thuê loại bất động sản khác':'k',
  'bán đất':'d',
  'nhà riêng':'nr',
  'cửa hàng, ki ốt':'ch',
  'bán loại bất động sản khác':'k',
  'trang trại, khu nghỉ dưỡng':'ttnd',
  'nhà đất bán':'d',
  'homestay':'ttnd',
  'bán nhà biệt thự, liền kề':'bt',
  'nhà trọ, phòng trọ':'npt',
  'bán nhà mặt phố':'nmt',
  'căn hộ chung cư':'cc',
  'kho, nhà xưởng':'kx',
  'cho thuê kho, nhà xưởng, đất':'kx',
  'cho thuê cửa hàng, ki ốt':'ch',
  'cho thuê nhà mặt phố':'nmt',
  'nhà mặt phố':'nmt',
  'cho thuê căn hộ chung cư':'cc',
  'đất':'d',
  'nhà đất':'d',
  'kho, nhà xưởng, đất':'kx',
  'đất nền dự án':'dn',
  'bán kho, nhà xưởng':'kx',
  'bán căn hộ chung cư':'cc',
  'văn phòng':'vp',
  'cho thuê văn phòng':'vp'
}

LEGAL_STATUS_DIC = {
    'sổ đỏ chính chủ, cc': "sh",
    'cc, sổ hồng chính chủ': "sh",
    'sổ đỏ cc, sổ đỏ chính chủ, sổ hồng chính chủ': "sh",
    'sổ hồng chính chủ, cc, sổ hồng chính chủ': "sh",
    'sổ đỏ chính chủ, sổ hồng chính chủ, sổ hồng chính chủ': "sh",
    'sổ hồng chính chủ, cc': "sh",
    'cc': "gt",
    'sổ hồng chính chủ': "sh",
    'cc, sổ hồng chính chủ, sổ hồng chính chủ': "sh",
    'sổ đỏ chính chủ, cc, sổ hồng chính chủ': "sh",
    'sổ đỏ cc, sổ đỏ chính chủ': "sh",
    'sổ đỏ cc': "sh",
    'sổ hồng chính chủ, sổ đỏ chính chủ, sổ hồng chính chủ': "sh",
    'sổ hồng chính chủ, sổ hồng chính chủ, cc': "sh",
    'sổ đỏ chính chủ, sổ đỏ cc': "sh",
    'sổ đỏ cc, cc': "sh",
    'sổ đỏ chính chủ, sổ hồng chính chủ': "sh",
    'cc, sổ đỏ chính chủ': "sh",
    'cc, sổ đỏ chính chủ, sổ hồng chính chủ': "sh",
    'sổ hồng chính chủ, sổ đỏ chính chủ': "sh",
    'sổ đỏ cc, sổ hồng chính chủ': "sh",
    'cc, sổ đỏ cc': "sh",
    'sổ đỏ chính chủ': "sh",
    'sổ hồng chính chủ, sổ hồng chính chủ': "sh",
    'cc, sổ hồng chính chủ, sổ đỏ chính chủ': "sh"
}

PRO_DIRECTION_DIC = {
    None: None
}