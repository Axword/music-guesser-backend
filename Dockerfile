FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /django
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
