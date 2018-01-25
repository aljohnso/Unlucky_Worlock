<<<<<<< HEAD
FROM tiangolo/uwsgi-nginx-flask:python3.5

COPY ./POA_Website/requirements.txt /tmp/
COPY ./POA_Website /app
COPY ./POA_Website/Pitzer_Outdoor_Adventure/static /app/static

# URL under which static (not modified by Python) files will be requested
# They will be served by Nginx directly, without being handled by uWSGI
ENV STATIC_URL /static
# Absolute path in where the static files wil be
ENV STATIC_PATH /app/Pitzer_Outdoor_Adventure/static


RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt


=======
# Use an official Python runtime as a parent image
FROM python:3.5

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME POA_web

# Run app.py when the container launches
CMD ["python", "./POA_Website/run.py"]
>>>>>>> Production
