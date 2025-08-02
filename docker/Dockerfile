FROM python:3.13-slim

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .
RUN chmod +x start.sh