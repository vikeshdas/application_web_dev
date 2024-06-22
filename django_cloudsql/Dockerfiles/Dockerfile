FROM python:3

WORKDIR /timbba_django
COPY . /timbba_django



RUN pip install --upgrade pip

RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y dos2unix

COPY configuration /configuration

COPY timbba /timbba
RUN dos2unix /configuration/entrypoint.sh  
RUN chmod +x /configuration/entrypoint.sh

CMD ["sh","../configuration/entrypoint.sh", "gunicorn", "-c", "../configuration/gunicorn_config.py", "timbba_django/timbba.wsgi:application"]
# CMD ["sh","entrypoint.sh", "gunicorn", "-c", "gunicorn_config.py", "timbba.wsgi:application"]

# # Use the official Python image from the Docker Hub
# FROM python:3

# # Set the working directory in the container
# WORKDIR /timbba_django

# # Copy the current directory contents into the container at /timbba_django
# COPY . /timbba_django/

# # Upgrade pip
# RUN pip install --upgrade pip

# # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

# # Update apt-get and install dos2unix
# RUN apt-get update && \
#     apt-get install -y dos2unix

# # Copy the entrypoint script into the container
# COPY /Dockerfiles/entrypoint.sh /entrypoint.sh

# # Convert entrypoint.sh to Unix format and make it executable
# RUN dos2unix /entrypoint.sh  
# RUN chmod +x /entrypoint.sh

# # Specify the entrypoint script and default command to run
# ENTRYPOINT ["sh", "configuration/entrypoint.sh"]
# CMD ["gunicorn", "-c", "configuration/gunicorn_config.py", "../timbba.wsgi:application"]
