FROM python:3


COPY . /timbba_django

WORKDIR /timbba_django

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN chmod +x configuration/entrypoint.sh


CMD ["sh", "configuration/entrypoint.sh"]
