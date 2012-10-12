# # is a tuple of table videos and some operations about it
class BigVideo:
    def __init__(self,infos):
        self.videoId = infos['videoId']
        self.videoName = infos['videoName']
        self.ownerId = infos['ownerId']
        self.keyValue = infos['keyValue']
        self.intro = infos['intro']
        self.uploadTime = infos['uploadTime']
        self.isPublic = infos['isPublic']
        self.recommendCount = infos['recommendCount']
        self.commentCount = infos['commentCount']
        self.category = infos['category']
        self.type = infos['type']
        #self.category = None
        #for x in infos:
        #    print x,
