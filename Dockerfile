FROM python:3

WORKDIR /opt/jira_devops

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy app
COPY . .

# set production properties
ENV DJANGO_SETTINGS_MODULE=settings.production

# build static files (set up minimum required env properties)
RUN JIRA_SERVER='dummy' JIRA_USERNAME='dummy'  JIRA_PASSWORD='dummy' python manage.py collectstatic --noinput
RUN JIRA_SERVER='dummy' JIRA_USERNAME='dummy'  JIRA_PASSWORD='dummy' python manage.py compress

EXPOSE 8000
# start HTTP server
CMD ["python", "manage.py", "runserver", "--noreload", "0.0.0.0:8000"]
# start HTTPS server, uncomment requrements.txt and defaults.py before switching
#CMD ["python", "manage.py", "runserver_plus", "--threaded", "--noreload", "--cert-file", "auto_crt", "0.0.0.0:8000"]
