# This file extracts the data from the csv files and puts it into JSON files

import pandas as pd
import os
import math
import json

# you might want to switch to the directory this file is located in manually
os.chdir("D://github_repos/Wahldaten/Landtagswahlen/Wahlkreise")

# make dicts
data_json = {'copyright': "Daten wurden mir durch das Innenministerium BaWü von der Landeswahlleiterin BaWü überlassen. Dabei gab es keine Angaben zu Lizenz oder Nutzungbeschränkungen.", "status": "05.03.2020", "data": {}}

# thirst rows to ignore (start with 1, include header)
rows_empty = 3

# read csv file 
data = pd.read_excel("src/Wahlkreiseinteilung_LW.xlsx",encoding='ISO-8859-1',sep=";",skiprows=lambda x: x < rows_empty)

# collect by gemeinde
for index,row in data.iterrows():
    if not math.isnan(row[1]):
        data_json["data"][str(row[4])] = {"wahlkreis_bezeichnung": str(row[6]), "wahlkreis_nummer": str(int(row[5])), "gemeinde_schluessel": str(int(row[3])), "kreis":str(row[2]), "kreis_schluessel": str(int(row[1]))}

with open('wahlkreise_ltw_gemeinde.json', 'w',encoding="utf-8") as fp:
    json.dump(data_json, fp,ensure_ascii=False)

# make dicts
data_json = {'copyright': "Daten wurden mir durch das Innenministerium BaWü von der Landeswahlleiterin BaWü überlassen. Dabei gab es keine Angaben zu Lizenz oder Nutzungbeschränkungen.", "status": "05.03.2020", "data": {}}

# collect by wahlkreis
for index,row in data.iterrows():
    if not math.isnan(row[1]):
        if str(row[6]) in data_json["data"]:
            data_json["data"][str(row[6])]["gemeinde_schluessel"].append(str(int(row[3])))
            data_json["data"][str(row[6])]["gemeinde"].append(str(row[4]))
        else:
            data_json["data"][str(row[6])] = {"wahlkreis_nummer": str(int(row[5])), "gemeinde": [str(row[4])], "gemeinde_schluessel": [str(int(row[3]))]}

with open('wahlkreise_ltw_wahlkreis.json', 'w',encoding="utf-8") as fp:
    json.dump(data_json, fp,ensure_ascii=False)

#### FROM HERE WE WILL USE THE DATA ABOVE TO MAP PLZ TO WAHLKREISE ####

# thirst rows to ignore (start with 1, include header)
rows_empty = 3

# read csv file 
data = pd.read_excel("src/Gemeindeverzeichnis.xlsx",encoding='ISO-8859-1',skiprows=lambda x: x < rows_empty,header=None)
data2 = {}
with open('wahlkreise_ltw_gemeinde.json', 'r', encoding="utf-8") as outfile:
    data2 = json.load(outfile)

# make dicts
data_json = {'copyright': "Daten wurden mir durch das Innenministerium BaWü von der Landeswahlleiterin BaWü überlassen. Dabei gab es keine Angaben zu Lizenz oder Nutzungbeschränkungen.", "status": "05.03.2020", "data": {}}

# collect by plz
for index,row in data.iterrows():
    if not math.isnan(row[0]):

        try:
            data_json["data"][str(int(row[7]))] = {"gemeinde": str(row[8]), "gemeinde_schluessel": str(int(row[2])), "gemeinde_schluessel_bundeseinheitlich": str(int(row[5])), "wahlkreis_bezeichnung": data2["data"][str(row[8])]["wahlkreis_bezeichnung"], "wahlkreis_nummer": data2["data"][str(row[8])]["wahlkreis_nummer"], "kreis": data2["data"][str(row[8])]["kreis"], "kreis_schluessel": data2["data"][str(row[8])]["kreis_schluessel"]}
        except:
            print(str(row[8]))

with open('wahlkreise_ltw_plz.json', 'w',encoding="utf-8") as fp:
    json.dump(data_json, fp,ensure_ascii=False)