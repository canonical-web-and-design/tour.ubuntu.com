import logging
import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('translate-html')

from translate_html import translate_htmlconfig

LEVELS = (logging.ERROR,
          logging.WARNING,
          logging.INFO,
          logging.DEBUG,
          )

import polib
import codecs
#import re
import subprocess
import sys
from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

BOM = u'\ufeff'
# FIXME: hardcoded for now
TEST_FILE = '../index.html'
# FIXME: hardcoded for now
TEST_TRANSLATED_FILE = '../index.ca.html'
# FIXME: hardcoded for now
TEST_POT_FILE = '../po/ubuntu-online-tour.pot'
# FIXME: hardcoded for now
TEST_PO_FILE = '../po/ca.po'


class SubprocessCaller:
    """Starts a process with the given arguments

    Keyword arguments:
    cmd_str -- subprocess command string
    args -- list with additional apt arguments
    check_output -- boolean, determines if the command output needs to be
    returned

    """

    def __init__(self, cmd_str, args, check_output = False):
        self.cmd_str = cmd_str
        self.args = args
        self.check_output = check_output

    def call_with_args(self):
        """
        Return value:
        None if check_output is False
        Byte string with the command output otherwise

        """

        cmd = list(self.cmd_str.split(" "))
        cmd.extend(self.args)
        logging.debug('Command: ' + ' '.join(cmd))

        if self.check_output:
            proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            )
            stdout_value = proc.communicate()[0]
            return stdout_value
        else:
            subprocess.call(cmd)


class HTMLStringExtractor(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.skiptag = False
        self._text = []

    def handle_data(self, data):
        text = data.strip()
        if (len(text) > 0) and not self.skiptag and (text != BOM):
            text = sub('[ \t\r\n]+', ' ', text)
            self._text.append(text)

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

    def text(self):
        return set(self._text)


def extract_messages(text):
    try:
        extractor = HTMLStringExtractor()
        extractor.feed(text)
        extractor.close()
        messages = extractor.text()

        po = polib.POFile()
        po.metadata = {
            'Project-Id-Version': '1.0',
            'Report-Msgid-Bugs-To': 'you@example.com',
            'POT-Creation-Date': '2007-10-18 14:00+0100',
            'PO-Revision-Date': '2007-10-18 14:00+0100',
            'Last-Translator': 'you <you@example.com>',
            'Language-Team': 'English <yourteam@example.com>',
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

        for message in messages:
            entry = polib.POEntry(
                msgid = message,
                msgstr = u'')
            po.append(entry)

        po.save(TEST_POT_FILE)

    except:
        print_exc(file = stderr)
        return text


def main():
    version = translate_htmlconfig.__version__
    # Support for command line options.
    usage = _("translate-html {--extract|--translate} [options]")
    parser = optparse.OptionParser(version="%%prog %s" % version, usage=usage)
    parser.add_option('-d', '--debug', dest='debug_mode', action='store_true',
        help=_('Print the maximum debugging info (implies -vv)'))
    parser.add_option('-v', '--verbose', dest='logging_level', action='count',
        help=_('set error_level output to warning, info, and then debug'))
    # exemple of silly CLI option
    parser.add_option("-x", "--extract", action="store_true",
        dest="extract_mode",
        help=_("Extract the strings from the original HTML file"))
    parser.add_option("-r", "--translate", action="store_true",
        dest="translate_mode",
        help=_("Get the translations from PO files and write them to a new" +
               " translated HTML file"))
    parser.set_defaults(logging_level=0, extract_mode=False,
                        translate_mode = False)
    (options, args) = parser.parse_args()

    # set the verbosity
    if options.debug_mode:
        options.logging_level = 3
    logging.basicConfig(level=LEVELS[options.logging_level],
                        format='%(asctime)s %(levelname)s %(message)s')

    if options.extract_mode:
        with codecs.open(TEST_FILE, 'r', 'utf-8') as f:
            html_file = f.read()

            extract_messages(html_file)

    elif options.translate_mode:

        with codecs.open(TEST_FILE, 'r', 'utf-8') as f:
            html_file = f.read()

            extract_messages(html_file)

            with codecs.open(TEST_TRANSLATED_FILE, 'w+', 'utf-8') as fd:
                fd.write(html_file)

            reload(sys)
            sys.setdefaultencoding("utf-8")

            po = polib.pofile(TEST_PO_FILE)
            for entry in po.translated_entries():
                regex = entry.msgid
                replacement = entry.msgstr
                #html_file = re.sub(regex, replacement, html_file)
                #html_file = html_file.replace(regex, replacement)
                sed_args = ['-i',
                            '-e',
                            's/>[\s]*{0}[\s]*</>{1}</g'.format(regex,
                                                               replacement),
                            TEST_TRANSLATED_FILE]
                sed = SubprocessCaller("sed", sed_args)
                sed.call_with_args()

            #with codecs.open('ca.html', 'w', 'utf-8') as fd:
            #    fd.write(html_file)

    else:
        print "You must specify a mode"
        parser.print_help()

if __name__ == "__main__":
    main()
