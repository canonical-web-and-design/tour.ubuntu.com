#! /usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 David Planella <david.planella@ubuntu.com>
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import logging
import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('translate-html')

from translate_html import StringExtractor, StringMerger, translate_htmlconfig

LEVELS = (logging.ERROR,
          logging.WARNING,
          logging.INFO,
          logging.DEBUG,
          )

import sys


def main():
    version = translate_htmlconfig.__version__

    # Support for command line options.
    usage = _("translate-html {--extract|--translate} [options]")
    parser = optparse.OptionParser(version="%%prog %s" % version, usage=usage)
    parser.add_option('-d', '--debug', dest='debug_mode', action='store_true',
        help=_('Print the maximum debugging info (implies -vv)'))
    parser.add_option('-v', '--verbose', dest='logging_level', action='count',
        help=_('set error_level output to warning, info, and then debug'))

    parser.add_option("-x", "--extract", action="store_true",
        dest="extract_mode",
        help=_("Extract mode: extract the strings from the original " +
               "HTML file"))
    parser.add_option("-r", "--translate", action="store_true",
        dest="translate_mode",
        help=_("Translate mode: get the translations from PO files and " +
               "write them to a new translated HTML file"))
    parser.set_defaults(logging_level=0, extract_mode=False,
                        translate_mode = False)
    (options, args) = parser.parse_args()

    # Set the verbosity
    if options.debug_mode:
        options.logging_level = 3
    logging.basicConfig(level=LEVELS[options.logging_level],
                        format='%(asctime)s %(levelname)s %(message)s')

    if options.extract_mode:
        string_extractor = StringExtractor.StringExtractor()
        string_extractor.extract()

    elif options.translate_mode:
        string_merger = StringMerger.StringMerger()
        string_merger.merge()

    else:
        sys.stderr.write("You must specify a mode\n")
        parser.print_help()

if __name__ == "__main__":
    main()
