import requests as r
from bs4 import BeautifulSoup as bs
import numpy as np
import pymysql


# ======
# Connect to database
# ======

def connectdb():
    db = pymysql.connect('127.0.0.1','crawler','crawler','ptt')
    cursor = db.cursor()


BOARD_ID = 'stock'

auth = []
title = []
date = []

# ======
# This function check the maxmium page of the board
# in case of the regular deletion
# ======

def index_check():
    try:
        g = r.get('https://www.ptt.cc/bbs/'+BOARD_ID+'/index.html')
        soup = bs(g.text,'html.parser')
        t = 0
        for i in soup.select('.btn-group-paging'):
        # print (i.select('a')[1])  檢查“上頁”
            k = i.select('a')[1]
        for i in k.get('href'):
            if i.isdigit():
                t *= 10
                t += int(i)
        return t+1 #last page
    
    except:
        errorMassage = 'Unable to find!'
        return errorMassage





def craw_outside():
    
    print (index_check())
    for INDEX in range(index_check(), 1,-1):
    
        g = r.get('https://www.ptt.cc/bbs/'+BOARD_ID+'/index'+str(INDEX)+'.html')
        soup = bs(g.text, 'html.parser')
        for  entry in soup.select('.r-ent'):
            title.append(entry.select('.title')[0].text)
            date.append(entry.select('.date')[0].text)
            auth.append(entry.select('.author')[0].text)
        print(index_check()-INDEX+1,'pages collected')


def craw_inside(ariticle_id):
    return 0            
 
connectdb()
np.savetxt('a.txt',np.column_stack((date,auth,title)),fmt='%s',encoding="utf-8")