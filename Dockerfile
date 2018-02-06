FROM tiangolo/uwsgi-nginx-flask:python3.5

COPY ./requirements.txt /tmp/
COPY ./POA_Website /app
COPY ./POA_Website/Pitzer_Outdoor_Adventure/static /app/static

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /app/Pitzer_Outdoor_Adventure/static


RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt
