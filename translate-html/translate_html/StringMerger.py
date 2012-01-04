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

import mimetypes
import codecs
import sys
import os
from translate_html import translate_htmlconfig
import re

try:
    import polib
except ImportError:
    sys.stderr.write('You need the Python Polib library to run this ' +
                     'script.\nYou can install it by running:\n\t' +
                     '$ sudo apt-get install python-polib')

# MIME type definitions (type, encoding)
HTML_FILE = ('text/html', None)
JS_FILE = ('application/javascript', None)


class StringMerger(object):

    def __init__(self):
        self.translations = self._load_translations()
        self.files = self._load_files()

    def _load_files(self):
        with open(translate_htmlconfig.get_source_file('po',
                                                       'POTFILES.in')) as fp:
            file_list = []
            for line in fp.readlines():
                if not line.startswith('#'):
                    line = os.path.join(
                        translate_htmlconfig.get_sources_path(), line)
                    file_list.append(line.strip())
            return file_list

    def _load_translations(self):
        po_dir = os.path.join(translate_htmlconfig.get_sources_path(), 'po')
        translations = []
        for po_file in os.listdir(po_dir):
            fname, fext = os.path.splitext(po_file)
            if fext == '.po':
                translations.append(fname)
        return translations

    def merge(self):
        for translation in self.translations:
            for file_to_merge in self.files:
                merger = getMerger(translation, file_to_merge)
                merger.merge()


class StringMergerHtml(object):

    def __init__(self, langcode, htmlfile):
        self.langcode = langcode
        self.pofile = os.path.join(translate_htmlconfig.get_sources_path(),
                              'po', langcode + '.po')
        self.htmlfile = htmlfile

    def merge(self):
        htmlfile_rel = self.htmlfile.replace(
                            translate_htmlconfig.get_sources_path(), '..')
        with codecs.open(self.htmlfile, 'r', 'utf-8') as f:
            html_file = f.read()

            fname, fext = os.path.splitext(self.htmlfile)
            html_file_translated = fname + '.' + self.langcode + fext
            print html_file_translated
            with codecs.open(html_file_translated,
                             'w+', 'utf-8') as fd:

                po = polib.pofile(self.pofile)

                html_file_translated = html_file
                for entry in po.translated_entries():
                    if (htmlfile_rel, '') in entry.occurrences:
                        # Note that we preserve the leading and trailing space
                        # to cater for words or sentences that have been split
                        # and are part of a larger sentence. We limit them to
                        # one single space for now.
                        regex = re.compile(r'>( ?)' +
                                           re.escape(entry.msgid) + r'( ?)<')
                        replacement = r'>\g<1>' + entry.msgstr + r'\g<2><'

                        html_file_translated = re.sub(regex, replacement,
                                                      html_file_translated)

                fd.write(html_file_translated)


class StringMergerJs(object):

    def __init__(self):
        pass

    def merge(self):
        pass


class StringMergerNone(object):

    def __init__(self):
        pass

    def merge(self):
        pass


def getMerger(pofile, path):
    """Factory-like function to guess the type of file to merge translations
    into by its MIME type, and return the appropriate merger class to
    handle it.

    """
    # Guess the type of the given file
    filetype, encoding = mimetypes.guess_type(path)

    # Return the appropriate merger class to handle the type
    if (filetype, encoding) == HTML_FILE:
        return StringMergerHtml(pofile, path)
    elif (filetype, encoding) == JS_FILE:
        return StringMergerJs(pofile, path)
    else:
        return StringMergerNone(pofile, path)
