#the API of the whole info database
import users
import bigUser
import videos
import bigVideo

#for users

#if user = None, then isUserExit = false else isUserExit = true
#return (isUserExit,User)
def get_user(userId):
    if userId is None:
        return False,None
    else:
        oneUser = users.get_user(userId)
        if oneUser is None:
            return False, None
        else:
            return True, oneUser

#check is userName and the passwd is belong to the same user
#return (isLoginable, User)
def check_user(userName, passwd):
    if userName is None or passwd is None:
        return False, None
    else:
        oneUser = users.check_user(userName, passwd)
        if oneUser is None:
            return False, None
        else:
            return True, oneUser

#insert a user with a list of user attributes
#return (isInserted, User)
def insert_user(userName, pwd, mail, picKey=None, isVip=False, videoCount=0, publicVideoCount=0, interest=None):
    if userName is None or pwd is None or mail is None:
        return False, None
    else:
        oneUser = users.insert_user(userName, pwd, mail, picKey, isVip, videoCount, publicVideoCount, interest)
        if oneUser is None:
            return False, None
        else:
            return True, oneUser

#for videos

#get Video by videoId
#return (isVideoExit, Video)
def get_video(videoId):
    if videoId is None:
        return False,None
    else:
        oneVideo = videos.get_video(videoId)
        if oneVideo is None:
            return False, None
        else:
            return True, oneVideo
        
#if Video=None, then isVideoExit= false, else isVideoExit=true
#return (isVideoExit, Video(with videoId, ownId, keyValue))
def insert_video(keyValue, ownerId):
    if keyValue is None or ownerId is None:
        return False,None
    else:
        oneVideo = videos.insert_video(keyValue, ownerId)
        if oneVideo is None:
            return False, None
        else:
            return True, oneVideo

#modify the attribute of the video
#return(isModified, Video)
def modify_video(videoId, videoName=None, ownerId=None, keyValue=None, intro=None, uploadTime=None, isPublic=None, recommendCount=None, commentCount=None, category=None):
    if videoId is None:
        return False, None
    else:
        oneVideo = videos.modify_video(videoId, videoName, ownerId, keyValue, intro, isPublic, recommendCount, commentCount, category)
        if oneVideo is None:
            return False, None
        else:
            return True, oneVideo
        
        
        
        

