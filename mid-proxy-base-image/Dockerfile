FROM python:3.10.4
USER root

# 设置时区
ENV TZ=Asia/Shanghai

ENV PYTHONUNBUFFERED 1

WORKDIR /code/
ADD . /code/

RUN apt-get update && apt-get install -y vim python3-dev && pip install -U pip &&  pip install -r requirements.txt