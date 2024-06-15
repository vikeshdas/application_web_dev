FROM python:3


COPY . /timbba_django

WORKDIR /timbba_django

RUN pip install --upgrade pip

RUN pip install -r requirements.txt


CMD ["gunicorn", "-c", "configuration/gunicorn_config.py", "timbba.wsgi:application"]
