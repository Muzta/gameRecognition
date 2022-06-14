FROM python:3.8-alpine

RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --upgrade pip setuptools wheel

# Copy the requirements into the image
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

# Copy everything from local to the image
COPY . /app

ENTRYPOINT [ "python" ]

CMD ["app.py"]