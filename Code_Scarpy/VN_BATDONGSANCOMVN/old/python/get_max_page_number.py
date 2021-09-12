from lxml import etree
from io import StringIO, BytesIO
import batdongsancomvn_helper
import math
from bs4 import BeautifulSoup
import pycurl
from io import BytesIO 


def get_all_ads_in_site(link_site):
    b_obj = BytesIO() 
    crl = pycurl.Curl() 
    # Set URL value
    crl.setopt(crl.URL, link_site)
    crl.setopt(pycurl.PROXY, "http://172.16.1.11:3128/")
    # Write bytes that are utf-8 encodeds
    crl.setopt(crl.WRITEDATA, b_obj)
    # Perform a file transfer 
    crl.perform() 
    # End curl session
    crl.close()
    # Get the content stored in the BytesIO object (in byte characters) 
    content = b_obj.getvalue()
    soup = BeautifulSoup(content.decode('utf8'), 'lxml')
    if link_site.find("can-mua-can-thue") >= 0:
        span_tag = soup.find("span", attrs={"class": "greencolor"}).get_text()
    else:
        span_tag = soup.find("span", attrs={"id": "count-number"}).get_text()
    all_ads = int(span_tag.replace(",", ""))
    return all_ads


def get_max_page_number():
    url_for_sale = 'https://batdongsan.com.vn/nha-dat-ban'
    url_for_lease = 'https://batdongsan.com.vn/nha-dat-cho-thue'
    url_to_buy_to_lease = 'https://batdongsan.com.vn/can-mua-can-thue'
    total_page = []
    total_page.append(math.ceil(get_all_ads_in_site(url_for_sale)/ads_per_page))
    total_page.append(math.ceil(get_all_ads_in_site(url_for_lease)/ads_per_page))
    total_page.append(math.ceil(get_all_ads_in_site(url_to_buy_to_lease)/ads_per_page))
    return (total_page[0], total_page[1], total_page[2])


ads_per_page = 20
folder, today, today_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder, to_buy_to_lease_folder = batdongsancomvn_helper.create_folder()
option_file = open(today_folder + '/option_file.txt', 'r')
value = option_file.read(1)
option_file.close()
with open(today_folder + '/max_page_number.txt', "w") as file:
    if (value == '1'):
        file.write(str(2) + '\n')
        file.write(str(2) + '\n')
        file.write(str(2) + '\n')
    else:
        file.write(str(get_max_page_number()[0]) + '\n')
        file.write(str(get_max_page_number()[1]) + '\n')
        file.write(str(get_max_page_number()[2]) + '\n')
file.close()
