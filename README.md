需要run此项目，分为两个部分：
- build出一个base-image, 此base-image仅用于更新pip环境和linux 环境， 更新后生成image上传至阿里云， 需要执行docker build; docker run; docker commit; docker tag; docker push 
- 依据阿里云上的base-image启动服务。先执行docker-compose build； 再执行docker-compopse up
  

第一部分： （如果不更新环境，则不需要执行这部分过程）
```bash
# 先到base image folder
cd mid-proxy-base-image  

 # 构建第一个基础镜像， 
docker build -t mid-proxy-base-image:1 .     ### mid-proxy-base-image:1    eca6c4d06d6a

# 构建出一个基础镜像的container, 然后去container内部去更新安装包，或者docker build -t的方式安装好所有安装包，
docker run -itd --name mid-proxy-base-container mid-proxy-base-image:1     ###  aa0165c2af38   mid-proxy-base-container 
#### 去container里安装 playwright: >>> playwright install ,   >>> playwright install-deps

############################# 当然，除了第一次，以后可以不用这么傻瓜， ########################################################################################
#######                       直接在Dockerfile里引用之前的image就好了，                                                                           ##########
#######                       不再 FROM python:3.10.4， 而是FROM  registry.cn-zhangjiakou.aliyuncs.com/mid-server/mid-server-edu-base:2，       ##########
#######                      根据这个镜像再去build一次或者run container and pip一次                                                              ###########
########################################################################################################################################################


# 上传镜像
### 去阿里云上可以看到以下命令

# 通过运行的container去提交镜像
docker commit eca6c4d06d6a  mid-proxy-base-image:2  #mid-proxy-base-image:2 e48ee8c79013
# 打包镜像
docker tag e48ee8c79013 registry.cn-zhangjiakou.aliyuncs.com/mid-server/mid-server-edu-base:2
# 上传镜像
docker push registry.cn-zhangjiakou.aliyuncs.com/mid-server/mid-server-edu-base:2

### 至此，第一阶段的环境镜像算是打包成功了，在阿里云上可以看到镜像registry.cn-zhangjiakou.aliyuncs.com/mid-server/mid-server-edu-base:2， 以后更新服务时可以此镜像为base去发布服务
```

第二部分：
```bash
# 发布代码服务
cd到根目录， vim Dockerfile 可以看到FROM registry.cn-zhangjiakou.aliyuncs.com/mid-server/mid-server-edu-base:2
说明服务已经使用了正常的环境，更新了所有安装包的

此时需要执行：
docker-compose build   # docker-compose通过Dockerfile先build出服务的镜像，
docker-compose up -d  # 服务即可启动
```