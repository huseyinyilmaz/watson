DOCKER_COMPOSE = docker-compose
mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
current_dir := $(dir $(mkfile_path))

.PHONY: down up restart

all: restart

down:
	$(DOCKER_COMPOSE) down --remove-orphans

up:
	$(DOCKER_COMPOSE) up --force-recreate --build

restart: down up


bash:
	$(DOCKER_COMPOSE) exec web bash

sh:
	$(DOCKER_COMPOSE) exec web sh

logs:
	$(DOCKER_COMPOSE) logs

ps:
	$(DOCKER_COMPOSE) ps

reset_db:
	$(DOCKER_COMPOSE) exec web	sh -c " \
		cd /watson/watson; \
		rm db.sqlite3 ; \
		rm ./*/migrations/000*.py ; \
		python manage.py makemigrations ; \
		python manage.py migrate ;"

user:
	$(DOCKER_COMPOSE) exec web	sh -c " \
		cd /watson/watson; \
		python manage.py createsuperuser; "

web:
	$(DOCKER_COMPOSE) up --scale web=0 web ;
	docker stop watson_web || echo "watson_web is not running..." ;
	echo ${pwd} ;
	docker run -ti --rm \
		--name=watson_web \
		-v $(current_dir):/watson \
		-p 8000:8000 \
		--network=watson_default \
		huseyinyilmaz/watson-dev-backend-base \
		sh -c "cd /watson/watson/ && python3 manage.py runserver 0.0.0.0:8000" ;
