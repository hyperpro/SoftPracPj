import web
import model
import fileServerApi

### FileServer
fs = fileServerApi.FileServer('http://localhost:17007')

def user_trans(full_user):
    new_user = model.User()
    new_user.id = full_user.userId
    new_user.name = full_user.userName
    new_user.pwd = full_user.passwd
    new_user.mail = full_user.mail
    thumbURL, err = fs.getThumbURL(full_user.picKey)
    if err!=None:
        new_user.pic = ""
    else:
        new_user.pic = thumbURL
    for element in full_user.video:
        new_user.add_video(video_trans(element))
    return new_user
        
        
def video_trans(full_video):
    new_video = model.Video()
    new_video.name = full_video.videoName
    new_video.id = full_video.videoId
    new_video.owner = full_video.ownerId
    new_video.intro = full_video.intro
    new_video.upload_time = full_video.uploadTime
    new_video.key = full_video.keyValue
    thumbURL, err = fs.getThumbURL(full_video.keyValue)
    if err!=None:
        new_video.prev = ""
    else:
        new_video.prev = thumbURL
    fileURL, err = fs.getFileURL(full_video.key)
    if err!=None:
        new_video.src = ""
    else:
        new_video.src = fileURL
    return new_video

    
     