FROM python:3.9-alpine3.13

LABEL maintainer = "marcoding78@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

#directory
COPY . .

#sets working directory for container to run
WORKDIR /.

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home bot && \
    chmod -R +x /scripts


#to use python from our env to
#dont use full path like "/py/bin/..."
#adding /scripts to not type full path of
#scripts that we want to run
ENV PATH="/scripts:/py/bin:$PATH"

#switch to app user
USER bot

CMD ["run.sh"]