# is a tuple of table users and some operations about it
class BigUser:
    def __init__(self, infos, videoList):
        self.userId = infos['userId']
        self.userName = infos['userName']
        self.passwd = infos['passwd']
        self.mail = infos['mail']
        self.picKey = infos['picKey']
        self.isVip = infos['isVip']
        self.videoCount = infos['videoCount']
        self.publicVideoCount = infos['publicVideoCount']
        self.interest = infos['interest']
        self.videoKeys = videoList
               