FROM python:3.8-slim

RUN pip install --upgrade pip setuptools wheel 
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Copy the requirements into the image
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from local to the image
COPY . /app

CMD ["python3", "/app/app.py"]