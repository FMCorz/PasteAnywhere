# -*- coding: utf-8 -*-

"""
Paste Anywhere

Plugin for Sublime Text to paste content

Copyright (c) 2013 Frédéric Massart - FMCorz.net

Licensed under The MIT License
Redistributions of files must retain the above copyright notice.

http://github.com/FMCorz/PasteAnywhere
"""


import sublime
import sublime_plugin
import os
import re
import threading
import functools
from PyPasteLib import Paster


class PasteThisCommand(sublime_plugin.TextCommand):

    def run(self, edit, **kwargs):

        view = self.view
        regions = view.sel()
        paster = Paster(self.get_setting('to', kwargs), settings=self.get_setting('settings', kwargs))
        identifiersUsed = []
        hasSomeTxt = False

        for region in regions:

            if region.empty():
                continue

            hasSomeTxt = True

            # Get from the first character to the last of the lines
            region = view.line(region)

            # Set the identifier
            identifier = None
            if self.get_setting('set_identifiers', kwargs):
                identifier = guess_filename(view.file_name(), view.window().folders())
                if identifier:
                    while identifier in identifiersUsed:
                        identifier = increment_identifier(identifier)
                    identifiersUsed.append(identifier)

            # Set the syntax
            syntax = get_syntax(view.settings().get('syntax'))

            txt = view.substr(region)
            paster.add(txt, syntax=syntax, identifier=identifier)

        if hasSomeTxt:
            paster.ttl(self.get_setting('ttl', kwargs))
            paster.private(self.get_setting('private', kwargs))
            paster.description(self.get_setting('description', kwargs))
            paster.poster(self.get_setting('poster', kwargs))
            paster.password(self.get_setting('password', kwargs))

            sendTo = self.get_setting('result_sent_to', kwargs)
            do = PasteIt(paster, sendTo=sendTo)
            do.start()

    def get_setting(self, setting, args):
        settings = sublime.load_settings('PasteAnywhere.sublime-settings')
        return args.get(setting, settings.get(setting))


class InsertInNewFileCommand(sublime_plugin.TextCommand):

    def run(self, edit, string):
        self.view.insert(edit, 0, string)


def get_syntax(path):
    syntaxfile = os.path.basename(path)
    return re.sub(u'\.tmLanguage$', u'', syntaxfile).lower().replace(u' ', u'_')


def guess_filename(filename, folders):
    if not filename:
        return filename

    for folder in folders:
        if filename.startswith(folder):
            filename = re.sub(u'^%s' % folder, u'', filename)
            break
    return filename.lstrip(os.sep)


def increment_identifier(identifier):
    (path, basename) = os.path.split(identifier)
    (base, ext) = os.path.splitext(basename)

    match = re.search(r'__(\d+)$', base)
    if match:
        nb = int(match.group(1))
        base = re.sub(r'__\d+$', u'__' + unicode(nb + 1), base)
    else:
        base += u'__2'

    basename = base + ext

    return os.path.join(path, basename)


def new_file(string):
    v = sublime.active_window().new_file()
    v.run_command('insert_in_new_file', {'string': string})


def output_panel(string):
    w = sublime.active_window()
    v = w.get_output_panel('PasteAnywhere')
    v.run_command('insert_in_new_file', {'string': string})
    w.run_command('show_panel', {'panel': 'output.PasteAnywhere'})


def set_clipboard(string):
    sublime.set_clipboard(string)
    sublime.status_message('Content pasted, check your clipboard.')


def status_message(message):
    sublime.status_message(message)


class PasteIt(threading.Thread):

    _sendTo = None

    def __init__(self, paster, sendTo=None):
        threading.Thread.__init__(self)
        self._sendTo = sendTo
        self._paster = paster

    def run(self):
        sublime.set_timeout(functools.partial(status_message, 'Pasting the content...'), 1)
        try:
            result = self._paster.paste()
            self.do(result)
        except Exception as e:
            import traceback
            traceback.print_exc()
            sublime.set_timeout(functools.partial(status_message, 'Error while pasting.'), 1)

    def do(self, result):
        if self._sendTo == 'outputpanel':
            sublime.set_timeout(functools.partial(output_panel, result), 1)
        elif self._sendTo == 'newfile':
            sublime.set_timeout(functools.partial(new_file, result), 1)
        else:
            sublime.set_timeout(functools.partial(set_clipboard, result), 1)
