FROM python:3.9-bullseye

RUN apt-get update && apt-get install -y dos2unix

WORKDIR /django_cloudsql
COPY . /django_cloudsql

ENV GOOGLE_APPLICATION_CREDENTIALS="/application_default_credentials.json"
ENV GOOGLE_CLOUD_PROJECT="gcloud-hands-on-417608"
ENV PORT 4200
# ENV HOST 0.0.0.0
RUN pip install -r requirements.txt
RUN dos2unix docker/entrypoints/entrypoint.sh  
RUN chmod +x docker/entrypoints/entrypoint.sh
 
# CMD ["sh","docker/entrypoints/entrypoint.sh", "gunicorn", "-c", "configuration/gunicorn_config.py", "timbba.wsgi:application"]
CMD ["sh","docker/entrypoints/entrypoint.sh"]


