# -*- coding: utf-8 -*-

import base64
import web
import model
import fileServerApi
import session

### Templates
elements = web.template.render('templates/elements')
t_globals = {
    'elements': elements
}
render = web.template.render('templates', base='base', globals=t_globals)


### Default Models
default_user = model.User()
for i in range(1, 8):
    str_i = str(i)
    temp = model.Video('video' + str_i, 'test' + str_i, 'intro of video' + str_i, 'upload_time' + str_i, i)
    default_user.add_video(temp)

default_video = model.Video('video1', 'test1', 'intro of video1', 'upload_time1', 1)

### FileServer
fs = fileServerApi.FileServer('http://localhost:17007')


class PageInfo:
    def __init__(self, title):
        self.title = title


### Methods
class Index:

    def GET(self):
        temp = session.is_logged()
        if temp:
            page_info = PageInfo('Index')
            current_userid = session.get_user_id()
            current_user = default_user ## waiting for delete
            ##current_user = getUser(current_userid)
            return render.index(default_user, page_info)
        else:
            raise web.seeother('/login')            
        return render.index(default_user, page_info)
        #return elements.video_prev(default_video)


class Login:

    def GET(self):
        page_info = PageInfo('Login')
        return render.login(page_info)
    
    def POST(self):
        data = web.input()
        answer = True  ## This should be the Function CheckUser, by Ark
        current_user = default_user ## also should be changed
        if answer:
            session.login(current_user.name)
            raise web.seeother('/')
        else:
            raise web.seeother('/login')
        
        
class Logout:
    
    def GET(self):
        session.logout()
        raise web.seeother('/')
        


class Register:

    def GET(self):
        page_info = PageInfo('Register')
        return render.register(page_info)


class Personal:

    def GET(self, id):
        page_info = PageInfo('Personal')
        return render.personal(default_user, default_user, page_info)


class Upload:
    
    """
    目前的做法是
    用户访问/upload页面会调用putAuth取得上传授权（一个会过期的上传url）
    将这个url编码之后放入表单，POST请求时可得到这个uploadURL
    然后调用fs.putFile上传文件
    """

    def GET(self):
        uploadURL, err = fs.putAuth()
        if err != None:
            web.debug(err)
            return app.notfound()
        encodedURL = base64.urlsafe_b64encode(uploadURL)

        page_info = PageInfo('Upload')
        return render.upload(default_user, page_info, encodedURL)

    def POST(self, encodedURL):
        uploadURL = base64.urlsafe_b64decode(str(encodedURL))
        x = web.input(up_img={})
        key, err = fs.putFile(x['up_img'].file, uploadURL)
        if err != None:
            web.debug(err)
            # do something
            return
        web.debug(key)
        # do somthing


class Video:

    def GET(self, key):
        page_info = PageInfo('Video')
        return render.video(default_video, default_user, page_info)


class Edit:

    def GET(self, key):
        page_info = PageInfo('Edit')
        return render.edit(default_video, default_user, page_info)
