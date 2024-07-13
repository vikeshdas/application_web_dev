FROM python:3.9-bullseye

RUN apt-get update && apt-get install -y dos2unix

WORKDIR /django_cloudsql
COPY . /django_cloudsql

# COPY application_default_credentials.json /django_cloudsql/application_default_credentials.json

ENV GOOGLE_APPLICATION_CREDENTIALS="/application_default_credentials.json"
ENV GOOGLE_CLOUD_PROJECT="gcloud-hands-on-417608"
RUN pip install google-cloud-secret-manager
RUN pip install -r requirements.txt
RUN dos2unix docker/entrypoints/entrypoint.sh  
RUN chmod +x docker/entrypoints/entrypoint.sh
 
CMD ["sh","docker/entrypoints/entrypoint.sh", "gunicorn", "-c", "configuration/gunicorn_config.py", "timbba.wsgi:application"]


