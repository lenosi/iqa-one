# iQA Test suites

## Description

Project *iqa-testsuite* include separate test suites for Messaging.

## Ideas

0) It is primarily designed for testing messaging components/services.

1) Every test suite should use `messaging_abstration` API for writing tests.
   It is not dependant on exact component you want to use under test.

2) Components for test integration with end software.
   Under (`messaging_components`) setup under conftest.py (with iteration way?)
   Or under not yet existing plugin for py.test

3) Test suites are by default based on [pytest](https://docs.pytest.org/en/latest/) tests runner, 
   but any test framework can be used instead.

4) Possibility for end to end testing without messaging_abstraction API.

Please read `README.md` and `requirements.txt` before running.

## Needed steps

1. Prepare/Deploy required topology (must be compatible with expected test suite)
2. Describe the topology in `inventory` file (fully compatible with Ansible Inventory)
3. Related to test runner execution
    - Provide `conftest.py` in which you describe (messaging) components from Inventory file
    - Fixtures for *broker*, *client* and *router* objects
4. Write tests using calls from `messaging-abstraction` module

## Objectives

- Modular
- Scalable
- Abstract

## Dependencies and projects

Every test suite can have different dependency. Read `README.md` of every test-suite.

iqa_testsuite depends on following projects:

- messaging_abstract
- messaging_components
- iqa_common
- pytest_iqa
   
#### [(messaging_abstract) Abstraction of Middleware Messaging](https://github.com/rh-messaging-qe/messaging_components) 

Abstract classes (Facades)

- Protocols
- Message
- Client 
    - Sender
    - Receiver
    - Connector
- Broker
- Router
- Node

#### [(messaging_components) Messaging Components](https://github.com/rh-messaging-qe/messaging_components) 

Implementation of specific components based on `messaging_abstract`.

- Supported Brokers 
    - Artemis
- Supported Routers
    - Qpid Dispatch
- Supported Clients
    - Python proton
    - Command line interface clients (RHEA, Python Proton, JMS)

#### [(iqa_common) IQA Common](https://github.com/rh-messaging-qe/iqa_common) 

Common classes methods for this test suite

- IQA Instance
- Node
    - Execution

#### IQA Instance

Is provided as a pytest plugin [pytest_iqa](https://github.com/rh-messaging-qe/pytest_iqa) 

`IQA Instance` knows facts about provided topology (based on inventory file). 
Such `instance` is able to execute commands directly on a specific node in topology
or access identified messaging components directly via provided APIs.
The instance should verify compatibility with your inventory file by `test suite requirements`.

## Running test suites

### Prepare:

```bash
# Create virtual environment
virtualenv3 venv

# Activate virtual environment 
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Options

#### Inventory

Path to Inventory file with hosts and facts.

```bash
--inventory ${path_to_inventory}
```

#### Execution

Need to be executed from main `conftest.py` test-suite root directory.

```bash
./venv/bin/py.test ${test_suite_dir} --inventory /path/to/inventory
```
