FROM tiangolo/uwsgi-nginx-flask:python3.5

COPY ./POA_Website /app

ENV STATIC_PATH /app/Pitzer_Outdoor_Adventure/static
