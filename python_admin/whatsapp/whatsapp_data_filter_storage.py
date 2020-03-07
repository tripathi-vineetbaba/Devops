#import all required libraries
from datetime import datetime
import re
import sqlite3 as sql
import itertools
#  Variable for your data file
whatsapp_chat_data='WhatsAppChatwithDevOps&CloudBabies.txt'
#Variable to store unprocessed line of your data
#errorFile=
#pattern to match date and time
id=1
pattern='^([1-9]{1,2})\/([1-9]{1,2})\/([12][0-9]),\s([1-9]{1,2}):([0-9]{2})\s(AM|PM)'
#Patter to match phone number string
number_pattern='(\+[0-9]{1,2})\s[\(]?([0-9]{1,5})[\)]?\s?([0-9]{3})[-]?[0-9]{1,4}'

#######  DATABASE SETUP##########################

def db_connect() :
    try:
        con=sql.connect('whatsapp_database.db')
        return con
    except Error:
        print(Error)

def create_tables_groupchat(con,groupname):
    cursor=con.cursor()
    create_table_query='CREATE TABLE IF NOT EXISTS ' + groupname + ' ( DATE TEXT, TIME TEXT, NAME TEXT, GROUP_NAME TEXT, NUMBER TEXT, MESSAGE TEXT);'
    cursor.execute(create_table_query)
    con.commit()
    con.close()

def read_file(whatsapp_chat_file):
    try :
        with open(whatsapp_chat_file,'r',encoding='utf-8') as whatsppfile :
            lines=whatsppfile.read().splitlines()
            return lines
    except FileNotFoundError:
        print("No such file or directory : " + whatsapp_chat_file)
        print("Please try with correct file")

def filter_date(line):
    day=re.search(pattern, str(line)).group(2)
    mon=re.search(pattern, str(line)).group(1)
    year=re.search(pattern, str(line)).group(3)
    date=day+'/'+mon+'/'+year
    date=datetime.strptime(date,'%d/%m/%y').date()
    return date
def filter_time(line):
    hour=re.search(pattern, str(line)).group(4)
    mins=re.search(pattern, str(line)).group(5)
    duration=re.search(pattern, str(line)).group(6)
    if duration == 'PM' :
        hour=int(hour) + 12
        if hour == 24 :
            hour=str(0)
        else :
            hour=str(hour)
    time=hour+'::'+mins
    time=datetime.strptime(time,'%H::%M').time()
    return time
def filter_pi(data):
    try :
        name_number=data.split(' - ')[1].split(':')[0].split(' joined ')[0]
        if re.match(number_pattern,name_number) :
            number=name_number
            name='NA'
        else :
            name=name_number
            number='NA'
        return(name,number)
    except :
        pass
def filter_message(data):
    try :
        message=data.split(' - ')[1].split(':')[-1]
        return message
    except :
        pass


def insert_data_into_database(data,errorFile='unprocessed_data.txt', groupname='DevopsandCloudBabies'):
    global id
    con=db_connect()
    cursor=con.cursor()
    insert_query='INSERT INTO ' + groupname + ' VALUES (?,?,?,?,?,?)'
    for line in data :
        try :
            date=filter_date(line)
            time=filter_time(line)
            pi_info=filter_pi(line)
            name=pi_info[0]
            number=pi_info[1]
            message=filter_message(line)
            record=(str(date),str(time),name,groupname,number,message)
            print(record)
            cursor.execute(insert_query,record)
            con.commit()
        except AttributeError:
            with open(errorFile,'a+', encoding='utf-8') as errorfile:
                errorfile.writelines(line + '\n')
            pass
    con.close()
def main():
    groupname='DevopsandCloudBabies'
    con=db_connect()
    create_tables_groupchat(con,groupname)
    data=read_file(whatsapp_chat_data)
    insert_data_into_database(data)

main()

