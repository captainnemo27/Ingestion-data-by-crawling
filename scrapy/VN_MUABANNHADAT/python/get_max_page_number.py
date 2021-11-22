from urllib.request import Request, urlopen
import muabannhadat_helper
import json


def get_page_number_in_site(link_site):
    url = Request(link_site, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(url) as response:
        content = response.read()
        json_file = json.loads(content)
        page_number = json_file['meta']['last_page']
        return page_number


def get_max_page_number():
    url_for_sale = 'https://api.muabannhadat.vn/v1/listings?offer_type=sell' 
    url_for_lease = 'https://api.muabannhadat.vn/v1/listings?offer_type=rent'
    total_page = []
    total_page.append(get_page_number_in_site(url_for_sale))
    total_page.append(get_page_number_in_site(url_for_lease))
    return (total_page[0], total_page[1])


ads_per_page = 15
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode, sale_folder, lease_folder = muabannhadat_helper.create_folder()
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
# get_max_page_number()