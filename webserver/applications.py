# -*- coding: utf-8 -*-

import base64
import web
import model
import fileServerApi
import session
import transclass

### Templates
elements = web.template.render('templates/elements')
t_globals = {
    'elements': elements
}
render = web.template.render('templates', base='base', globals=t_globals)

### FileServer
fs = fileServerApi.FileServer('http://localhost:17007')

### Default Models
default_user = model.User()
for i in range(1, 8):
    str_i = str(i)
    temp = model.Video(str_i, 'video' + str_i, 'test' + str_i, 'intro of video' + str_i, 'upload_time' + str_i, i)
    default_user.add_video(temp)

default_video = model.Video('1','video1', 'test1', 'intro of video1', 'upload_time1', 1)




def notfound():
    return web.notfound(render.notfound())

class PageInfo:
    def __init__(self, title, message = "", error = ""):
        self.title = title
        self.message = message
        self.error = error


### Methods
class Index:

    def GET(self):
        temp = session.is_logged()
        if temp:
            page_info = PageInfo('Index')
            current_userid = session.get_user_id()
            ##ans, temp_user = get_user(current_userid)
            ##if ans: 
                ##current_user = transclass.user_trans(temp_user)
            ##else:
            ##    raise web.notfound()
            ##return render.index(current_user, page_info)
            current_user = default_user
            return render.index(default_user, page_info)
        else:
            raise web.seeother('/login')


class Login:

    def GET(self):
        page_info = PageInfo('Login')
        return render.login(page_info)

    def POST(self):
        data = web.input()
        #ans, current_user = check_user(username = data.username, password = data.password)
        answer = True  ## waiting for delete
        current_user = default_user ## also should be changed
        if answer:
            session.login(current_user.name)
            raise web.seeother('/')
        else:
            page_info = PageInfo('Login','Message Error')
            return render.login(page_info)
            


class Logout:

    def GET(self):
        session.logout()
        raise web.seeother('/')



class Register:

    def GET(self):
        page_info = PageInfo('Register')
        return render.register(page_info)
    def POST(self):
        data = web.input()
        if data.password != data.password_comfirm:
            page_info = PageInfo('Register',err = 'two passwords are not same')
            return render.register(page_info)
        else:
            ##answer, temp_user = insert_user(pwd = data.password,username = data.username)
            answer = True ## waiting for delete
            id = 1 ##
            if answer:
                ##session.login(temp_user.id)
                session.login(id)
                raise web.seeother('/')
            else:
                page_info = PageInfo('Register',err = 'input error')
                return render.register(page_info)
            
        

class Personal:

    def GET(self, id):
        page_info = PageInfo('Personal')
        ##ans!, temp1_user = get_user(session.get_user_id())
        ##ans2, temp2_user = get_user(session.get_user_id())
        ##if ans1 and ans2:
            ##current_user1 = transclass.user_trans(temp1_user)
            ##current_user2 = transclass.user_trans(temp2_user)
            ##return render.personal(current_user1, current_user2, page_info)
        ##else:
            ##raise web.notfound()
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
            raise web.notfound()
        encodedURL = base64.urlsafe_b64encode(uploadURL)

        page_info = PageInfo('Upload')
        ##ans, temp_user = get_user(session.get_user_id())
        ##if ans:
            ##current_user = transclass.user_trans(temp_user)
            ##render.upload(current_user, page_info,encodedURL)
        ##else:
            ##return web.notfound()
        return render.upload(default_user, page_info, encodedURL)

    def POST(self, encodedURL):
        uploadURL = base64.urlsafe_b64decode(str(encodedURL))
        x = web.input(up_img={})
        key, err = fs.putFile(x['up_img'].file, uploadURL)
        if err != None:
            web.debug(err)
            #raise web.seeother('/upload')
            # do something
            return
        web.debug(key)
        ##raise web.seeother('/')
        # do somthing


class Video:

    def GET(self, id):
        page_info = PageInfo('Video')
        ##ans1, temp_video = get_video(id)
        ##current_video = transclass.video_trans(temp_video)
        ##ans2, temp_user = get_user(session.get_user_id())
        ##current_user = transclass.user_trans(temp_user)
        ##if ans1 and ans2:
            ##return render.video(current_video,current_user,page_info)
        ##else:
            ##raise web.nofound() 
        return render.video(default_video, default_user, page_info)


class Edit:

    def GET(self, id):
        page_info = PageInfo('Edit')
        ##ans1, temp_video = get_video(id)
        ##ans2, temp_user = get_user(session.get_user_id())
        ##if ans1 and ans2:
            ##current_video = transclass.video_trans(temp_video)
            ##current_user = transclass.user_trans(temp_user)
            ##return render.edit(current_video,current_user,page_info)
        ##else:
            ##raise web.nofound()
        return render.edit(default_video, default_user, page_info)
    def POST(self,id):
        data = web.input()
        page_info = PageInfo('Edit')
        return render.edit(default_video, default_user,page_info)
        ##ans, temp_video = modify_video(id, name = data.video_name, intro =  data.video_intro)
        ##ans2, temp_user = get_user(session.get_user_id()).
        ##if ans2:
            ##current_user = transclass.user_trans(temp_user)
        ##else:
            ##raise web.nofound()
        ##if ans:
          ##  current_video = transclass.video_trans(temp_video)
          ##  page_info = PageInfo('Edit',message = '保存成功！')
          ##  return render.edit(current_video,current_user,page_info)
        ##else:
          ##  page_info = PageInfo('Edit',err = '保存失败，请再试！')
          ##  return render.edit(current_video,current_user,page_info)
            
