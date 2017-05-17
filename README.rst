lp-jira-sync
============

Launchpad JIRA sync tool

Usage
-----

::

    giraffe% virtualenv venv
    giraffe% . ./venv/bin/activate
    (venv) giraffe% pip install .
    (venv) giraffe% rehash
    (venv) giraffe% lp-jira-sync --help


Configuration
-------------

This tool uses `oslo.config` for cli options.
See `lp-jira-sync --help` output for the list of options.


Sub commands
------------

create-jira-issues
~~~~~~~~~~~~~~~~~~

Scan Launchpad bug tasks and create the corresponding issues on JIRA
unless already exist.
