#!/usr/bin/env python

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

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Copyright 2015 Thierry Carrez <thierry@openstack.org>
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# This file is based on 
#   openstack/gerrit-dash-creator
#   c6e15c63b03a3634b9c1e0d397f28a0423ba0e4e
#   gerrit_dash_creator/cmd/bugs.py
# and
#   openstack/project-config
#   9f5d7cfea4ca3adc40adf6ac4d33f36e658ea399
#   jenkins/scripts/release-tools/launchpad_add_comment.py

import os

from launchpadlib import launchpad

from oslo_config import cfg


CONF = cfg.CONF


lp_opts = [
    cfg.StrOpt('credentials-file',
        default=os.environ.get('LP_CREDS_FILE'),
        help=('plain-text credentials file, '
              'defaults to value of $LP_CREDS_FILE')),
    cfg.StrOpt('project-name',
        default='openstack',
        help=('Project (group) to scan')),
    cfg.StrOpt('marker-tag',
        default='midokura-jira-tracked',
        help=('Tag to mark bug to sync')),
]

CONF.register_cli_opts(lp_opts, group='lp')


CACHE_DIR = os.path.expanduser('~/.cache/launchpadlib/')
SERVICE_ROOT = 'production'


def open_lp():
    if CONF.dry_run:
        return launchpad.Launchpad.login_anonymously(
            consumer_name='lp-jira-sync',
            service_root=SERVICE_ROOT,
            launchpadlib_dir=CACHE_DIR)
    else:
        return launchpad.Launchpad.login_with(
            application_name='lp-jira-sync',
            service_root=SERVICE_ROOT,
            launchpadlib_dir=CACHE_DIR,
            credentials_file=CONF.lp.credentials_file)


def scan(lp, status=None, callback=None):
    marker_tag = CONF.lp.marker_tag
    project_name = CONF.lp.project_name
    project = lp.projects[project_name]
    kwargs = dict(
        tags=['%s' % (marker_tag,)],
    )
    if status is not None:
        kwargs['status'] = status
    bugtasks = project.searchTasks(**kwargs)

    for bugtask in bugtasks:
        bug = bugtask.bug
#        print bugtask.web_link, bugtask.bug_link 
        bug_id = bug.id
#        print bug.web_link, bug.title
        if callback is not None:
            callback(bug)
