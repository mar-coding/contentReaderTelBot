FROM python:3.9-alpine3.13

LABEL maintainer = "marcoding78@gmail.com"

ENV PYTHONUNBUFFERED 1

#directory
COPY . ./code

#sets working directory for container to run
WORKDIR /code

RUN python -m venv /code/py && \
    /code/py/bin/pip install --upgrade pip && \
    /code/py/bin/pip install -r /code/requirements.txt && \
    adduser --disabled-password --no-create-home bot && \
    chmod -R +x /code/scripts && \
    chown -R bot:bot /code && \
    chmod -R 755 /code 


#to use python from our env to
#dont use full path like "/py/bin/..."
#adding /scripts to not type full path of
#scripts that we want to run
ENV PATH="/code/scripts:/code/py/bin:$PATH"

#switch to app user
USER bot

CMD ["run.sh"]