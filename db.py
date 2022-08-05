from cgi import test
from encodings import utf_8
import json
from tempfile import tempdir
from matplotlib.pyplot import get
import pandas as pd
from router import getUsers
import os

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

db_outline_columns = ['id','name','user_id']


suanpan_path = "C:/Users/wudai.xhw/AppData/Local/xuelang/suanpan-desktop"
db_dir = os.path.join(suanpan_path,"data",'db')




def getDbByUser(user_name):
    '''
    查找单个用户的信息
    return：该用户的所有组件的dataframe
    '''
    if user_name not in getUsers():
        print('用户不存在')
        return 
    else:
        path = os.path.join(db_dir,user_name,"comp.db")
        db_outline_data = pd.DataFrame(data=None,columns=db_outline_columns)
        
        with open(path,'r',encoding="utf_8") as f:
            db_list = json.load(f)
        for db in db_list:
            temp ={}
            for item in db_outline_columns:
                temp[item] = db[item]
                # print("temp ===" ,temp)
            db_outline_data = db_outline_data.append(temp,ignore_index=True)

        # print (db_outline_data)
        return db_outline_data
        
def getDbAll():
    '''
    返回所有的信息
    '''
    userList = getUsers()
    db_outline_data = pd.DataFrame(data=None,columns=db_outline_columns)
    for user in userList:
        db_outline_data = db_outline_data.append(getDbByUser(user),ignore_index=True)
    return db_outline_data

        
