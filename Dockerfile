# Starting image to work from; apparently the most widely used docker image for flask
FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV UWSGI_INI /poserrank/uwsgi.ini
ENV STATIC_PATH /poserrank/poserrank/static

COPY ./ /poserrank
WORKDIR /poserrank

RUN pip install -r /poserrank/requirements.txt