source_mysql_host="172.16.0.167"
source_mysql_user="root"
source_mysql_password="123456789"
source_mysql_db="VN_REAL_RAW_"
source_mysql_table="MOGIVN"
des_mysql_host="172.16.0.167"
des_mysql_user="root"
des_mysql_password="123456789"
des_mysql_db="VN_REAL_CLEAN_"
des_mysql_table="REAL_CLEAN_MOGIVN"

# List of dictionaries
LAND_TYPE_DIC = {'thue-nha-mat-tien-pho': 'nmt',
 'thue-phong-tro-khu-nha-tro': 'npt',
 'thue-nha-hem-ngo': 'nh',
 'thue-van-phong-nha-rieng-can-ho': 'vp',
 'thue-phong-tro-loi-di-rieng': 'npt',
 'mua-nha-mat-tien-pho': 'nmt',
 'thue-can-ho-chung-cu': 'cc',
 'mua-nha-hem-ngo': 'nh',
 'thue-nha-biet-thu-lien-ke': 'bt',
 'thue-mat-bang-cua-hang-shop-nhieu-muc-dich': 'ch',
 'thue-nha-xuong': 'kx',
 'thue-duong-noi-bo': 'd',
 'mua-dat-tho-cu': 'd',
 'thue-cua-hang-shop-shophouse': 'ch',
 'thue-van-phong-toa-nha-cao-oc': 'vp',
 'mua-can-ho-chung-cu': 'cc',
 'thue-can-ho-dich-vu': 'chdv',
 'thue-phong-tro-o-chung-chu': 'npt',
 'mua-nha-biet-thu-lien-ke': 'bt',
 'thue-nha-kho': 'kx',
 'thue-mat-bang-cua-hang-shop-thoi-trang-my-pham-thuoc': 'ch',
 'thue-van-phong-ao-tron-goi': 'vp',
 'thue-can-ho-officetel': 'ot',
 'thue-phong-tro-o-ghep': 'npt',
 'thue-van-phong-officetel': 'vp',
 'mua-duong-noi-bo': 'd',
 'thue-mat-bang-cua-hang-shop-quan-an-nha-hang': 'ch',
 'thue-mat-bang-cua-hang-shop-spa-tiem-toc-nail': 'ch',
 'thue-dat-trong': 'dnn',
 'thue-can-ho-penthouse': 'ph',
 'thue-mat-bang-cua-hang-shop-cafe-do-uong': 'ch',
 'mua-dat-nen-du-an': 'dn',
 'thue-van-phong-tt-thuong-mai': 'vp',
 'mua-cua-hang-shop-shophouse': 'ch',
 'thue-bai-de-xe': 'd',
 'mua-mat-bang-cua-hang-shop-nhieu-muc-dich': 'ch',
 'mua-mat-bang-cua-hang-shop-thoi-trang-my-pham-thuoc': 'ch',
 'mua-dat-kho-xuong': 'kx',
 'mua-can-ho-dich-vu': 'chdv',
 'mua-can-ho-penthouse': 'ph',
 'mua-dat-nong-nghiep': 'dnn',
 'mua-can-ho-officetel': 'ot',
 'mua-mat-bang-cua-hang-shop-quan-an-nha-hang': 'ch',
 'mua-mat-bang-cua-hang-shop-cafe-do-uong': 'ch',
 'mua-mat-bang-cua-hang-shop-spa-tiem-toc-nail': 'ch',
 'thue-can-ho-tap-the-cu-xa': 'cc',
 'mua-can-ho-tap-the-cu-xa': 'cc'}

LEGAL_STATUS_DIC = {
    "không xác định" : "k",
    "sổ hồng" : "sh",
    "hợp đồng mua bán" : "hd",
    "giấy tờ hợp lệ" : "gt",
    "sổ đỏ": "sh",
    "giấy tờ viết tay": "gt",
    "không xác định" : "k"
}

PRO_DIRECTION_DIC = {
    "nam" : "n",
    "bắc" : "b",
    "đông": "d",
    "tây": "t",
    "đông nam" : "dn",
    "đông bắc": "db",
    "tây bắc": "tb",
    "tây nam": "tn",
    "không xác định": "k"
}