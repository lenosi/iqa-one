all: docker

# Create and start Elastic stack Docker containers and network
docker:
	docker-compose up

# Remove created Elastic stack Docker containers and network
clean:
	docker-compose down

# An example of running the IQA Elasticsearch Python client searching for the 'broker' keyword
example:
	docker exec -it broker_logging /bin/bash -c "~/bin/artemis producer --destination iqa_logging --message-count 100 --url tcp://localhost:61616 --user user --password password"
	docker exec -it broker_logging /bin/bash -c "~/bin/artemis consumer --destination iqa_logging --message-count 100 --url tcp://localhost:61616 --user user --password password"
	python3 iqa-elasticsearch.py -op -k broker