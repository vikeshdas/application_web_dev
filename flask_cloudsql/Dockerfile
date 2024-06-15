FROM python:3


COPY . /timbba_flask

WORKDIR /timbba_flask

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh

# CMD ["gunicorn", "-c", "gunicorn_config.py", "timbba.wsgi:application"]
CMD ["sh", "entrypoint.sh"]