## 安装 face-recognition
首先说明，我的系统是win10，python版本是python3.7

需要事先下载一下3个包并安装：

1、vs c++ 2015,必须是2015，dlib或cmake编译环境需要
可以用这个链接：https://www.microsoft.com/zh-CN/download/details.aspx?id=48145

也可以用社区版

2、Boost C++ Libraries
可以用这个链接：https://dl.bintray.com/boostorg/release/1.66.0/binaries/

选择boost_1_66_0-msvc-14.0-64.exe，安装到C盘即可

3、cmake
可以用这个链接：https://cmake.org/download/

选择cmake-3.15.0-rc4-win64-x64.msi

注意！！！cmake在安装过程中切记选择添加路径到环境变量中。
4、当上面3个都安装好之后，可以直接在命令窗口安装pip install face-recognition即可，在这过程中会自动安装好dlib，当然也可以先安装dlib，这就看各位心情了。

建议使用国内镜像安装：pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com dlib


 
