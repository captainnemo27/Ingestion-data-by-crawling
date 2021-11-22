from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup
import revervn_helper
import re
import math


def get_max_page_number():
    '''
    Return site's max page numbers

        Parameters:
                None

        Returns:
                read_data["total"] / ads_per_page (int): Integer max page numbers
                ads_per_page is number ads on one page.
                read_data["total"] is the total number of ads for the site
    '''
    url_for_sale = Request('https://rever.vn/s/mua',  headers={'User-Agent': 'Mozilla/5.0'})
    url_for_lease = Request('https://rever.vn/s/thue',  headers={'User-Agent': 'Mozilla/5.0'})
    content_for_sale = urlopen(url_for_sale).read()
    content_for_lease = urlopen(url_for_lease).read()
    soup = BeautifulSoup(content_for_sale, 'html.parser')
    page_number_for_sale = soup.select(
        '#leads > div.results-sc > span > span > strong')[0].get_text()
    max_page_number_for_sale = re.findall('[0-9]+', page_number_for_sale)
    for i in range(len(max_page_number_for_sale)):
        max_page_number_for_sale[i] = int(max_page_number_for_sale[i])
    max_page_number_for_sale = max(max_page_number_for_sale)
    max_page_number_for_sale = math.ceil(max_page_number_for_sale / ads_per_page)
    soup = BeautifulSoup(content_for_lease, 'html.parser')
    page_number_for_lease = soup.select(
        '#leads > div.results-sc > span > span > strong')[0].get_text()
    max_page_number_for_lease = re.findall('[0-9]+', page_number_for_lease)
    for i in range(len(max_page_number_for_lease)):
        max_page_number_for_lease[i] = int(max_page_number_for_lease[i])
    max_page_number_for_lease = max(max_page_number_for_lease)
    max_page_number_for_lease = math.ceil(max_page_number_for_lease / ads_per_page)
    return (max_page_number_for_sale, max_page_number_for_lease)


ads_per_page = 20
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder = revervn_helper.create_folder()
option_file = open(today_folder + '/option_file.txt', 'r')
value = option_file.read(1)
option_file.close()
with open(today_folder + '/max_page_number.txt', "w") as file:
    if (value == '1'):
        file.write(str(2) + '\n')
        file.write(str(2) + '\n')
    else:
        file.write(str(get_max_page_number()[0]) + '\n')
        file.write(str(get_max_page_number()[1]) + '\n')
file.close()