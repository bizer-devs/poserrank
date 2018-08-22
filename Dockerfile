# Starting image to work from; apparently the most widely used docker image for flask
FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./ /poserrank
RUN pip install -r /poserrank/requirements.txt