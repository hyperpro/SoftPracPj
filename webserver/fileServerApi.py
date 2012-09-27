import httplib2


class FileServer:

    def __init__(self, host):
        self.host = host
        self.conn = httplib2.Http(".cache")

    def putFile(self, file):
        """
        input:  file
        return: key, err
        """
        resp, content = self.conn.request(self.host + '/put-auth', 'GET')
        if resp['status'] != '200':
            return (None, 'put-auth: status code = ' + resp['status'])
        putUrl = content

        file.seek(0, 2)
        length = file.tell()
        file.seek(0, 0)
        resp, content = self.conn.request(putUrl, 'POST', body=file.read(),
            headers={'content-length': str(length)})
        if resp['status'] != '200':
            return (None, 'upload: status code = ' + resp['status'])
        return (content, None)

    def getFileURL(self, key):
        """
        input:  key
        return: fileURL, err
        """
        resp, content = self.conn.request(self.host + '/get/' + key, 'GET')
        if resp['status'] != '200':
            return (None, 'get: status code = ' + resp['status'])
        return (content, None)

    def deleteFile(self, key):
        """
        input:  key
        return: err
        """
        resp, content = self.conn.request(self.host + '/delete/' + key, 'GET')
        if resp['status'] != '200':
            return 'delete: status code = ' + resp['status']
        return None

    def getThumbURL(self, key):
        """
        input:  key
        return: thumbURL
        """
        return self.host + '/get-thumb/' + key
