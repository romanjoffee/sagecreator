|build-status|

SageCreator
===========
|
| SageCreator is a package meant to simplify cluster setup for Machine Learning in AWS.
| It does all the heavy lifting to get cluster up and running in a matter of minutes on any of the AWS instance type(s).
| It is using **spot-instances** by default which can significantly reduce total cost of running the cluster.
| If spot instance(s) are not available or the spot-instance price is too low, it falls back to **on-demand** instance(s).
|
| After provision you can access **jupyter notebook** that can run your code against provisioned server(s)

Installation
------------

Install and update using `pip`_:

.. code-block:: text

    $ pip install sagecreator

Python is required and it is highly recommended to install and run the package in `virtualenv`_.
Supported in Python >= 3.5.0.

.. _pip: https://pip.pypa.io/en/stable/quickstart/

.. _virtualenv: https://virtualenv.pypa.io/en/stable/


Prerequisites
-------------

**AWS Account**

To provision the cluster you need an IAM user with:

- Access Key ID
- Secret Access Key
- Key pair (optional) - if not provided it will be generated and stored locally


Execution
---------

After the installation, configure the tool by specifying configuration parameters:

---------

.. code-block:: text

    $ sage configure

| **Instance type**, **Spot price**, **Cluster size** are set to default values but can be specified per your requirements.
| **Company**, **Owner**, **Service** should be specified - those are used as tags for each instance in the cluster.

---------

.. code-block:: text

    $ sage provision

| Provision cluster. Provision step can take up to 20 minutes depending on network connection, cluster size, and instance type.

---------

.. code-block:: text

    $ sage pwd

Displays path of the configuration file that has full cluster configuration. Though not necessary it is possible to manually edit that file with customizations.

---------

.. code-block:: text

    $ sage terminate

Terminate cluster. This operation terminates all cluster nodes matching tags tuple of **Company**, **Owner**, **Service**.

|

Jupyter access
--------------

| Once provision step is done and cluster is up you can access jupyter notebook on http://localhost:9000
| We have provided a sample notebook to train a model on Fashion MNIST dataset using CNN in Keras
|

Under the hood
--------------

| The logic that orchestrates the cluster and deploys the software is written in **Ansible**
|


.. |build-status| image:: https://travis-ci.com/evoneutron/sagecreator.svg?branch=master
    :target: https://travis-ci.com/evoneutron/sagecreator
