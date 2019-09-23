VENV_DIR=../../venv
REQUIREMENTS=../../../requirements.txt
SAMPLE=iqa_one_router_sample.py

all: docker
.PHONY: clean venv local ssh docker

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
	@echo "Executing dispatch router as a local container named 'router1'"
	@echo
	@docker run -itd --name router1 rhmessagingqe/qpid-dispatch:ubuntu1804 2> /dev/null || docker start router1

local: INVENTORY=inventory_local.yml
local: run

ssh: INVENTORY=inventory_ssh.yml
ssh: run

docker: INVENTORY=inventory_docker.yml
docker: run-container run
	@echo
	@echo "Stopping router1 container"
	@docker stop router1 || true
	@echo "Note: This sample created a container named 'router1'. Please remove it as needed."
