#!/apps/lib/anaconda2/bin/python

from string import split
from os import listdir
import pandas as pd
import mysql.connector
from cryptography.fernet import Fernet

def get_pwd():
    file = open('secretkey.txt')
    key = file.read()

    cipher_suite = Fernet(key)

    pwd = cipher_suite.decrypt(
        "gAAAAABc-Sxbr3KqW2pKGF7zGGif_3P2VYQPLmyl20LR6HMhDJ7yZ_sawDMAuzMpJgrK9OnglChlJ2csZkPp0EnulLcGFZ1e8w==")

    return pwd

num_desktops = 18
connection = mysql.connector.connect(user='eris_cluster', password=get_pwd(),
                                         host='mysql2.dipr.partners.org',
                                         database='eris_cluster')

cur = connection.cursor()
cur.execute("SELECT * FROM rd_user_info ORDER BY date_time DESC LIMIT " + str(2 * num_desktops))

table = cur.fetchall()

cur.execute("SELECT * FROM rd_caps")

caps = cur.fetchall()

cur.close()
connection.close()

all_users = []
row_list = []
cap_list = []
overusers = []

# determines how many remote desktops each user is connected to and 
# returns a list of the users who are using more than one machine
def find_usage(users):
    for i in range(len(users)):
        mach_ct = 1
        for j in range(i+1, len(users)):
            if users[i] == users[j]:
                mach_ct += 1
        if mach_ct > 1:
            username = users[i]
            user_data = {'user': username, 'num_machines': mach_ct}
            overusers.append(user_data)

if table[num_desktops][0] == "rgs00":
  table = table[0:num_desktops]
else:
  for i in range(1, num_desktops):
    if table[i][0] == "rgs00":
      table = table[i:i+num_desktops]
      break

for row in table:
    node_name = row[0]
    node_users = row[2].split()
    for u in node_users:
        all_users.append(u)
    num_users = len(node_users)
    node_data = {'server': node_name, 'users': num_users}
    row_list.append(node_data)

for row in caps:
    node_name = row[0]
    node_cap = row[2]
    node_data = {'server': node_name, 'capacity': node_cap}
    cap_list.append(node_data)

find_usage(all_users)

df1 = pd.DataFrame()
df1 = pd.DataFrame(row_list)
df1 = df1[['server', 'users']]

rd_data = df1.to_json(orient='index')
#print data
with open('rd-data.json', 'w+') as file:
    file.write(rd_data)

df2 = pd.DataFrame()
df2 = pd.DataFrame(cap_list)
df2 = df2[['server', 'capacity']]

rd_caps = df2.to_json(orient='index')
#print data
with open('rd-caps.json', 'w+') as file:
    file.write(rd_caps)

if len(overusers) > 0:
    df3 = pd.DataFrame()
    df3 = pd.DataFrame(overusers)
    df3 = df3[['user', 'num_machines']]
    overuser_data = df3.to_json(orient='index')
    with open('overuser-data.json', 'w+') as file:
        file.write(overuser_data)
