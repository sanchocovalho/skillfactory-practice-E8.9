FROM python:3.7.6
EXPOSE 5000/tcp
EXPOSE 6379/tcp
EXPOSE 5432/tcp
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app/