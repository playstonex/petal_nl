
FROM debian:latest

# Update
RUN apt-get update && apt-get install -y \
    python\
    python-pip\ 
    libicu-dev\ 
    python-numpy

# Install app dependencies
RUN pip install polyglot flask gunicorn gevent

WORKDIR /usr/src/app

COPY ./* ./

EXPOSE 8888

CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]
