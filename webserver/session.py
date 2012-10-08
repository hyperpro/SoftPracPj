# -*- coding: utf-8 -*-

import web
from settings import db

def add_sessions_to_app(app):
    if web.config.get('_session') is None:
        store = web.session.DBStore(db, 'sessions')
        session = web.session.Session(app, store,
            initializer={'is_logged' : False, 'userid':'guest'})
        web.config.session_parameters['ignore_expiry'] = False
        web.config.session_parameters['timeout'] = 60
        web.config._session = session
    else:
        session = web.config._session

def get_session():
    return web.config._session

def is_logged():
    return get_session().is_logged

def login(userid):
    s = get_session()
    s.is_logged = True;
    s.userid = userid;

def logout():
    get_session().kill()

def get_user_id():
    return get_session().userid

