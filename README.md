h1. 依赖

    * 需安装httplib2
    sudo pip install httplib2

    * 需安装web.py
    sudo pip install web.py

h1. FileServer

    * fileServerApi.py

    * 初始化:    fs = fileServerApi.FileServer(<file server host>)
    * 上传:      key, err = fs.putFile(file)
    * 下载:      fileURL, err = fs.getFileURL(key)
    * 删除:      err = fs.deleteFile(key)
    * 视频缩略图: thumbURL, err = fs.getThumbURL(key)