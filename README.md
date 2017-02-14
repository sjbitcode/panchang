# panchang
Get daily panchang emails at 6:30AM EST.

---

A Python-Celery-RabbitMQ project with Docker and Docker Compose.

---

### Installing

You'll need to install the following to set up and run the project:
- [Docker](http://www.docker.com/) - Build, Ship and Run your application as containers
- [Docker Compose](https://docs.docker.com/compose/) - A tool for defining and running multi-container Docker applications

Follow the instructions to [install Docker on your OS](https://www.docker.com/products/overview#/install_the_platform).

---

### Containers

This project uses the following docker containers:

#### rabbit
The message broker for celery. Runs on port _5672_.

#### worker
The python-celery application to scrape data and send emails. This container will be running celery and links to the **rabbit** container.

---

### Setup

Copy the `docker-compose-production.yml` file and replace the email configurations with your own email data.

Run `docker-compose -f docker-compose-production.yml up -d` to build the containers and run in daemon mode.

---

### Logging

All activity is recorded in one log, located in `logs/` in the directory where the Docker containers are running.

---

### Commands

Good to know Docker commands.

`docker-compose up` - Builds, (re)creates, starts, and attaches to containers.
- Pass the `-d` flag to run in _detached_ mode.

`docker-compose ps` - Check the status of containers.

`docker-compose logs` - View combined logs.
- Pass the `-f` flag to follow output.

`docker-compose logs <service>` - View the logs of one service.

`docker-compose stop` - Stop running containers.
- Pass the `-t` flag to specify a shutdown time in seconds.

`docker-compose rm` - Remove stopped containers.
- Pass the `-f` flag to force removal.
- Pass the `-v` flag to remove volumes attached to containers.

`docker-compose run <service> <command>` - Run a one-off command on a container.
- Pass the `--rm` flag to remove the container after run.

