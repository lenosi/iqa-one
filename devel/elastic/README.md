# IQA Elasticsearch logging example

This example demonstrates the usage of the Elastic Stack for logging in the IQA framework.

Elastic Stack is deployed using Docker.

## Running the example

* To deploy the Elastic Stack, open a separate terminal tab or window and run

    ```make```
    
  and wait for all containers to start properly (until you see `filebeat` and `journalbeat` containers
  output JSON data about gathered logs in the terminal)
  
* After that, to run the Python example, execute

    ```make example```
    
  which produces and consumes 100 messages and then displays all results with the 'broker' keyword using Python. 

* To remove containers and network created by this example, run

    ```make clean```

