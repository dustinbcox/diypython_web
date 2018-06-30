FROM gcr.io/google_appengine/python

RUN apt-get update && apt-get upgrade -y && apt-get install -y ncurses-dev
RUN virtualenv -p python3.6 /env
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
ADD . /app
CMD $PROCESSES
EXPOSE 5000
