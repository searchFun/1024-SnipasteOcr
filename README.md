# SnipasteOCR

SnipasteOCR

### 需要配置node环境
#### 1、下载node压缩包解压到本地
假设解压到D:/nodejs
#### 2、建立自己的npm模块全局安装文件夹和缓存文件夹
文件夹名字和位置不限，在后面会把他们设置到npm中

假设此处分别为D:\nodejs\node_global\和D:\nodejs\node_cache

(注：模块默认安装文件夹是C:\Users\Administrator\AppData\Roaming\npm，如果你不想使用自己的文件夹，此处和后面相关设置可以不做)
#### 3.配置用户变量
用户变量 NODE_HOME 设置 D:\nodejs\ 

用户变量 NODE_PATH 设置 D:\nodejs\node_global\node_modules\，此目录为全局模块查找位置。

用户变量 PATH 添加 %NODE_HOME% 条目

#### 4.命令行设置npm
在此之前可以命令行输入node检查是否安装成功

#### 5、另外还要设置npm的config中的一些值，这将最终改变npm全局安装模块的目录和缓存目录
设置全局安装目录命令
npm config set prefix "D:\nodejs\node_global"

设置缓存目录命令
npm config set cache "D:\nodejs\node_cache"

还可以用如下命令查看npm的设置
npm config get