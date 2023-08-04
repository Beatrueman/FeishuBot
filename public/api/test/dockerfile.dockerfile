FROM python:3.9

ADD . /app

WORKDIR /app

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["python","Test.py"]