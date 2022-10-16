.PHONY: help backup docker-uild docker-browser docker-login
.DEFAULT_GOAL := help

VERSION=0.1
DOCKER_IMAGE=ricfio/adsbot:$(VERSION)
WORKDIR=/workspaces/adsbot

help:
	@awk 'BEGIN {FS = ":.*#"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\n"} /^[a-zA-Z0-9_-]+:.*?#/ { printf "  \033[36m%-27s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST); printf "\n"

backup: ## Backup
backup: source=$(shell basename $(CURDIR))
backup: target=$(shell echo `pwd`_`date +'%Y%m%d_%H%M'`.tar.gz)
backup: 
	@cd .. && tar -czf $(target) $(source) && ls -l $(source)_*.tar.gz

docker-build: ## Build docker image
	@docker build -t $(DOCKER_IMAGE) .

docker-browser: ## Run google chrome from docker container
	@docker run --rm $(DOCKER_IMAGE) bash -c 'google-chrome-stable --no-sandbox --display=host.docker.internal:0.0 --disable-dev-shm-usage'

docker-login: ## Login docker container
docker-login: pwd=`pwd`
docker-login:
	@docker run -it --rm --workdir=$(WORKDIR) --volume=$(pwd):$(WORKDIR) --user=vscode $(DOCKER_IMAGE) bash
