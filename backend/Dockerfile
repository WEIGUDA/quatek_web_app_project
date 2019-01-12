FROM python:3.6-stretch

EXPOSE 5001

ENV ENV=production
ENV DEBUG=True
ENV MONGODB_HOST=mongo
ENV REDIS_URL=redis://redis
ENV SOCKET_HOST=0.0.0.0
ENV ORACLE_HOME=/app/oracle/instantclient_18_3
ENV LD_LIBRARY_PATH=/app/oracle/instantclient_18_3

WORKDIR /app
COPY . /app

RUN apt-get update 
RUN apt-get install -y libaio1 
RUN pip3 install -i https://mirrors.aliyun.com/pypi/simple pipenv --trusted-host mirrors.aliyun.com 
RUN pipenv install --system --verbose --ignore-pipfile --deploy

CMD python run_pro.py

