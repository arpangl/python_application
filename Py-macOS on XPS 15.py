import requests as r
from bs4 import BeautifulSoup as bs
import pymysql
import datetime as dt

# ======
# Define Variables
# ======
BOARD_ID = 'stock'

auth = []
title = []
date = []
hot = [] #熱度
link = [] #連結

# ======
# Connect to database
# ======

def connectdb():
    global cursor
    global db
    try:
        db = pymysql.connect('220.133.40.181','crawler','crawler','ptt')
        cursor = db.cursor()
        print ('Connection established successfully!')
    except pymysql.err.OperationalError as e:
        print (type(e))
        print (f'error code: {e[1:4]}')
        
# ======
# This function check the maxmium page of the board
# in case of the regular deletion
# ======

def index_check():
    try:
        g = r.get('https://www.ptt.cc/bbs/'+BOARD_ID+'/index.html')
        soup = bs(g.text,'html.parser')
        t = 0
        for i in soup:
        # print (i.select('a')[1])  檢查“上頁”
            k = i.select('a')[1]
        for i in k.get('href'):
            if i.isdigit():
                t *= 10
                t += int(i)
        return t+1 #last page
    
    except:
        errorMassage = 'Unable to find!\n Please check the board you search is valid.'
        return errorMassage


# ======
# Craw the title, autor, hot, link and save as list
# ======

def craw_outside():
    try:
        for INDEX in range(index_check(), index_check()-1,-1):
            g = r.get('https://www.ptt.cc/bbs/'+BOARD_ID+'/index'+str(INDEX)+'.html')
            soup = bs(g.text, 'html.parser')
            for entry in soup.select('.r-ent'):
                if "刪除" in entry.select('.title')[0].text:
                    continue
                else:
                    link.append('https://www.ptt.cc/'+entry.select('a')[0].get('href'))
                    hot.append(entry.select('.nrec')[0].text)
                    title.append(entry.select('.title')[0].text)
                    date.append(dt.datetime.fromtimestamp(int(entry.select('a')[0].get('href')[13:23])))
                    auth.append(entry.select('.author')[0].text)
            print(index_check()-INDEX+1,'pages collected')
    except:
        return 0
        print ('Error! Please check the entire web site\'s structure to update the crawler\'s code')    
  
def craw_inside():
    return 0

def man_db():
    cursor.excute()


# =====
# resolve the data (majorly author, title, hot, url, hot)
# and save them into the database
# =====
def craw_and_save():
    for INDEX in range(index_check(), 1,-1):
        g = r.get('https://www.ptt.cc/bbs/'+BOARD_ID+'/index'+str(INDEX)+'.html')
        soup = bs(g.text, 'html.parser')
        for entry in soup.select('.r-ent'):
            if "刪除" in entry.select('.title')[0].text:
                continue
            else:
                hot = entry.select('.nrec')[0].text
                if hot == '':
                    hot = 0
            sql = "INSERT into `"+BOARD_ID+"` (Author,Title,atime,hot,url) values ('"+entry.select('.author')[0].text+"','"+pymysql.escape_string(entry.select('.title')[0].text)+"','"+str(dt.datetime.fromtimestamp(int(entry.select('a')[0].get('href')[13:23])))+"','"+str(hot)+"','https://www.ptt.cc"+entry.select('a')[0].get('href')+"')"
            print (sql)
            cursor.execute(sql)
        print(index_check()-INDEX+1,'pages collected')
        db.commit()


connectdb()
craw_and_save()
db.close()
    

