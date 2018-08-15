FROM python:3.6-slim

LABEL Name=quatek_web_app_backend Version=0.0.1
EXPOSE 5001

ENV ENV=production
ENV DEBUG=True
ENV MONGODB_HOST=mongo
ENV REDIS_URL=redis://redis
ENV SOCKET_HOST=0.0.0.0

WORKDIR /app
COPY . /app

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pipenv --trusted-host pypi.tuna.tsinghua.edu.cn && \
    pipenv install --ignore-pipfile

CMD ["pipenv", "run", "python3", "run_pro.py"]

