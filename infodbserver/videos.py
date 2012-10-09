#operate of the whole videos table in the database
import bigVideo

import sys
sys.path.append("../webserver")
from settings import db



#use keyValue and ownId to insert a tuple into videos table
#if successed insert return Video,else reutrn None
def insert_video(keyValue, ownerId):
    try:
        db.insert("videos", keyValue=keyValue, ownerId=ownerId)
        myvar = dict(keyName=keyValue)
        results = db.select("videos", myvar, where="keyValue = $keyName")
        print len(results)
        if len(results)>0:
            return bigVideo.BigVideo(results[0])
        else:
            return None
    except Exception, e:
        return None
    

#get Video by videoId
def get_video(videoId):
    if videoId is None:
        return None
    myvar = dict(videoId = videoId)
    results = db.select('videos', myvar, where="videoId = $videoId")
    if len(results)==0:
        return None
    return bigVideo.BigVideo(results[0])
    
#modify the video and return it if successfully
def modify_video(videoId, videoName, ownerId, keyValue, intro, isPublic, recommendCount, commentCount, category):
    if videoId is None:
        return None
    
    vars = {}
    if videoName is not None:
        vars['videoName'] = videoName
    if ownerId is not None:
        vars['ownerId'] = ownerId
    if keyValue is not None:
        vars['keyValue'] = keyValue
    if intro is not None:
        vars['intro'] = intro
    if isPublic is not None:
        vars['isPublic'] = isPublic
    if recommendCount is not None:
        vars['recommendCount'] = recommendCount
    if commentCount is not None:
        vars['commentCount'] = commentCount
    if category is not None:
        vars['category'] = category
    sql  = "update videos set "
    length = len(vars.keys())
    count = 1
    for x in vars.keys():
        sql = sql+x
        sql = sql+"=$"+x
        if count<length:
            sql = sql+","
        count = count+1

    sql = sql + " where videoId = $videoId"
    vars['videoId']=videoId
    try:
        db.query(sql,vars = vars)
        return get_video(videoId)
    except Exception,e:
        return None
   

   

    
