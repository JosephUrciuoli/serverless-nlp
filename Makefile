DOCKER_IMAGE = $(docker_image)
DOCKER_REPO = $(docker_repo)
PROFILE = $(aws_profile)
VERSION = latest

P="\\033[34m[+]\\033[0m"

.PHONY: build
build:
	@echo "  $(P) build"
	docker build -t $(DOCKER_IMAGE):$(VERSION) .

.PHONY: push
push:
	@echo "  $(P) push"
	eval `aws ecr get-login --profile $(aws_profile) --region $(aws_region) --no-include-email`
	docker tag $(DOCKER_IMAGE):$(VERSION) $(DOCKER_REPO):$(VERSION)
	docker push $(DOCKER_REPO):$(VERSION)

.PHONY: lint
lint:
	@echo "  $(P) lint"
	pylint ./docker-resources cmd.py

.PHONY: format
format:
	@echo "  $(P) format"
	black ./docker-resources cmd.py





