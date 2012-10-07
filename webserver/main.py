# -*- coding: utf-8 -*-

import base64
import web
import model
import fileServerApi

### Route
urls = (
	'/', 'Index',
	'/login', 'Login',
	'/register', 'Register',
	'/personal/(.*)', 'Personal',
	'/video/(.*)', 'Video',
	'/edit/(.*)', 'Edit',
	'/upload/(.*)', 'Upload',  # POST
	'/upload', 'Upload',  # GET
)


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

### Main Applicaiton 
app = web.application(urls, globals())

### User Sessions
web.config.debug = False
session = web.session.Session(app,web.session.DiskStore('sessions'),initializer={'login':'False', 'username':'guest'})
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['timeout'] = 70
web.config.session_parameters['exprired_message'] = 'Please login again'



### FileServer
fs = fileServerApi.FileServer('http://localhost:17007')


class PageInfo:
	def __init__(self, title):
		self.title = title


### Methods
class Index:

	def GET(self):
		cookie = web.cookies();
		if cookie:
			if session.login == 'True':
				current_user = Getuser(session.login) ## Ark Yang's Function 
				return render.index(current_user, page_info)
			else:
				raise web.seeother('/login')
		else:
			raise web.seeother('/login')			 
		page_info = PageInfo('Index')
		return render.index(default_user, page_info)
		#return elements.video_prev(default_video)


class Login:

	def GET(self):
		page_info = PageInfo('Login')
		return render.login(page_info)


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


if __name__ == '__main__':
	app.run()
