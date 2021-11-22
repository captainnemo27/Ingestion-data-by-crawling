import json
import sys
import os
import requests
import urllib
import unidecode

# # ARGUMENTS
word_dir=os.getcwd()

# # FOLDER LIST
json_dir=word_dir+"/"+"json"

# # FILE LIST
country_file=json_dir+"/COUNTRY.json"
dic_file=json_dir+"/DICTIONARY.json"
category_file=json_dir+"/category_list.temp"

# # API
city_api = "https://homedy.com/Common/CityAC"
district_ward_api = "https://homedy.com/Common/DistrictAC?CityId="
QUERY = "https://homedy.com/Search/GetUrl?KeyWord="


def parsing(url):
    with urllib.request.urlopen(url) as api:
        data = json.loads(api.read().decode())
        return data['Url']

if not os.path.exists(json_dir):
    os.makedirs(json_dir)

# DOWNLOAD COUNTRY.json
solditems = requests.get(city_api)
data = solditems.json()

if (os.path.exists(country_file) == False):
    with open(country_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False)


dic_country={}
with open(country_file) as json_file:
    country = json.load(json_file)
    list_city = country['Data']

    for city in list_city:
        city_id = int(city['Id'])
        
        city_name = unidecode.unidecode(city['Name'])
        city_name = city_name.replace(" ","_")
        city_file = json_dir+"/"+city_name+".json"

        url = district_ward_api+str(city_id)

        # DOWNLOAD city.json
        solditems = requests.get(url)
        data = solditems.json()
        if (os.path.exists(city_file) == False):
            with open(city_file, 'w') as f:
                json.dump(data, f, ensure_ascii=False)

        dic_country[city_id] = {}

        with open (city_file) as json_f:
            ct = json.load(json_f)
            list_district = ct['Data']

            for district in list_district:
                district_id = int(district['Id'])
                district_name = district['Name']

                dic_country[city_id][district_id] = {}
                list_ward_id = []
                list_street_id = []
                
                list_ward = district['Wards']
                for ward in list_ward:
                    ward_id = int(ward['Id'])
                    ward_name = ward['Name']
                    list_ward_id.append(ward_id)

                list_street = district['Streets']
                for street in list_street:
                    street_id = int(street['Id'])
                    street_name = street['Name']
                    list_street_id.append(street_id)

                dic_country[city_id][district_id] = (list_ward_id,list_street_id)

# DOWNLOAD DIC_COUNTRY.json
if (os.path.exists(dic_file) == False):
    with open(dic_file, 'w') as f:
        json.dump(dic_country, f, ensure_ascii=False)

with open(dic_file) as json_file:
    dic_country = json.load(json_file)

# CREATE DOWNLOAD_LIST
category = [1,2]
with open(category_file, "w") as write_file:
    for i in category:
        if (i==1):
            for city in dic_country:
                if city in ['1','2']:
                    for district in dic_country[city]:
                        for ward in dic_country[city][district][0]:
                            url = QUERY+"&SellType="+str(i)+"&CityId="+str(city)+"&DistrictId="+str(district)+"&WardId="+str(ward)#+"&StreetId="+str(street)
                            write_file.write(parsing(url)+ '\n')
                elif city in ['3','4']:
                    for district in dic_country[city]:
                        url = QUERY+"&SellType="+str(i)+"&CityId="+str(city)+"&DistrictId="+str(district)
                        write_file.write(parsing(url)+ '\n')
                else:
                    url = QUERY+"&SellType="+str(i)+"&CityId="+str(city)
                    write_file.write(parsing(url)+ '\n')
        else:
            for city in dic_country:
                if city in ['1','2']:
                    for district in dic_country[city]:
                        url = QUERY+"&SellType="+str(i)+"&CityId="+str(city)+"&DistrictId="+str(district)
                        write_file.write(parsing(url)+ '\n')
                else:
                    url = QUERY+"&SellType="+str(i)+"&CityId="+str(city)
                    write_file.write(parsing(url)+ '\n')
