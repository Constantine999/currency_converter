FROM python:3.12


ENV PYTHONUNBUFFERED=1

WORKDIR /currency_convertor

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY src .
