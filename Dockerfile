FROM woahbase/alpine-rpigpio:armhf

# This hack is widely applied to avoid python printing issues in docker containers.
# See: https://github.com/Docker-Hub-frolvlad/docker-alpine-python3/pull/13
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3"]

COPY . /var/www/

RUN pip3 install -r /var/www/requirements.txt

EXPOSE 5000

CMD [ "/var/www/busy-flag.py" ]
