FROM edisonstuart/orodha-base-image-prod:latest

ARG SERVER_USER=gunicorn-user
ARG PORT=5000

RUN adduser ${SERVER_USER} -G www-data -D
USER ${SERVER_USER}

COPY ./application /orodha-notification-service/application
COPY ./scripts/server_scripts/server_start.sh /orodha-notification-service

WORKDIR /orodha-notification-service

CMD /orodha-notification-service/server_start.sh -u gunicorn-user -p ${PORT}
