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
# This module implements a class to merge translations contained in Gettext
# PO files into different types of files. Right now only merging into HTML
# has been implemented.

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

PO_FOLDER = translate_htmlconfig.PO_FOLDER
POTFILES = translate_htmlconfig.POTFILES


class StringMerger(object):
    """This class implements an object to load translations from Gettext
    PO files and merge them into different types of files.

    """
    def __init__(self, test_mode):
        self.translations = self._load_translations()
        self.files = self._load_files()
        self.test_mode = test_mode

    def _load_files(self):
        """Gets the list of files to merge translations for"""
        with open(translate_htmlconfig.get_source_file(PO_FOLDER,
                                                       POTFILES)) as fp:
            file_list = []
            for line in fp.readlines():
                if not line.startswith('#'):
                    line = os.path.join(
                        translate_htmlconfig.get_sources_path(), line)
                    file_list.append(line.strip())
            return file_list

    def _load_translations(self):
        """Loads the PO files to read translations from"""
        po_dir = os.path.join(translate_htmlconfig.get_sources_path(),
                              PO_FOLDER)
        translations = []
        for po_file in os.listdir(po_dir):
            fname, fext = os.path.splitext(po_file)
            if fext == '.po':
                translations.append(fname)
        return translations

    def merge(self):
        """Merge translations into the final translated files"""
        for translation in self.translations:
            for file_to_merge in self.files:
                merger = getMerger(self.test_mode, translation, file_to_merge)
                merger.merge()


class StringMergerHtml(object):
    """HTML string merger. Reads the given translations from PO files and
    merges them into an HTML file

    """
    def __init__(self, test_mode, langcode, htmlfile):
        self.langcode = langcode
        self.ietf_langcode = langcode_glib_to_ietf(langcode)
        self.pofile = os.path.join(translate_htmlconfig.get_sources_path(),
                              PO_FOLDER, self.langcode + '.po')
        self.htmlfile = htmlfile
        self.test_mode = test_mode

    def merge(self):
        """Does the actual merge operation and writes translated files to
        disk"""
        htmlfile_rel = self.htmlfile.replace(
                            translate_htmlconfig.get_sources_path(), '..')
        with codecs.open(self.htmlfile, 'r', 'utf-8') as f:
            html_file = f.read()

            fname = os.path.basename(self.htmlfile)
            dirname = os.path.join(translate_htmlconfig.get_sources_path(),
                                                   self.ietf_langcode)
            if not os.path.exists(dirname):
                os.makedirs(dirname)

            html_file_translated = os.path.join(dirname, fname)
            print >> sys.stderr, 'Translation written at:', \
                                 html_file_translated
            with codecs.open(html_file_translated,
                             'w+', 'utf-8') as fd:
                po = polib.pofile(self.pofile)

                html_file_translated = html_file

                if self.test_mode:
                    entry_list = po
                else:
                    entry_list = po.translated_entries()

                for entry in entry_list:
                    #FIXME: is this check too strict? (We're limiting merging
                    # translations only if the original file listed in the
                    # PO files source file comments exists)
                    if (htmlfile_rel, '') in entry.occurrences:
                        # Note that we preserve the leading and trailing space
                        # to cater for words or sentences that have been split
                        # and are part of a larger sentence.
                        regex = re.compile(r'>(\s*)' +
                                           re.escape(entry.msgid) + r'(\s*)<')
                        msgstr = self._mangle_po_entry(entry)
                        replacement = r'>\g<1>' + msgstr + '\g<2><'

                        html_file_translated = re.sub(regex, replacement,
                                                      html_file_translated)

                html_file_translated = self.add_html_language(
                                                        self.ietf_langcode,
                                                        html_file_translated)
                fd.write(html_file_translated)

    def _mangle_po_entry(self, po_entry):
        """If the test mode is set, inverts the original English text in the
        msgid. We do this to spot untranslatable strings."""
        if self.test_mode and self._is_po_entry_untranslated(po_entry):
                po_entry = po_entry.msgid[::-1]
        else:
            po_entry = po_entry.msgstr

        return po_entry

    def _is_po_entry_untranslated(self, po_entry):
        #FIXME: polib has a bug whereby the fuzzy flag is not set when reading
        # a PO file
        is_untranslated = False
        if not po_entry.translated() and not po_entry.obsolete and \
            not 'fuzzy' in po_entry.flags:
            is_untranslated = True
        return is_untranslated

    def add_html_language(self, ietf_langcode, html_str):
        """Adds the 'lang' and 'dir' attributes to the final translated file's
        <html> tag"""
        rtl_langs = ['he', 'ps', 'ar', 'ur']
        lang_dir = 'ltr'

        if ietf_langcode.split('-')[0] in rtl_langs:
            lang_dir = 'rtl'

        regex = re.compile('(<html)(.*?)(>)')
        repl = r'\1 lang="{0}" dir="{1}"\3'.format(ietf_langcode, lang_dir)

        html_str = re.sub(regex, repl, html_str)

        return html_str


class StringMergerJs(object):
    """JavaScript string merger. Currently not implemented.

    """
    def __init__(self):
        pass

    def merge(self):
        pass


class StringMergerNone(object):
    """Dummy string merger

    """
    def __init__(self):
        pass

    def merge(self):
        pass


def getMerger(test_mode, pofile, path):
    """Factory-like function to guess the type of file to merge translations
    into by its MIME type, and return the appropriate merger class to
    handle it.

    """
    # Guess the type of the given file
    filetype, encoding = mimetypes.guess_type(path)

    # Return the appropriate merger class to handle the type
    if (filetype, encoding) == HTML_FILE:
        return StringMergerHtml(test_mode, pofile, path)
    elif (filetype, encoding) == JS_FILE:
        return StringMergerJs(test_mode, pofile, path)
    else:
        return StringMergerNone(test_mode, pofile, path)


def langcode_glib_to_ietf(glib_langcode):
    return re.sub('[_@]', '-', glib_langcode)
