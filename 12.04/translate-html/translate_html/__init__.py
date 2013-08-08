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
    usage = _('''translate-html {--extract|--translate} [options]

    This script can be used to prepare translatable messages in HTML files
    and expose them to translators and to subsequently use those translations
    to build localized HTML files based on the original in English.

    It works in one of two modes:

    - Extract mode: extracts translatable strings from the file specified
      in the 'po/POTFILES.in' file and puts them into a .pot file into the
      'po' folder, ready to give it to translators.
    - Translate mode: fetches the translations in the form of .po files in the
      'po-html' folder and builds localized files based on the original.
      Untranslated strings in the PO files are left as their English originals
      in the generated localized files. The localized files are named
        <ISO-639-2-lang-code>/<original-filename>.<original-fileext>
      E.g.
        en/index.html      <- original file
        zh-CN/index.html   <- Simplified Chinese translation

    Structure of the 'po-html' folder:

      po-html/template.pot <- translation template created in extract mode
      po-html/POTFILES.in  <- files to extract strings from are specified here
      po-html/zh_CN.po     <- translation done by translators
      po-html/ca.po        <- another translation, naming: <ISO 639-2 code>.po

    ''')
    parser = optparse.OptionParser(version="%%prog %s" % version, usage=usage)
    parser.add_option('-d', '--debug', dest='debug_mode', action='store_true',
        help=_('Print the maximum debugging info (implies -vv)'))
    parser.add_option('-v', '--verbose', dest='logging_level', action='count',
        help=_('set error_level output to warning, info, and then debug'))

    parser.add_option("-x", "--extract", action="store_true",
        dest="extract_mode",
        help=_("Extract mode: extract the strings from the original " +
               "HTML file"))
    parser.add_option("-t", "--translate", action="store_true",
        dest="translate_mode",
        help=_("Translate mode: get the translations from PO files and " +
               "write them to a new translated HTML file"))
    parser.add_option("-s", "--test", action="store_true",
        dest="test_mode",
        help=_("Test mode: only effective in conjunction with Translate " +
               "mode. If set, untranslatable messages are translated as " +
               "reversed English, so that they are easy to spot."))
    parser.set_defaults(logging_level=0, extract_mode=False,
                        translate_mode=False, test_mode=False)
    (options, args) = parser.parse_args()

    # Set the verbosity
    if options.debug_mode:
        options.logging_level = 3
    logging.basicConfig(level=LEVELS[options.logging_level],
                        format='%(asctime)s %(levelname)s %(message)s')

    if options.extract_mode:
        if options.test_mode:
            sys.stderr.write("WARNING: You've specified the test mode flag." +
                             "Test mode is only valid when specified along" +
                             "with the translate mode flag, and will thus" +
                             "be ignored")
        string_extractor = StringExtractor.StringExtractor()
        string_extractor.extract()

    elif options.translate_mode:
        string_merger = StringMerger.StringMerger(options.test_mode)
        string_merger.merge()

    else:
        sys.stderr.write("ERROR: You must specify a mode\n\n")
        parser.print_help()

if __name__ == "__main__":
    main()
