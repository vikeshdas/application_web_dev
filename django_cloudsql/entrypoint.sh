
python manage.py makemigrations timbba
python manage.py migrate timbba

gunicorn -b :$PORT timbba.wsgi
