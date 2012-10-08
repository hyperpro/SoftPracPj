# -*- coding: utf-8 -*-

import base64
import web
import model
import fileServerApi
import session
import applications

### Route
urls = (
	'/', 'applications.Index',
	'/login', 'applications.Login',
	'/logout', 'applications.Logout',
	'/register', 'applications.Register',
	'/personal/(.*)', 'applications.Personal',
	'/video/(.*)', 'applications.Video',
	'/edit/(.*)', 'applications.Edit',
	'/upload/(.*)', 'applications.Upload',  # POST
	'/upload', 'applications.Upload',  # GET
)

### Main Applicaiton 
app = web.application(urls, globals())
session.add_sessions_to_app(app)


if __name__ == '__main__':
	app.run()
