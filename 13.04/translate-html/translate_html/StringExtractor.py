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
#
# This module implements a class to extract translatable messages from
# different types of files and put them into a Gettext POT file ready to give
# to translators to do their work. At this point only extracting messages
# from HTML files has been implemented.

import codecs
import mimetypes
import os
from HTMLParser import HTMLParser
from traceback import print_exc
from sys import stderr
from translate_html import translate_htmlconfig
from re import sub
import sys
from datetime import datetime

try:
    import polib
except ImportError:
    sys.stderr.write('You need the Python Polib library to run this ' +
                     'script.\nYou can install it by running:\n\t' +
                     '$ sudo apt-get install python-polib')

# MIME type definitions (type, encoding)
HTML_FILE = ('text/html', None)
JS_FILE = ('application/javascript', None)

BOM = u'\ufeff'
PO_FOLDER = translate_htmlconfig.PO_FOLDER
GETTEXT_DOMAIN = translate_htmlconfig.GETTEXT_DOMAIN
POTFILES = translate_htmlconfig.POTFILES


class HTMLStringParser(HTMLParser):
    """This class does the actual extraction from messages from HTML files.
    HTML entities are generally not supported, the only exception being
    &amp;.

    return a Python set containing the extracted text

    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.skiptag = False
        self.entityseen = False
        self._text = []

    def handle_data(self, data):
        text = data.strip()
        if (len(text) > 0) and not self.skiptag and (text != BOM):
            text = sub('[ \t\r\n]+', ' ', text)
            if not self.entityseen:
                self._text.append(text)
            else:
                entity = self._text.pop()
                self._text[-1] += ' ' + entity + ' ' + text
                self.entityseen = False

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            self.skiptag = True
        elif tag == 'noscript':
            self.skiptag = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.skiptag = False
        elif tag == 'noscript':
            self.skiptag = False

    def handle_entityref(self, name):
        # We only support &amp; for now
        if name == 'amp':
            self.handle_data('&' + name + ';')
            self.entityseen = True

    def text(self):
        return set(self._text)


class StringExtractor(object):
    """This class reads the list of files to extract strings from from the
    POTFILES.in file, performs the extraction and saves the POT file to disk.

    """
    def __init__(self):
        self.files = self._load_files()
        self.potfile = polib.POFile()
        time_str = datetime.now().isoformat(' ')
        self.potfile.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'you@example.com',
            'POT-Creation-Date': time_str,
            'PO-Revision-Date': time_str,
            'Last-Translator': 'you <you@example.com>',
            'Language-Team': 'English <yourteam@example.com>',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

    def _load_files(self):
        """Loads the files to extract strings from. They are expected to
        be listed in the POFILES.in file"""
        with open(translate_htmlconfig.get_source_file(PO_FOLDER,
                                                       POTFILES)) as fp:
            file_list = []
            for line in fp.readlines():
                if not line.startswith('#'):
                    line = os.path.join(
                        translate_htmlconfig.get_sources_path(), line)
                    file_list.append(line.strip())
            return file_list

    def _save_potfile(self):
        """Writes the resulting POT file to disk"""
        self.potfile.save(os.path.join(
                            translate_htmlconfig.get_sources_path(),
                            PO_FOLDER,
                            GETTEXT_DOMAIN + '.pot'))

    def extract(self):
        """Extracts the messages from the given file by choosing the
        appropriate extractor type, and saves the POT file to disk"""
        for file_to_extract in self.files:
            extractor = getExtractor(self.potfile, file_to_extract)
            extractor.extract()
        self._save_potfile()


class StringExtractorJs(object):
    """This class implements the extractor from messages in JavaScript files
    It is currently not supported.

    """
    def __init__(self, potfile, jsfile):
        self.jsfile = jsfile
        self.potfile = potfile

    def extract(self):

        jsfile_rel = self.jsfile.replace(
                            translate_htmlconfig.get_sources_path(), '..')
        with codecs.open(self.jsfile, 'r', 'utf-8') as fp:
            linecount = 0
            for line in fp.readlines():
                linecount += 1
                if line.startswith('var'):
                    var, message = line.split('=', 1)
                    var = var.split()[1]
                    message = message.strip()
                    message = message[1:-2]

                    entry = polib.POEntry(
                                comment=var,
                                occurrences=[(jsfile_rel, linecount)],
                                msgid=message,
                                msgstr=u'')
                    self.potfile.append(entry)


class StringExtractorHtml(object):
    """This class implements the extractor from messages in HTML files.
    It reads the given HTML file and puts the extracted messages in a
    potfile structure

    """
    def __init__(self, potfile, htmlfile):
        self.htmlfile = htmlfile
        self.potfile = potfile

    def extract(self):
        htmlfile_rel = self.htmlfile.replace(
                            translate_htmlconfig.get_sources_path(), '..')
        try:
            with codecs.open(self.htmlfile, 'r', 'utf-8') as fp:
                html_file = fp.read()
                extractor = HTMLStringParser()
                extractor.feed(html_file)
                extractor.close()
                messages = extractor.text()

                for message in messages:
                    entry = polib.POEntry(
                        occurrences=[(htmlfile_rel, 0)],
                        msgid=message,
                        msgstr=u'')
                    self.potfile.append(entry)
        except:
            print_exc(file=stderr)


class StringExtractorNone(object):
    """Dummy message extractor

    """
    def __init__(self, potfile, path):
        pass

    def extract(self):
        pass


def getExtractor(potfile, path):
    """Factory-like function to guess the type of file to extract translations
    from by its MIME type, and return the appropriate extractor class to
    handle it.

    """
    # Guess the type of the given file
    filetype, encoding = mimetypes.guess_type(path)

    # Return the appropriate extractor class to handle the type
    if (filetype, encoding) == HTML_FILE:
        return StringExtractorHtml(potfile, path)
    elif (filetype, encoding) == JS_FILE:
        return StringExtractorJs(potfile, path)
    else:
        return StringExtractorNone(potfile, path)
