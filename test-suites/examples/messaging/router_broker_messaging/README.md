# Messaging through a Router or Broker example

This example demonstrates loading an iQA instance from an Ansible inventory
file and exchanging messages through a Router or a Broker component using the
following client implementations: Qpid JMS (Java), Qpid Python Proton, and RHEA (NodeJS).

It is important to mention that this is not using any automation testing framework,
so it can be executed with Python 3.

## Running the example

This example provides two inventory files. One of them named as 'inventory_broker_docker.yml'
defines a Broker component and the three client components (Java, Python and NodeJS).

The other inventory file named as 'inventory_router_docker.yml' defines a Router component
and the same three client components.

The container names that will be created are:
* **router1** *or* **broker1**
* **cli-java**
* **cli-proton-python**
* **cli-rhea**

***Note:** You can adjust the container names if needed.* 

* To create a virtual environment that can be used by all examples, execute (or skip it
if you have already done it before):

    ```make venv```
    
* Once you have your virtual environment, you can run one of the following commands:

    1. To exchange messages through a Router component:
    
        ```make router```
    
        It will create (or start) a router1 container, all three client containers mentioned
        above and execute a small Python script to exchange messages through the Router component.
    
    2. To exchange messages through a Broker component:

        ```make broker```
    
        It will create (or start) a broker1 container, all three client containers mentioned
        above and execute a small Python script to exchange messages through the Broker component.
