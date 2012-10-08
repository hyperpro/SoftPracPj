import web
import model
import fileServerApi

### FileServer
fs = fileServerApi.FileServer('http://localhost:17007')

def user_trans(full_user):
    new_user = model.User()
    new_user.id = full_user.id
    new_user.name = full_user.name
    new_user.pwd = full_user.pwd
    new_usr.mail = full_user.mail
    thumbURL, err = fs.getThumbURL(full_user.key)
    if err!=NONE:
        new_usr.pic = ""
    else:
        new_usr.pic = thumbURL
    for element in full_user.video:
        new_user.add_video(video_trans(element))
    return new_user
        
        
def video_trans(full_video):
    new_video = model.Video()
    new_video.name = full_video.name
    new_video.id = full_video.id
    new_video.owner = full_video.owner
    new_video.intro = full_video.intro
    new_video.upload_time = full_video.upload_time
    new_video.key = full_video.key
    thumbURL, err = fs.getThumbURL(full_video.key)
    if err!=NONE:
        new_video.prev = ""
    else:
        new_video.prev = thumbURL
    fileURL, err = fs.getFileURL(full_video.key)
    if err!=NONE:
        new_video.src = ""
    else:
        new_video.src = fileURL
    return new_video

    
     