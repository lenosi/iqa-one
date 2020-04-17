VENV_DIR=../../venv
REQUIREMENTS=../../../requirements.txt
SAMPLE=iqa_one_broker_cluster_sample.py

all: docker
.PHONY: clean venv docker

clean:
	# Useful when you have old venv
	@echo "Removing virtual env: $(VENV_DIR)"
	rm -rf $(VENV_DIR) || true
	
venv: clean
	@echo "Creating virtual env: $(VENV_DIR)"
	virtualenv -p python3 $(VENV_DIR)
	. $(VENV_DIR)/bin/activate && pip install -r $(REQUIREMENTS)
	
run:
	@echo "Running: python $(SAMPLE)"
	@echo "Read the inventory file for more information"
	@echo
	@[[ -d $(VENV_DIR) ]] || echo -en "Virtual env does not exist: $(VENV_DIR)\nRun: make venv\n"
	@. $(VENV_DIR)/bin/activate && python $(SAMPLE) $(INVENTORY)

run-container:
	@echo "Executing artemis broker as a local container named 'broker1'"
	@echo
	@docker run -itd --name broker1 rhmessagingqe/artemis:latest 2> /dev/null || docker start broker1
	@echo Waiting for container to start...
	@sleep 10

docker: INVENTORY=inventory_docker.yml
docker: run-container run
	@echo
	@echo "Stopping broker1 container"
	@docker stop broker1 || true
	@echo "Note: This sample created a container named 'broker1'. Please remove it as needed."
