FROM python:3

RUN apt -qq -y update && apt -qq -y upgrade

ENV APP /app
RUN mkdir $APP
WORKDIR $APP

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

CMD ["uwsgi","app.ini"]
