import re
import sqlite3
from sqlite3 import Error

def startDateExtract(s):
    pattern='^\(\([0-2][0-9]\)|\(\(3\)[0-1]\)\)\(\/\)\(\(\(0\)[1-9]\)|\(\(1\)[0-2]\)\)\(\/\)\(\(\d{2}\)|\(\d{4}\)\) , \([0-9][0-9]\):\([0-9][0-9]\) -'
    result=re.match(pattern,s)
    if result:
        return True
    return False
def startUserExtract(s):
    patterns=['\([\w]+\):','\([\w]+[\s]+[\w]+\):','\([\w]+[\s]+[\w]+[\s]+[\w]+\):','\([+]\d{2} \d{5} \d{5}\):']
    pattern='^'+'|'.join(patterns)
    result=re.match(pattern,s)
    if result:
        return True
    return False
def getWatsappData(line):
    splitline=line.split('-')
    datetime=splitline[0]
    date,time=datetime.split(',')
    datainfo = ' '.join(splitline[1:])
    if startUserExtract(datainfo):
      userdata=datainfo.split(':')
      user=userdata[0]
      data=' '.join(userdata[1:])
    else:
        user=None
    return date,time,user,data
def sql_connection():
    try:
        con=sqlite3.connect('mywatsapp.db')
       # print(con,"connection established")
        return con
    except Error:
        print(Error)
def sql_table(con):
    cursorObj =con.cursor()
    cursorObj.execute("CREATE TABLE watsapp (id integer PRIMARY KEY AUTOINCREMENT,date text,time text,user text,data text);")
    con.commit()
def sql_insert(con):
    cursorObj=con.cursor()
    cursorObj.execute("INSERT INTO watsapp VALUES (?,?,?,?);",entries)
    con.commit()
parsedata=[]
conn=sql_connection()
#sql_table(conn)
with open('pycharmfile/watsappchat.txt',mode='r',encoding='utf-8') as fp:
 list=fp.readlines()
 messageBuffer=[]
 entries=()
 date,time,user,data=None,None,None,None
 for line in list:
       # line=fp.readline()
        if not line:
            break
        line=line.strip()
        if (startDateExtract(line)):
           if len(messageBuffer)>0:
                parsedata.append([date,time,user,''.join(messageBuffer)])
            #print(parsedata)
            #print(messageBuffer)
                messageBuffer.clear()
           Date,Time,User,Data=getWatsappData(line)
           print(Date, Time, User, Data)
          # entries=getWatsappData(line)
           # sql_insert(conn)
           # messageBuffer.append(data)


        else:
            messageBuffer.append(line)

        #sql_insert(conn)
#for row in conn.execute("SELECT * FROM watsapp"):
 #   print(row)













