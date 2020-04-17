VENV_DIR=../../venv
REQUIREMENTS=../../../requirements.txt
SAMPLE=iqa_messaging_sample.py

all: router
.PHONY: clean venv clients run run-container local ssh docker

clean: docker-clean
	# Useful when you have old venv
	@echo "Removing virtual env: $(VENV_DIR)"
	rm -rf $(VENV_DIR) || true

docker-clean:
	@echo "Removing created containers:"
	@docker rm -f cli-java cli-rhea cli-proton-python broker1 router1 || true

venv: clean
	@echo "Creating virtual env: $(VENV_DIR)"
	virtualenv -p python3 $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install -r $(REQUIREMENTS)

clients:
	@echo "Executing client containers (cli-java, cli-proton-python and cli-rhea)"
	@docker run -itd --name cli-java rhmessagingqe/cli-java 2> /dev/null || docker start cli-java || true
	@docker run -itd --name cli-proton-python rhmessagingqe/cli-proton-python 2> /dev/null || docker start cli-proton-python || true
	@docker run -itd --name cli-rhea rhmessagingqe/cli-rhea:centos7 2> /dev/null || docker start cli-rhea || true

run: clients
	@echo
	@echo "Running: python $(SAMPLE)"
	@echo "Read the inventory file for more information"
	@echo
	@[[ -d $(VENV_DIR) ]] || echo -en "Virtual env does not exist: $(VENV_DIR)\nRun: make venv\n"
	@. $(VENV_DIR)/bin/activate && python $(SAMPLE) $(INVENTORY)

run-router:
	@echo "Stopping running brokers"
	@docker stop broker1 || true
	@echo "Executing dispatch router as a local container named 'router1'"
	@docker run -itd --name router1 rhmessagingqe/qpid-dispatch:ubuntu1804 2> /dev/null || docker start router1

router: INVENTORY=inventory_router_docker.yml
router: run-router run
	@echo
	@echo "Stopping containers"
	@docker stop router1 cli-java cli-proton-python cli-rhea || true
	@echo
	@echo "Note: This sample created four containers named:"
	@echo "      - router1"
	@echo "      - cli-java"
	@echo "      - cli-proton-python"
	@echo "      - cli-rhea"
	@echo "Please remove them as needed or using make docker-clean."

run-broker:
	@echo "Executing apache artemis as a local container named 'broker1'"
	@docker run -itd --name broker1 rhmessagingqe/artemis:latest 2> /dev/null || docker start broker1
	@echo Waiting for container to start...
	@sleep 10

broker: INVENTORY=inventory_broker_docker.yml
broker: run-broker run
	@echo
	@echo "Stopping containers"
	@docker stop broker1 cli-java cli-proton-python cli-rhea || true
	@echo
	@echo "Note: This sample created four containers named:"
	@echo "      - broker1"
	@echo "      - cli-java"
	@echo "      - cli-proton-python"
	@echo "      - cli-rhea"
	@echo "Please remove them as needed or using make docker-clean."
