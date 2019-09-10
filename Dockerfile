
FROM debian:latest

# Update
RUN apt-get update && apt-get install -y \
    python3\
    python3-pip\ 
    python-numpy\
    wget

# Install app dependencies
RUN pip3 install NumPy SciPy
RUN pip3 install fasttext flask gunicorn gevent

WORKDIR /usr/src/app

COPY ./* ./

RUN wget https://www.dropbox.com/s/59l7vwm0u0vq58u/lid.176.bin\?dl\=0

EXPOSE 8888

CMD ["gunicorn", "app:app", "-c", "gunicorn.conf.py"]
