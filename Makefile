IMAGE_NAME = mohamedaziz0801/simple-flask-login

TAG ?= latest

.PHONY: build push all

build_push: build push

build:
	@echo "Building Docker image with tag: $(TAG)"
	docker build -t $(IMAGE_NAME):$(TAG) .

push:
	@echo "Pushing Docker image to registry..."
	docker push $(IMAGE_NAME):$(TAG)