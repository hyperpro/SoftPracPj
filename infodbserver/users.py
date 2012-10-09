#operate of the whole users table in the database

import bigUser

import sys
#if not "../webserver/" in sys.path:
#    sys.path.append("../webserver/")
#if not 'settings' in sys.modules:
#    settings = __import__('settings')
#else:
#    eval('import settings')
#    settings = eval('reload(settings)')

import sys
sys.path.append("..")
from webserver.settings import db

#get a user by userid, if user is noe exit, return None; else return this User 
def get_user(userId): 
    myvar = dict(uid=userId)
    results = db.select('users', myvar, where="userId = $uid")
    if len(results)==0:
        return None
    return bigUser.BigUser(results[0])

#check userName and passwd is of the same user
#if is right, return this user
def check_user(userName, passwd):
    myvar = dict(uName=userName, upwd=passwd)
    results = db.select('users', myvar, where="userName = $uName and passwd = $upwd")
    if len(results)>0:
        return bigUser.BigUser(results[0])
    else:
        results = db.select('users', myvar, where="mail = $uName and passwd = $upwd")
        if len(results)>0:
            return bigUser.BigUser(results[0])
        else:
            return None

#insert a user to table users
#if is success return this user
def insert_user(userName, pwd, mail, picKey, isVip, videoCount, publicVideoCount, interest):
    try:
        db.insert('users',userName=userName, passwd=pwd, mail=mail, picKey=picKey, isVip=isVip, videoCount=videoCount, publicVideoCount=publicVideoCount, interest=interest)
        myvar = dict(uName=userName)
        results = db.select('users', myvar, where="userName=$uName") 
        if len(results)>0:
            return bigUser.BigUser(results[0])
        else:
            return None
    except:
        return None
    
    
if __name__ == "__main__":
    print 'begin'
    a = get_user(12)
    print a.userId,a.mail, a.picKey,a.isVip, a.videoCount
        