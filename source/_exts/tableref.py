#!/usr/bin/env python3
# encoding: utf-8
#
# Copyright (c) 2014 Doug Hellmann.  All rights reserved.
#
#
#                         All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software
# and its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Doug Hellmann not be used in advertising or publicity
# pertaining to distribution of the software without specific,
# written prior permission.
#
# DOUG HELLMANN DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS, IN NO EVENT SHALL DOUG HELLMANN BE LIABLE FOR ANY
# SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.
#
"""Extension to allow references to tables.

Use the ``:table:`` role in-line, specifying the title of the
table as set in the ``.. table`` directive.

For example::

    The CPython interpreter accepts several command line options
    to control its behavior, listed in :table:`CPython Command
    Line Option Flags`.

    .. table:: CPython Command Line Option Flags

        ========    =======
        Option      Meaning
        ========    =======
        -B          do not write .py[co] files on import
        -d          debug output from parser
        -E          ignore PYTHON* environment variables
        -i          inspect interactively after running script
        -O          optimize generated bytecode slightly
        -OO         remove doc-strings
        -s          do not add user site directory to sys.path
        -S          do not run 'import site' on initialization
        -t          issue warnings about inconsistent tab usage
        -tt         issue errors for inconsistent tab usage
        -v          verbose
        -3          warn about Python 3.x incompatibilities
        ========    =======

"""

import functools

from docutils import nodes, utils


class tableref(nodes.reference):
    pass


def _role(typ, rawtext, text, lineno, inliner,
          options={}, content=[], nodeclass=None):
    text = utils.unescape(text)
    pnode = nodeclass(
        rawsource=text,
        text='',
        internal=True,
        refuri=text,
    )
    return [pnode], []


def latex_visit_tableref(self, node):
    self.body.append(r'Table ~\ref{table:%s}' % node['refuri'])
    raise nodes.SkipNode


def latex_depart_tableref(self, node):
    return


def html_visit_tableref(self, node):
    self.body.append('the table below')
    raise nodes.SkipNode


def html_depart_tableref(self, node):
    return


def builder_inited(app):
    app.info('defining table role')
    app.add_role(
        'table',
        functools.partial(_role, nodeclass=tableref)
    )


def setup(app):
    app.info('initializing tableref')
    app.add_node(
        tableref,
        latex=(latex_visit_tableref, None),
        html=(html_visit_tableref, html_depart_tableref),
    )
    app.connect('builder-inited', builder_inited)
