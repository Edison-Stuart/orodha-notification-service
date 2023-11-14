# orodha-notification-service

This service will handle the creation/storage of notifications for the Orodha app.

## Usage & Requirements

In order to use this repository there are some conditions that have to be met. You must have a `.env` file containing:

-   DOCKER_USERNAME
-   DOCKER_PASSWORD
-   TAG
-   DBROOTUSER
-   DBROOTPASSWORD
-   DBUSER
-   DBPASSWORD
-   DBNAME
-   DBHOSTNAME
-   DBPORTS
-   KEYCLOAK_SERVER_URL
-   KEYCLOAK_REALM_NAME
-   KEYCLOAK_CLIENT_ID
-   KEYCLOAK_CLIENT_SECRET_KEY

    The `docker-compose.main.yaml` file uses these variables in order to build the image using the Dockerfile as well as set up the database.

### API

#### Namespaces

There are two namespaces, `/notifications` as well as `/main`.

The `/notifications` namespace supports GET, DELETE, and POST requests which respectively obtain, remove, and create notifications.

For a GET request a user_id needs to be passed into the route as a query parameter:

```
/notifications?user_id={SOME_STR_VALUE}
```

Similarly, the DELETE request expects a notification_id query parameter, like so:

```
/notifications?notification_id={SOME_STR_VALUE}
```

At this time the DELETE request only takes one notification_id, it will be modified to accept
multiple in the future.

Without their expected query param values, the DELETE and GET requests will return errors.

The POST request does not expect and id in the route, just a form body like a typical POST request.

#### Expected Data Model

The POST request expects the data to be formated as such:

```
    {
      "targets": ["recipient_of_notification", ...],
      "list_id": "id_of_target_list",
      "notification_type": "base" or "list_invite",
    },

```

#### Headers

These routes expect the headers of

```
{"Content-Type": "application/json"}
```

and

```
{"Authorization": "Bearer {some user token provided by keycloak}"}
```

#### Building with Docker

The Dockerfile has an argument called `REQUIREMENTS_FILE` that is by default set to `requirements.txt`. For now, this can only be changed by setting an environment variable named REQUIREMENTS_FILE to the requirement file that you would like to use.

This repository contains a secondary requirements file named `dev_requirements.txt`. This file contains the tools that are required to not only run, but also test the application. In the future there are plans to utilize the profiles function of docker-compose to launch with a different requirement file depending on if the app is being run in development or production.
