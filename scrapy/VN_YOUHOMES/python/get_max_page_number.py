from urllib.request import urlopen
from urllib.request import Request
from lxml import etree
from io import StringIO, BytesIO
import youhomes_helper
import math


def get_number_in_text(text):
    total_page_position = text.find('totalPage')
    number = 0
    for i in range(total_page_position, total_page_position + 30):
        if text[i].isnumeric():
            number = number * 10 + int(text[i])
    return int(number)


def get_max_page_number():
    url_for_sale = []
    url_for_lease = []
    url_for_sale.append('https://youhomes.vn/mua/can-ho-26.html')
    url_for_sale.append('https://youhomes.vn/mua/nha-tho-cu-48.html')
    url_for_lease.append('https://youhomes.vn/thue/can-ho-36.html')
    url_for_lease.append('https://youhomes.vn/thue/nha-tho-cu-51.html')
    total_page = []

    for i in range(0, len(url_for_sale)):
        url_for_sale_ = Request(url_for_sale[i], headers={'User-Agent': 'Mozilla/5.0'})
        content_for_sale = urlopen(url_for_sale_).read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(str(content_for_sale)), parser)
        text = tree.xpath('//*[@id="contents"]/div[2]/div/script[3]')
        total_page.append(get_number_in_text(text[0].text))
    for i in range(0, len(url_for_lease)):
        url_for_lease_ = Request(url_for_lease[i], headers={'User-Agent': 'Mozilla/5.0'})
        content_for_lease = urlopen(url_for_lease_).read()
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(str(content_for_lease)), parser)
        text = tree.xpath('//*[@id="contents"]/div[2]/div/script[3]')
        total_page.append(get_number_in_text(text[0].text))
    return (total_page[0], total_page[1], total_page[2], total_page[3])


folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder, house_sale_folder, apartment_sale_folder, house_lease_folder, apartment_lease_folder = youhomes_helper.create_folder()
option_file = open(today_folder + '/option_file.txt', 'r')
value = option_file.read(1)
option_file.close()
with open(today_folder + '/max_page_number.txt', "w") as file:
    if (value == '1'):
        file.write(str(2) + '\n')
        file.write(str(2) + '\n')
        file.write(str(2) + '\n')
        file.write(str(2) + '\n')
    else:
        file.write(str(get_max_page_number()[0]) + '\n')
        file.write(str(get_max_page_number()[1]) + '\n')
        file.write(str(get_max_page_number()[2]) + '\n')
        file.write(str(get_max_page_number()[3]) + '\n')
file.close()
