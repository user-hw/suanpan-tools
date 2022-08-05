from genericpath import isdir
import os

suanpan_path = "C:/Users/wudai.xhw/AppData/Local/xuelang/suanpan-desktop"
db_dir = os.path.join(suanpan_path,"data",'db')


def getUsers():
    '''
    查找所有用户信息
    return：所有用户信息的list
    '''
    users = []
    for path in  os.listdir(db_dir):
        now_file = os.path.join(db_dir,path)
        
        if os.path.isdir(now_file):
            users.append(path)
    return users
