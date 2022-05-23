FROM python:3.10
RUN apt-get update
RUN apt-get install libgl1 -y
WORKDIR /app/
COPY . /app/
RUN pip install -r requirements.txt
