FROM python:3


COPY . /timbba_flask

WORKDIR /timbba_flask

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:create_app()"]
