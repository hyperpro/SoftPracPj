import web
import model
import fileServerApi

### Route
urls = (
	'/', 'Index',
	'/login', 'Login',
	'/register', 'Register',
	'/personal', 'Personal',
	'/video', 'Video',
	'/edit', 'Edit',
	'/upload', 'Upload',
)


### Templates
elements = web.template.render('templates/elements')
t_globals = {
	#'datestr': web.datestr
	'elements': elements
}
render = web.template.render('templates', base='base', globals=t_globals)


### Default Models
default_user = model.User()
for i in range(1, 8):
	str_i = str(i)
	temp = model.Video('video' + str_i, 'intro of video' + str_i, 'upload_time' + str_i, i)
	default_user.add_video(temp)

default_video = model.Video('video1', 'intro of video1', 'upload_time1', 1)

### FileServer
fs = fileServerApi.FileServer('http://localhost:17007')


class PageInfo:
	def __init__(self, title):
		self.title = title


### Methods
class Index:

	def GET(self):
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

	def GET(self):
		page_info = PageInfo('Personal')
		return render.personal(default_user, page_info)


class Upload:

	def GET(self):
		page_info = PageInfo('Upload')
		return render.upload(default_user, page_info)

	def POST(self):
		x = web.input(up_img={})
		# web.debug(x['up_img'].value)
		key, err = fs.putFile(x['up_img'].file)
		if err != None:
			web.debug(err)
			# do something
			return
		web.debug(key)
		# do somthing


class Video:

	def GET(self):
		page_info = PageInfo('Video')
		return render.video(default_video, default_user, page_info)


class Edit:

	def GET(self):
		page_info = PageInfo('Edit')
		return render.edit(default_video, page_info)


###
app = web.application(urls, globals())

if __name__ == '__main__':
	app.run()
