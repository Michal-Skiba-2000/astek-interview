FROM python:3.10.2
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /
RUN pip3 install -r requirements.txt
WORKDIR /emenu
