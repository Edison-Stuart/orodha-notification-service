if [ -z "$BUILD_TAG" ];
  then
    echo "\$BUILD_TAG is not defined, defaulting to 'latest'"
	BUILD_TAG=latest
fi

if [ -z "$DOCKER_COMPOSE_FILE" ];
  then
    echo "\$DOCKER_COMPOSE_FILE is not defined, defaulting to 'docker-compose.yaml'"
    DOCKER_COMPOSE_FILE=docker-compose.yaml
fi

if [ -z "$DOCKER_USERNAME" ];
  then
    echo "\$DOCKER_USERNAME is not defined, cannot complete build."
	exit 1
fi

if [ -z "$DOCKER_PASSWORD" ];
  then
    echo "\$DOCKER_PASSWORD is not defined, cannot complete build."
	exit 1
fi

export IMAGE_NAME=$DOCKER_USERNAME/orodha-notification-service:$BUILD_TAG

docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD

docker-compose -f $DOCKER_COMPOSE_FILE build

docker-compose -f $DOCKER_COMPOSE_FILE push
