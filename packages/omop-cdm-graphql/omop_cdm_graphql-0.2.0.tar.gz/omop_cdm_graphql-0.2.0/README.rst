====================
OMOP CDM GraphQL
====================

GraphQL service for exposing OMOP CDM records.

Exported scripts
================

* load-omop-cdm-db-records
* run-omop-cdm-graphql-app

Step 1 - Create Python virtual environment
==========================================

.. code-block:: shell

    python3 -m venv venv

Step 2 - Activate Python virtual environment
============================================

.. code-block:: shell

    source venv/bin/activate

Step 3 - Install
================

.. code-block:: shell

    pip install omop-cdm-graphql

Step 4 - Update the configuration file
======================================

.. code-block:: yaml

    ---
    port: 8081
    url: http://localhost
    database_file: /tmp/omop-cdm-graphql/omop-cdm-v1.db

Step 5 - Copy configuration file to launch directory
====================================================

.. code-block:: bash

    cp venv/lib/python3.10/site-packages/omop_cdm_graphql/conf/config.yaml .

Step 6 - Load the database
==========================

Run the loader to load mock records.

.. code-block:: bash

    load-omop-cdm-db-records

Step 7 - Run the app
====================

.. code-block:: bash

    run-omop-cdm-graphql-app

Step 8 - Open browser
=====================

`http://localhost:8080/graphql <http://localhost:8080/graphql>`_

References
==========

- `GitHub <https://github.com/jai-python3/omop-cdm-graphql>`_
- `PYPI <https://pypi.org/project/omop-cdm-graphql/>`_
