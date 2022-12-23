FROM python:3.10.6-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update -y && apt install -y libsnappy-dev
RUN pip install -r requirements.txt

COPY . .
ENV DJANGO_SETTINGS_MODULE=WebPushNotif.settings.production

RUN chmod +x /usr/src/app/run.sh
CMD /bin/bash -c "/usr/src/app/run.sh"
