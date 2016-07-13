FROM python:2.7.12

ENV PYTHONIOENCODING UTF-8

EXPOSE 81

# install requirements - https://support.aptible.com/topics/paas/how-to-set-up-pip-caching/
ADD requirements.txt /app/

WORKDIR /app/
RUN pip install -r requirements.txt

ADD . /app/
# Set the default directory where CMD will execute

VOLUME [/app]

ENTRYPOINT ["/app/docker-entrypoint.sh"]