FROM python:3.11.4-slim-bookworm

ARG SERVER_USER=gunicorn-user
ARG BUILD_FILE=requirements.txt
ARG PORT=5000
COPY ./${BUILD_FILE} .

RUN apt-get update -y && \
	DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC && \
	apt-get install -y python3-pip python3-dev && \
	useradd ${SERVER_USER} && \
	usermod -aG www-data ${SERVER_USER} && \
	pip install -r ${BUILD_FILE} && \
	rm ${BUILD_FILE}

COPY ./application /orodha-notification-service/application
COPY ./scripts/server_scripts/server_start.sh /orodha-notification-service
RUN chmod +x /orodha-notification-service/server_start.sh 

WORKDIR /orodha-notification-service

CMD /orodha-notification-service/server_start.sh  -u ${SERVER_USER} -p ${PORT}
