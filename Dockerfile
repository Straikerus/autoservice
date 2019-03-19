FROM alpine:latest

WORKDIR /app/

ADD ./requirements.txt .

RUN apk add --no-cache ca-certificates && update-ca-certificates
RUN apk add --update --no-cache python3
RUN apk add --update --no-cache postgresql-dev
RUN apk add --no-cache --virtual=build-dependencies wget ca-certificates build-base python3-dev musl-dev
RUN wget --no-check-certificate "https://bootstrap.pypa.io/get-pip.py" -O /dev/stdout | python3

RUN echo "http://dl-3.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories
RUN apk update

RUN apk add --update --no-cache libmagic jpeg-dev zlib-dev \
    freetds freetds-dev unixodbc unixodbc-dev libstdc++

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn meinheld

ADD . .

EXPOSE 80

ENV DJANGO_SETTINGS_MODULE=autoservice.settings_prod

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
