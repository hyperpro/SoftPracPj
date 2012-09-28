dddd依赖
hahahahha
----


 * 需安装httplib2

    sudo pip install httplib2

 * 需安装web.py

    sudo pip install web.py

FileServer
----------

 * 运行方法：exe/目录下运行run.sh（./run.sh）
 * api见: fileServerApi.py

 * Usage Tip:

        初始化:    fs = fileServerApi.FileServer(<file server host>)

        上传:      uploadURL, err = fs.putAuth()
                    key, err = fs.putFile(file, uploadURL)

        下载:      fileURL, err = fs.getFileURL(key)

        删除:      err = fs.deleteFile(key)

        视频缩略图: thumbURL, err = fs.getThumbURL(key)

Webserver
---------

 * Python 代码请使用tab缩进，别用空格思密达！！！

