FROM ubuntu:latest

WORKDIR /apis

RUN apt-get update && apt-get upgrade -y

RUN apt-get install python3-pip -y

COPY apis /apis/apis

COPY crypcentra /apis/crypcentra

COPY manage.py /apis

COPY requirements.txt /apis

RUN pip3 install -r requirements.txt

RUN python3 manage.py makemigrations apis

RUN python3 manage.py migrate

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
