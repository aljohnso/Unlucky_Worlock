FROM tiangolo/uwsgi-nginx-flask:python3.5

COPY ./POA_Website/requirements.txt /tmp/
COPY ./POA_Website /app

RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

ENV STATIC_PATH /app/POA_Website/Pitzer_Outdoor_Adventure/static
ENV STATIC_URL /static
