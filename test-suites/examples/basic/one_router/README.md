# One Router example

This example demonstrates loading an iQA instance from an Ansible inventory
file and managing a Router component.

It is important to mention that this is not using any automation testing framework,
so it can be executed with Python 3.

## Running the example

This example provides a single inventory file defined with a Router component which
is supposed to be running in a docker container.

The container name that will be created is 'router1'.

***Note:** You can adjust the container name if needed.* 

* To create a virtual environment that can be used by all examples, execute (or skip it
if you have already done it before):

    ```make venv```
    
* Once you have your virtual environment, you can run:

    ```make```
    
    It will create (or start) a router1 container and execute a small Python script
    to manage and communicate with the Broker instance.
    
