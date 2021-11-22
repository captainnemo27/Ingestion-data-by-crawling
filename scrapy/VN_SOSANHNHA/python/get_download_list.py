import json
import sys
import csv

# ARGUMENTS
folder_name=sys.argv[1]
word_dir=sys.argv[2]

# CONSTANT
QUERY = "https://sosanhnha.com/search?"

# FOLDER LIST
delta_folder=word_dir+"/"+folder_name+"/DELTA"
json_folder=word_dir+"/"+"json"

# FILE LIST
category_list=delta_folder+"/category_list.temp"
country_file=json_folder+"/COUNTRY.json"
download_list_file=delta_folder+"/download_list.temp"

# CREATE CATEGORY LIST
category = []
with open(category_list, "r") as read_file:
    data = csv.reader(read_file, delimiter="\t")
    for line in data:
        category.append(line[0])

# CREATE CITY DICTIONARY
dic_country={}
with open(country_file) as json_file:
    country = json.load(json_file)
    list_city = country['data']

    for city in list_city:
        city_id = int(city['id']) + 1
        city_name = city['name']
        city_file = json_folder+"/"+city_name+".json"

        list_value=[]
        with open (city_file) as json_f:
            ct = json.load(json_f)
            list_district = ct['data']
            for district in range(1,len(list_district)):
                district_id = list_district[district]['dis_id']
                list_value.append(district_id)
        dic_country[city_id] = list_value

# CREATE DOWNLOAD_LIST
with open(download_list_file, "w") as write_file:
    for i in category:
        for key in dic_country:
            # if city is HCM, HN, DN, CT, BD
            if (key in [30,25,16,14,10]):
                for val in dic_country[key]:
                    url = QUERY+"iCat="+str(i)+"&iCit="+str(key)+"&iDis="+str(val)
                    name = str(i)+"-"+str(key)+"-"+str(val)
                    write_file.write(url + '\t' + name + '\n')
            else:
                url = QUERY+"iCat="+str(i)+"&iCit="+str(key)
                name = str(i)+"-"+str(key)+"-_"
                write_file.write(url + '\t' + name + '\n')


