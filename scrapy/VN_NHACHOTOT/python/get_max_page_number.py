import json
import wget
import chotot_helper


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

    url = 'https://gateway.chotot.com/v1/public/ad-listing?cg=1000&limit=50&o=0&page=1'
    wget.download(url, today_folder + '/page-mua-ban-bat-dong-san-1.json')
    file_name = today_folder + "/page-mua-ban-bat-dong-san-1.json"
    with open(file_name, "r") as file:
        read_data = json.load(file)
    file.close()
    return int(read_data["total"] / ads_per_page)


ads_per_page = 50
folder, today, today_folder, spider_folder, all_folder, delta_folder, list_mode = chotot_helper.create_folder()
option_file = open(today_folder + '/option_file.txt', 'r')
value = option_file.read(1)
option_file.close()
with open(today_folder + '/max_page_number.txt', "w") as file:
    if (value == '1'):
        file.write(str(2))
    else:
        file.write(str(get_max_page_number()))
file.close()
