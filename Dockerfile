FROM python

ARG SERVER_ADDRESS
ARG SERVER_PORT

WORKDIR /mytask_server

ENTRYPOINT pip install -r requirements.txt &&\
    cd mytask_server &&\
    python manage.py makemigrations &&\
    python manage.py migrate &&\
    python manage.py runserver ${SERVER_ADDRESS}:${SERVER_PORT}