#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import librato
import github3


# Grab config from the environment.
# =================================

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
LIBRATO_EMAIL = os.environ['LIBRATO_EMAIL']
LIBRATO_TOKEN = os.environ['LIBRATO_TOKEN']


# Collect data from GitHub.
# =========================

gh = github3.login(token=GITHUB_TOKEN)
repo = gh.repository('gittip', 'www.gittip.com')
focus = repo.milestone(1)

open_pull_requests = len(list(repo.iter_pulls(state='open')))
open_issues = focus.open_issues

closed_issues = focus.closed_issues
total_issues = open_issues + closed_issues
completion = int(round((closed_issues / total_issues)*100))


# Post it to Librato.
# ===================

lb = librato.connect(LIBRATO_EMAIL, LIBRATO_TOKEN)

q = lb.new_queue()
q.add('focus.pull_requests.open', open_pull_requests)
q.add('focus.issues.open', open_issues)
q.add('focus.issues.closed', closed_issues)
q.add('focus.issues', total_issues)
q.add('focus.completion', completion)
q.submit()


# Emit a local message.
# =====================

msg = "{} / {} ({}%)".format( closed_issues
                            , total_issues
                            , completion
                             )
print(msg)
