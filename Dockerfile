
### 不再安装python环境，在mid-server-edu-base:2中python环境都已经安装了，包括playwright的环境
FROM registry.cn-zhangjiakou.aliyuncs.com/mid-server/mid-server-edu-base:3

ENV PYTHONUNBUFFERED 1

WORKDIR /code/
# ADD . /code/  ### 这里不复制文件夹，docker-compose.yaml文件里挂载./ /code/

EXPOSE 8889

CMD ["python3", "main.py"]

## 先run: docker-compose build 
## 再run: docker-compose up -d