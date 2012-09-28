# -*- coding: utf-8 -*-

import httplib2


class FileServer:

    def __init__(self, host):
        self.host = host
        self.conn = httplib2.Http(".cache")

    def putAuth(self):
        """
        input:  (None)
        return: uploadURL
        """
        try:
            resp, content = self.conn.request(self.host + '/put-auth', 'GET')
        except Exception, e:
            return (None, e)

        if resp['status'] != '200':
            return (None, 'put-auth: status code = ' + resp['status'])
        return (content, None)

    def putFile(self, file, uploadURL):
        """
        input:  file
        return: key, err
        """
        try:
            file.seek(0, 2)
            length = file.tell()
            file.seek(0, 0)
            resp, content = self.conn.request(uploadURL, 'POST', body=file.read(),
                headers={'content-length': str(length)})
        except Exception, e:
            return (None, e)

        if resp['status'] != '200':
            return (None, 'upload: status code = ' + resp['status'])
        return (content, None)

    def getFileURL(self, key):
        """
        input:  key
        return: fileURL, err
        """
        try:
            resp, content = self.conn.request(self.host + '/get/' + key, 'GET')
        except Exception, e:
            return (None, e)

        if resp['status'] != '200':
            return (None, 'get: status code = ' + resp['status'])
        return (content, None)

    def deleteFile(self, key):
        """
        input:  key
        return: err
        """
        try:
            resp, content = self.conn.request(self.host + '/delete/' + key, 'GET')
        except Exception, e:
            return (None, e)

        if resp['status'] != '200':
            return 'delete: status code = ' + resp['status']
        return None

    def getThumbURL(self, key):
        """
        input:  key
        return: thumbURL, err
        """
        try:
            resp, content = self.conn.request(self.host + '/get/' + key, 'GET')
        except Exception, e:
            return (None, e)

        if resp['status'] != '200':
            return (None, 'get: status code = ' + resp['status'])
        return (content + '?thumb=1', None)
