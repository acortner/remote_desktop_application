#!/apps/lib/anaconda2/bin/python
"""Remote Desktop User Data

    This script connects to all remote desktops, and records the number of active users.
    Remote Desktop List:
"""

from subprocess import Popen, PIPE
import datetime
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


def database_commit(items):
    """Adds a row the the remote desktop user database, and commits the changes

    :param items:
    :type items: list
    :raises ValueError: If the given list of items has more or less than two items.
    """
    if len(items) != 3:
        raise ValueError("The given parameter is not of list length 2.")

    val = items

    sql = "INSERT INTO rd_user_info (machine_name, date_time, users) VALUES (%s, %s, %s)"

    connection = mysql.connector.connect(user='eris_cluster', password=get_pwd(),
                                         host='mysql2.dipr.partners.org',
                                         database='eris_cluster')
    cur = connection.cursor()
    cur.execute(sql, val)
    connection.commit()

    # Always close your connections

def get_rd_data():
    """Connects to every remote desktop and records the list of users in the database
    """
    connection = mysql.connector.connect(user='eris_cluster', password=get_pwd(),
                                         host='mysql2.dipr.partners.org',
                                         database='eris_cluster')

    timestamp = getdate()
    if timestamp.split()[1][0:5] == "00:00":
        cur = connection.cursor()
        cur.execute("DELETE FROM rd_user_info")
        connection.commit()
    users_list_cmd_quote = "\"ps auxw | grep nxnode.bin | grep -v grep | \
    grep -v root | cut -d ' ' -f 1 | sort -u\""

    rd_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 15, 16]
    grx_numbers = [3, 4, 5, 6]
    cur = connection.cursor()
    for num in rd_numbers:
        rd_name = "rgs%02d" % num
        rd_cmd = " ".join(["ssh", rd_name, users_list_cmd_quote, "2>/dev/null"])
        rd_users = shell_cmd(rd_cmd)
        rd_users = rd_users.split()
        rd_users_str = " ".join(rd_users)
        if rd_users_str == "This account is currently not available.":
            rd_users_str = ""
        items = [rd_name, timestamp, rd_users_str]
        database_commit(items)

    for num in grx_numbers:
        grx_name = "grx%02d" % num
        grx_cmd = " ".join(["ssh", grx_name, users_list_cmd_quote, "2>/dev/null"])
        grx_users = shell_cmd(grx_cmd)
        grx_users = grx_users.split()
        grx_users_str = " ".join(grx_users)
        if grx_users_str == "This account is currently not available.":
            grx_users_str = ""
        items = [grx_name, timestamp, grx_users_str]
        database_commit(items)

    # Always close your connections
    cur.close()
    connection.close()


get_rd_data()

