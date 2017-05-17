# Copyright (C) 2017 Midokura SARL.
# All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import argparse

from oslo_config import cfg

from lp_jira_sync import lp
from lp_jira_sync import ji


CONF = cfg.CONF
CONF.register_cli_opts([
    cfg.BoolOpt('debug'),
    cfg.BoolOpt('dry-run'),
    cfg.StrOpt('command',
        default='create-jira-issues',
        choices=['create-jira-issues'],
        positional=True)
])


def create_jira_issues():
    # Scan LP bugs with the marker tag and
    # create the corresponding JIRA issues if not exist

    lpad = lp.open_lp()
    lp_bugs = {}
    def f(bug):
        lp_bugs[bug.web_link] = bug
    lp.scan(lpad, status=['New', 'In Progress', 'Confirmed'], callback=f)

    j = ji.open_jira()
    def check_lp(issue):
        lp_url = ji.get_lp_link(j, issue)
        if lp_url in lp_bugs:
            print "%s already has JIRA issue %s" % (lp_url, issue.key)
            lp_bugs.pop(lp_url)
    ji.scan(j, callback=check_lp)

    # print "LP Bugs not in JIRA: "
    # for web_link, bug in lp_bugs.iteritems():
    #     print "\t", web_link, bug.title

    for web_link, bug in lp_bugs.iteritems():
        ji.create_issue_for_lp_bug(j, bug)
    return 0


def main():
    CONF()

    if CONF.debug:
        import httplib2
        httplib2.debuglevel = 1

    globals()[CONF.command.replace('-', '_')]()
