FROM python:3.11



ENV PYTHONUNBUFFERED True

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt


COPY service-account-key.json /app/service-account-key.json

ENV GOOGLE_APPLICATION_CREDENTIALS="/app/service-account-key.json"
ENV INSTANCE_CONNECTION_NAME="solid-scope-415202:asia-southeast2:servcdet"
ENV CLOUDSQL_PROXY_SOCK="/cloudsql/$INSTANCE_CONNECTION_NAME"
ENV MYSQL_USER="root"
ENV MYSQL_PASSWORD="123456"

EXPOSE $PORT

CMD ["waitress-serve", "--call", "app:create_wsgi_app"]
# CMD ["python","app.py"]