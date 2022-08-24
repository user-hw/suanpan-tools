from genericpath import isdir
import json
import pandas as pd
from router import getUsers
import lzstring
import os
from shutil import copy

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

db_outline_columns = ['id','name','user_id']


suanpan_path = "C:/Users/wudai.xhw/AppData/Local/xuelang/suanpan-desktop"
db_dir = os.path.join(suanpan_path,"data",'db')
db_detail_dir = os.path.join(suanpan_path,"data",'minio','suanpan','studio')
EXPORT_PATH='C:/Users/wudai.xhw/Desktop/命令行工具/'


pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 180)

pd.options.display.max_rows = None


def getDbByUser(user_name):
    '''
    查找单个用户的信息
    return：该用户的所有组件的dataframe
    '''
    if user_name not in getUsers(db_dir):
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
                if item=='id':
                    temp[item] = int(db[item])
                else:
                    temp[item] = db[item]
            db_outline_data = db_outline_data.append(temp,ignore_index=True)
        return db_outline_data
        
def getDbAll():
    '''
    返回所有的信息
    '''
    userList = getUsers(db_dir)   
    db_outline_data = pd.DataFrame(data=None,columns=db_outline_columns)
    for user in userList:
        db_outline_data = db_outline_data.append(getDbByUser(user),ignore_index=True)
    return db_outline_data

def getDetailById(user_name,id):
    '''
    通过id获取所有的细节信息
    '''   
    if user_name not in getUsers(db_detail_dir):
        print('用户不存在')
        return 
    else:
        x = lzstring.LZString()
        file_path = os.path.join(db_detail_dir,user_name,"component",str(id),'data')
        with open(file_path,'rb') as file:
            f = file.read()
            
        buf=[]
        for i in range(len(f)//2):
            buf.append(f[i*2]*256+f[i*2+1])
        res = []
        for i in buf:
            res.append(chr(i & 0xffff))
        content = x.decompress(''.join(res))
        content_json = json.loads(content)
        PrettyJson = json.dumps(content_json, indent=2, separators=(',', ': '), sort_keys=True, ensure_ascii=False)
        return PrettyJson
    

def getPackages(user_name,id,to_path):
    file_path = os.path.join(db_detail_dir,user_name,"component",str(id),'packages')
    if os.path.isdir(file_path):
        for file in  os.listdir(file_path):
            now_file = os.path.join(file_path,file)
            if file in os.listdir(to_path):
                ans = input('文件已经存在，是否覆盖文件[y/n]:')
                if (ans) in ['y','yes']:
                    copy(now_file,to_path)
                    return '导出成功'
                else:
                    return '取消导出'   
    else:
        return '暂时没有办法导出'

def getInfoById(id):
    df =getDbAll()
    res = df[df.id == id]
    try:
        return res['id'].tolist()[0],res['name'].tolist()[0],res['user_id'].tolist()[0],res
    except:
        return None,None,None,None

def getInfoByName(name):
    df =getDbAll()
    res = df[df.name == name] 
    try:
        return res['id'].tolist()[0],res['name'].tolist()[0],res['user_id'].tolist()[0],res
    except:
        return None,None,None,None