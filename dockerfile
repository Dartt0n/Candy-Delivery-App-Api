FROM python:3.9

RUN mkdir /usr/src/candy-api
WORKDIR /usr/src/candy-api

EXPOSE 8080

COPY . /usr/src/candy-api
RUN pip install -r /usr/src/candy-api/requirements.txt

CMD ["python3", "main.py"]
