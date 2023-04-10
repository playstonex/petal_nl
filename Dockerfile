
FROM debian:latest

# Update
RUN apt-get update && apt-get install -y \
    python3\
    python3-pip

# Install app dependencies
RUN pip3 install flask gunicorn gevent zhconv fasttext fastlid hanzidentifier

WORKDIR /usr/src/app

COPY ./* ./

EXPOSE 8888

CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]
