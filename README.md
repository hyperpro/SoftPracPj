依赖
----

 * 需安装httplib2

    sudo pip install httplib2

 * 需安装web.py

    sudo pip install web.py

 * 需安装python-mysqldb

    sudo apt-get install python-mysqldb

 * 需mysql建表（注意：用户名root密码为空）

 	cd到webserver目录

        mysql -u root -p

 		mysql> create database videoproject;

 	ctrl+D退出

        mysql -u root videoproject < videoproject.mysql




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

        视频缩略图: 200x150大小: thumbURL, err = fs.getThumbURL(key)
                  原图大小:     thumbURL, err = fs.getThumbURL(key, 0)

Webserver
---------

 * 运行方法：webserver/目录下执行 python main.py

 * 在浏览器中访问 localhost:8080 / 0.0.0.0:8080 即可

 * 注意：

          Python 代码请使用tab缩进，别用空格思密达！！！

          若FileServer未运行，访问/upload时会出错

