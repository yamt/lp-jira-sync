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

import re

import jira

from oslo_config import cfg

jira_opts = [
    cfg.URIOpt('url', help='JIRA url'),
    cfg.StrOpt('user', help='JIRA user'),
    cfg.StrOpt('password', help='JIRA password', secret=True),
    cfg.StrOpt('marker-label',
        default='launchpad-tracked',
        help=('Label to mark issues')),
    cfg.ListOpt('create-labels',
        default=['launchpad-tracked'],
        help=('Labels to use when creating new issues')),
    cfg.StrOpt('default-assignee',
        help='The asignee for newly created JIRA issues'),
    cfg.StrOpt('project',
        default='MI',
        help=('Project Key')),
]

CONF = cfg.CONF
CONF.register_cli_opts(jira_opts, group='jira')


# KNOWN_STATUS = {
#     'To Do',
#     'In Progress',
#     'Blocked',
#     'Resolved',
#     'Closed',
# }

LINK_TITLE_LAUNCHPAD = 'Launchpad'


# XXX should be config
# re_lp_url = re.compile('https://bugs\.launchpad\.net/.*/\+bug/([0-9]+)')


def open_jira():
    # XXX is there a convenient way to drop write permission for dry-run?
    jira_auth = (CONF.jira.user, CONF.jira.password)
    return jira.JIRA(CONF.jira.url, basic_auth=jira_auth)


def add_lp_link(j, i, url):
    if CONF.dry_run:
        print "Would create LP link %s -> %s" % (i.key, url)
        return
    # XXX should use globalId?
    j.add_simple_link(i, {
        'url': url,
        'title': LINK_TITLE_LAUNCHPAD,
        'icon': {
            'url16x16': 'https://bugs.launchpad.net/favicon.ico',
        }
    })


def get_lp_link(j, i):
    for link in j.remote_links(i):
        if link.object.title == LINK_TITLE_LAUNCHPAD:
            return link.object.url
    print "Failed to get LP link for %s" % i.key


def scan(j, callback=None):
    # NOTE(yamamoto): We don't use maxResults=False as it seems broken
    # in case the server didn't return isLast.
    startAt = 0
    while True:
        issues = j.search_issues('labels = %(label)s' % {
            'label': CONF.jira.marker_label,
        }, startAt=startAt)
        if len(issues) == 0:
            break
        startAt += len(issues)
        for issue in issues:
            # print issue.key, issue.fields.summary
            if callback is not None:
                callback(issue)


def create_issue_for_lp_bug(j, bug):
    web_link = bug.web_link
    if CONF.dry_run:
        print "Would create JIRA issue for %s" % web_link
        return
    fields = {
        'project': {
            'key': CONF.jira.project,
        },
        'summary': bug.title,
        'issuetype': {
            'name': 'Task',
        },
        'labels': CONF.jira.create_labels,
    }
    assignee = CONF.jira.default_assignee
    if assignee is not None:
        fields['assignee'] = {
            'name': assignee,
        }
    i = j.create_issue(fields=fields)
    add_lp_link(j, i, web_link)
    print "JIRA issue %s was created for %s" % (i.key, web_link)
