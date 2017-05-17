lp-jira-sync
============

Launchpad JIRA sync tool

Overview
--------

For some reasons, I have to use both of
`Launchpad` [#launchpad_networking_midonet]_ and
Midokura-private JIRA [#midokura_jira]_ to manage
`networking-midonet` [#networking_midonet]_
related issues.
The purpose of this tool is to automate some of
the cumbersome processes in the environment.


.. [#launchpad_networking_midonet] https://bugs.launchpad.net/networking-midonet/
.. [#midokura_jira] https://midobugs.atlassian.net
.. [#networking_midonet] https://docs.openstack.org/developer/networking-midonet/


Installation
------------

::

    giraffe% virtualenv venv
    giraffe% . ./venv/bin/activate
    (venv) giraffe% pip install .
    (venv) giraffe% rehash
    (venv) giraffe% lp-jira-sync --help


Configuration
-------------

This tool uses `oslo.config` [#oslo_config]_ for cli options.
See `lp-jira-sync --help` output for the list of options.
For secret values like credentials, I recommend to
store them in a configuration file and specify it by `--config-file`
option, rather than specifying them on the command line directly.

.. [#oslo_config] https://docs.openstack.org/developer/oslo.config/


Sub commands
------------

create-jira-issues
~~~~~~~~~~~~~~~~~~

Scan Launchpad bug tasks and create the corresponding issues on JIRA
unless already exist.
