# This file extracts the data from the csv files and puts it into JSON files

import pandas as pd
import os
import math
import json

# you might want to switch to the directory this file is located in manually
os.chdir("D://github_repos/Wahldaten/Landtagswahlen/Wahlkreise_SN")

# make dicts
data_json = {'copyright': "Daten wurden uns durch den Landeswahlleiter überlassen. Dabei gab es keine Angaben zu Lizenz oder Nutzungbeschränkungen.", "status": "26.05.2020", "data": {}}

# thirst rows to ignore (start with 1, include header)
rows_empty = 2

# read csv file 
data = pd.read_excel("src/Wahlkreiseinteilung_LW_Sachsen.xlsx",encoding='ISO-8859-1',sep=";",skiprows=lambda x: x < rows_empty, converters={'PLZ': lambda x: str(x), 10: lambda x: str(x), 11: lambda x: str(x), 12: lambda x: str(x), 13: lambda x: str(x), 14: lambda x: str(x), 15: lambda x: str(x)})
data = data.fillna(0)

# collect by plz
for index,row in data.iterrows():
    if not math.isnan(row["LTWK 2019"]):
        # check if there are multiple PLZs
        for i in ["PLZ", 10, 11, 12, 13, 14, 15]:
            if not row[i] == 0:
                data_json["data"][str(row[i])] = {"plz": str(row[i]),"wahlkreis_bezeichnung": str(row["LTWK-Bezeichnung"]), "wahlkreis_nummer": str(int(row["LTWK 2019"])), "kreis":str(row["Landkreisbezeichnung"]), "kreis_schluessel": str(int(row["LK-Schlüssel"])), "gemeinde_schluessel": str(row["AGS"]), "gemeinde": str(row["Gemeindename"])}
        
with open('wahlkreise_ltw-sn_plz.json', 'w',encoding="utf-8") as fp:
    json.dump(data_json, fp,ensure_ascii=False)

# make dicts
data_json = {'copyright': "Daten wurden uns durch den Landeswahlleiter überlassen. Dabei gab es keine Angaben zu Lizenz oder Nutzungbeschränkungen.", "status": "26.05.2020", "data": {}}

#collect by gemeinde
for index,row in data.iterrows():
    if not math.isnan(row["LTWK 2019"]):
        # check if there are multiple PLZs
        for i in ["PLZ", 10, 11, 12, 13, 14, 15]:
            if not row[i] == 0:
                data_json["data"][str(row["Gemeindename"])] = {"gemeinde": str(row["Gemeindename"]), "wahlkreis_bezeichnung": str(row["LTWK-Bezeichnung"]), "wahlkreis_nummer": str(int(row["LTWK 2019"])), "kreis":str(row["Landkreisbezeichnung"]), "kreis_schluessel": str(int(row["LK-Schlüssel"])), "gemeinde_schluessel": str(row["AGS"]), "plz": str(row[i])}
        
with open('wahlkreise_ltw-sn_gemeinde.json', 'w',encoding="utf-8") as fp:
    json.dump(data_json, fp,ensure_ascii=False)

# make dicts
data_json = {'copyright': "Daten wurden uns durch den Landeswahlleiter überlassen. Dabei gab es keine Angaben zu Lizenz oder Nutzungbeschränkungen.", "status": "26.05.2020", "data": {}}

#collect by Wahlkreis
for index,row in data.iterrows():
    if not math.isnan(row["LTWK 2019"]):
        plzs = []
        for i in ["PLZ", 10, 11, 12, 13, 14, 15]:
            if not row[i] == 0:
                if str(row["LTWK-Bezeichnung"]) in data_json["data"]:
                    data_json["data"][str(row["LTWK-Bezeichnung"])]["plz"].append(str(row[i]))
                    data_json["data"][str(row["LTWK-Bezeichnung"])]["gemeinde"].append(str(row["Gemeindename"]))
                    data_json["data"][str(row["LTWK-Bezeichnung"])]["gemeinde_schluessel"].append(str(row["AGS"]))
                else:
                    data_json["data"][str(row["LTWK-Bezeichnung"])] = {"wahlkreis_bezeichnung": str(row["LTWK-Bezeichnung"]), "wahlkreis_nummer": str(int(row["LTWK 2019"])), "kreis":str(row["Landkreisbezeichnung"]), "kreis_schluessel": str(int(row["LK-Schlüssel"])), "gemeinde_schluessel": [str(row["AGS"])], "plz": [str(row[i])], "gemeinde":[str(row["Gemeindename"])]}
            
with open('wahlkreise_ltw-sn_wahlkreis.json', 'w',encoding="utf-8") as fp:
    json.dump(data_json, fp,ensure_ascii=False)