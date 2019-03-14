|build-status|

SageCreator
===========

| SageCreator is a package meant to simplify cluster setup for Machine Learning in AWS.
| It does all the heavy lifting to get cluster up and running in a matter of minutes on any of the AWS instance type(s).
| It uses **spot instances** by default which can significantly reduce total cost of running the cluster.
| If spot instances are not available or the specified spot instance price is too low, it falls back to **on-demand** instances.
|
| You can access **Jupyter notebook** that can run your code against provisioned server(s). See `Jupyter access`_ for more info.

Installation
------------

Install and update using `pip`_:

.. code-block:: text

    $ pip install sagecreator

Python 3 is required and it is highly recommended to install and run the package in `virtualenv`_.
Supported in Python >= 3.5.0.

.. _pip: https://pip.pypa.io/en/stable/quickstart/

.. _virtualenv: https://virtualenv.pypa.io/en/stable/


Prerequisites
-------------

**AWS Account**

To provision the cluster you need an `AWS Account`_ and an IAM user with:

- Access Key ID
- Secret Access Key

User should either be in **Administrators** group as described in `IAM user`_ tutorial, or create a `custom IAM policy`_

Execution
---------

After the installation, configure the tool by specifying configuration parameters:

.. code-block:: text

    $ sage configure
    Access key id: <AWS Access Key ID>
    Secret access key: <AWS Secret Access Key>
    Company: <Name of your organization>
    Owner: <Name of your team>
    Key pair name: <Name of the key pair> (Optional - if NOT provided it will be created with a new private key)
    Private key file: <Absolute path to private key file> (required only if Key pair name was provided)

| **Company**, **Owner**, **Service** are required - those are used as tags for each instance in the cluster.
| **Key pair name**, **Private key file** are optional - if provided, given 'key pair name' / 'private key file' will be used to provision the cluster.

---------

| Provision the cluster.
| Provision step can take up to 20 minutes depending on the network connection, cluster size, and instance type.

.. code-block:: text

    $ sage provision
    Service: <Name of your service>
    Instance type [t3.small]: <Instance type> (Optional, defaults to t3.small)
    Spot instance price [0.1]: <Spot instance price> (Optional, defaults to $0.1 per instance)
    Cluster size [1]: <Cluster size> (Optional, defaults to 1 node)

.. image:: https://s3.amazonaws.com/evoneutron/github/sagecreator/provision1080.gif

| **Important**:
| The tool provides NO guarantee that the instance(s) will be provisioned at specified **Spot instance price**.
| If specified price is lower than the current AWS spot instance price then **On-demand** instance(s) will be provisioned instead.
| Thus, it is up to the user to ensure that specified price is high enough for the request to be fulfilled.

---------

| Display path of the cluster configuration file.
| Though not necessary it is possible to manually edit that file with customizations prior to running **provision** step.

.. code-block:: text

    $ sage pwd

---------

| Terminate cluster. This operation terminates all cluster nodes matching tags tuple of **Company**, **Owner**, **Service**.

.. code-block:: text

    $ sage terminate
    Service: <Name of your service to terminate>

.. _Jupyter access:

Jupyter access
--------------

| Once provisioning step is done and the cluster is up you can access jupyter notebook in your browser at http://localhost:9000.
| We have provided a sample notebook to execute. It trains the model on Fashion MNIST dataset using CNN in Keras.

Under the hood
--------------

| The logic that orchestrates the cluster is written in `Ansible`_

.. _custom IAM policy:

Custom IAM policy
-----------------

Alternatively, instead of assigning user to **Administrators** group which has access to all AWS services (as described in `IAM user`_), you can create separate Group named **Provisioners** with more restrictive policy:

.. code-block:: text

    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "ec2:*",
          "Effect": "Allow",
          "Resource": "*"
        },
        {
          "Action": "rds:*",
          "Effect": "Allow",
          "Resource": "*"
        },
        {
          "Action": "route53:*",
          "Effect": "Allow",
          "Resource": "*"
        }
      ]
    }

Then assign the user to the **Provisioners** group which has access to a subset of AWS services that are sufficient to orchestrate the cluster.


SSH access
----------

| If **Key pair name** / **Private key file** were NOT provided when configuring the cluster then default key pair is created and a new private key is stored locally.
| In order to ``ssh`` into the servers point ``ssh`` to the correct (private key) file:

.. code-block:: text

    $ ssh -i <path to private key file> ubuntu@<host>

where *path to private key file* is ``../venv/lib/python3.X/site-packages/sagebase/.ssh/pkey.pem``


.. |build-status| image:: https://travis-ci.com/evoneutron/sagecreator.svg?branch=master
    :target: https://travis-ci.com/evoneutron/sagecreator

.. _`AWS Account`: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html#sign-up-for-aws

.. _`IAM User`: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html#create-an-iam-user

.. _`Ansible`: https://www.ansible.com
