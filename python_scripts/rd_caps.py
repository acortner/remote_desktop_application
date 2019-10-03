#!/apps/lib/anaconda2/bin/python

# This script will attempt to ping all of the NoMachine Remote Desktops available on ERISOne
# It will return a list of available machines that will be send to rd_data.py

from subprocess import call, Popen, PIPE
from string import split
import datetime
from os import listdir
import mysql.connector
from cryptography.fernet import Fernet


def getdate():
    """Returns the current datetime stamp formatted Y-%m-%d %H:%M:%S

    :return: the correctly formatted datetime stamp
    :rtype: str
    """
    currentDT = datetime.datetime.now()
    formatedDT = currentDT.strftime("%Y-%m-%d %H:%M:%S")

    return formatedDT


def shell_cmd(command):
    """Executes the given command within terminal and returns the output as a string

    :param command: the command that will be executed in the shell
    :type command: str

    :return: the output of the command
    :rtype: str
    """
    process = Popen(command, stdout=PIPE, shell=True)
    return process.communicate()[0].strip()


def get_pwd():
    file = open('secretkey.txt')
    key = file.read()

    cipher_suite = Fernet(key)

    pwd = cipher_suite.decrypt(
        "gAAAAABc-Sxbr3KqW2pKGF7zGGif_3P2VYQPLmyl20LR6HMhDJ7yZ_sawDMAuzMpJgrK9OnglChlJ2csZkPp0EnulLcGFZ1e8w==")

    return pwd

rd_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16]
grx_numbers = [3, 4, 5, 6]

capacities = []
subscription_cmd_quote = "\"/usr/NX/bin/nxserver --version\""

sql = "INSERT INTO rd_caps (machine_name, date_time, capacity) VALUES (%s, %s, %s)"

connection = mysql.connector.connect(user='eris_cluster', password=get_pwd(),
                                         host='mysql2.dipr.partners.org',
                                         database='eris_cluster')
cur = connection.cursor()
cur.execute("DELETE FROM rd_caps")
connection.commit()

# Checks all of the rgs machines 
for num in rd_numbers:
    rd_name = "rgs%02d" % num
    rd_cmd = " ".join(["ssh", rd_name, subscription_cmd_quote, "2>/dev/null"])
    subscription = shell_cmd(rd_cmd)
    if "Terminal" in subscription:
        items = [rd_name, getdate(), 100]
        cur.execute(sql, items)
	connection.commit()
    elif "Workstation" in subscription:
        items = [rd_name, getdate(), 4]
        cur.execute(sql, items)
	connection.commit()
    elif "Small Business" in subscription:
        items = [rd_name, getdate(), 10]
        cur.execute(sql, items)
	connection.commit()
    else:
        items = [rd_name, getdate(), 0]
        cur.execute(sql, items)
	connection.commit()
    
# Checks all of the grx machines 
for num in grx_numbers:
    grx_name = "grx%02d" % num
    grx_cmd = " ".join(["ssh", grx_name, subscription_cmd_quote, "2>/dev/null"])
    subscription = shell_cmd(grx_cmd)
    if "Terminal" in subscription:
        items = [grx_name, getdate(), 100]
        cur.execute(sql, items)
	connection.commit()
    elif "Workstation" in subscription:
        items = [grx_name, getdate(), 4]
        cur.execute(sql, items)
	connection.commit()
    elif "Small Business" in subscription:
        items = [grx_name, getdate(), 10]
        cur.execute(sql, items)
	connection.commit()
    else:
        items = [grx_name, getdate(), 0]
        cur.execute(sql, items)
	connection.commit()

cur.close()
connection.close()
