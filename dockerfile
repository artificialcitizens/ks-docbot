# Use the official Python image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

RUN apt-get update
RUN apt-get install -y g++

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "pdf_bot.py"]