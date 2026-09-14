DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
STORAGES_FILE = docker_compose/storages.yaml
BROKERS_FILE = docker_compose/brokers.yaml

.PHONY: storages
storages:
	${DC} -f ${STORAGES_FILE} ${ENV} up --build -d

.PHONY: storages-down
storages-down:
	${DC} -f ${STORAGES_FILE} down

.PHONY: brokers
brokers:
	${DC} -f ${BROKERS_FILE} ${ENV} up --build -d

.PHONY: brokers-down
brokers-down:
	${DC} -f ${BROKERS_FILE} down
