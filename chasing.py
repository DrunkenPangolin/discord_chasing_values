import math
import numpy as np
import pandas as pd
import re

f = open("/home/sam/Coding/discord_chasing_values/chasing_raw.txt", "r")
txt = f.read()
f.close()

#username = input("Enter username here\n")

results = []
for i in range(1,5):
    print(i)
    results.extend(re.findall("(\d{2}/\d{2}/\d{4})(?:.*\n){" + str(i) + "}(\S*) \((\d+\.\d*\D%)", txt))

df = pd.DataFrame(results, columns=["Date", "Username", "EB"])

f = open("/home/sam/Coding/discord_chasing_values/conversion_table.txt", "r")
con_table_raw = f.read()
f.close()

con_table = str(con_table_raw.replace("\n",",").replace("\t",",")).split(",")

conversion_dict = {}
for i in range(1, len(con_table), 2):
    try:
        conversion_dict[con_table[i]] = int(con_table[i-1])
    except:
        conversion_dict[int(con_table[i])] = con_table[i-1]

def EB_long(EB):
    oom = re.findall("\d(\D)+%",EB)[0]
    eb_long = float(re.findall("^\d+.\d+",EB)[0])*(10**conversion_dict[oom])
    return eb_long

def role(EB):
    oom = int(math.log10(EB_long(EB)/100))
    role = conversion_dict[oom - oom % 3] + "farmer " + str(oom % 3 + 1)
    return role

df['EB_long (%)'] = df.apply(lambda row: EB_long(row.EB), axis = 1)

df['Role'] = df.apply(lambda row: role(row.EB), axis = 1)

df['Date'] = pd.to_datetime(df.Date, dayfirst=True)

df = df.sort_values(by="EB_long (%)")
df.to_csv("data.csv")


print(df[(df['Username'] == "DrunkenPangolin")])
