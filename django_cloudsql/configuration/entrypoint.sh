#!/bin/sh
wait_for_mysql() {
  until python -c "import socket; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(('cloudsql_proxy', 3307))" >/dev/null 2>&1
  do
    echo "Waiting for MySQL service to start..."
    sleep 5
  done
}

wait_for_mysql

python manage.py makemigrations timbba
python manage.py migrate timbba

exec "$@"