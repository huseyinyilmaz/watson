.PHONY: build

TAG = huseyinyilmaz/watson-dev-backend-base
all: build push

build:
	docker build . --tag=$(TAG)

push:
	docker push $(TAG)
