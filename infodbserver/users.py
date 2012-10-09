#operate of the whole users table in the database

import bigUser
import videos


import sys
sys.path.append("../webserver")
from settings import db

#get a user by userid, if user is noe exit, return None; else return this User 
def get_user(userId): 
    myvar = dict(uid=userId)
    results = db.select('users', myvar, where="userId = $uid")
    if len(results)==0:
        return None
    else:
        videoKeyValueList = videos.get_videoKeyValueList(userId)
        return bigUser.BigUser(results[0], videoKeyValueList)

#check userName and passwd is of the same user
#if is right, return this user
def check_user(userName, passwd):
    myvar = dict(uName=userName, upwd=passwd)
    results = db.select('users', myvar, where="userName = $uName and passwd = $upwd")
    if results is None or len(results)==0:
        results = db.select('users', myvar, where="mail = $uName and passwd = $upwd")
    if len(results)>0:
        temp = results[0]
        videoKeyValueList = videos.get_videoKeyValueList(temp['userId'])
        return bigUser.BigUser(temp, videoKeyValueList)
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
            return bigUser.BigUser(results[0],[])
        else:
            return None
    except:
        return None
    
    

        