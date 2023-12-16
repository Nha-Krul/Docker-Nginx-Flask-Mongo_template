FROM python:3.10-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
RUN python -m pip install --upgrade pip
COPY website/requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt
RUN pip install gunicorn gevent

# copy project - Siempre es relativo al contecto del docker-compose.yml
COPY ./website/ /var/www/

WORKDIR /var/www/app

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080","app:application", "-k", "gevent", "--worker-connections", "100"]
