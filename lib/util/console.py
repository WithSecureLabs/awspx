

import logging
import os
import re
import sys
import termios
import threading
import tty
from datetime import datetime
from logging import Handler
from pathlib import Path
from rich._log_render import LogRender
from rich.bar import Bar
from rich.console import Console as RichConsole
from rich.progress import Progress
from rich.style import Style
from rich.table import Table, box
from rich.text import Text


logging.addLevelName(25, "NOTICE")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


class Log(Handler):

    levels = {
        "CRITICAL": Style(color="red", bold=True, reverse=True),
        "ERROR":  Style(color="red", bold=True),
        "WARNING":  Style(color="dark_red"),
        "NOTICE":  Style(color="yellow"),
        "INFO":  Style(dim=True),
        "DEBUG":  Style(color="green", dim=True),
    }

    def __init__(
        self,
        level=logging.DEBUG,
        console=RichConsole(),
    ):

        super().__init__(level=level)

        self.console = console
        self._render = LogRender(show_level=True)

    def _styllize(self, record):

        from lib.util.keywords import (Keywords, Regex)

        message = Text(self.format(record))
        message.highlight_regex(Regex.arn, 'dim')
        message.highlight_regex(Regex.resource, 'i')
        message.highlight_regex(Regex.integer, 'bold i')
        message.highlight_words(Keywords.resource, 'i')
        message.highlight_words(Keywords.action, 'i')
        message.highlight_words(Keywords.edge, 'i')
        message.highlight_words(Keywords.node, 'i')
        message.highlight_words(Keywords.attack, 'i')

        return message

    def emit(self, record):

        level = record.levelname.upper()
        style = self.levels[level] if level in self.levels else None

        self.console.print(
            self._render(
                self.console,
                [self._styllize(record)],
                log_time=datetime.fromtimestamp(record.created),
                time_format="[%d/%m/%y %H:%M:%S]",
                level=Text(level, style=style)
            )
        )


class Operation(Progress):

    table = None

    def __init__(self, table):
        super().__init__()
        self.table = table

    def get_renderables(self):

        with self._lock:
            yield self.table


class Console(Table):

    _verbose = False
    console = RichConsole()
    logger = logger
    level = logging.DEBUG

    def __init__(self, name=None, log=False):

        super().__init__(
            box=None if name is None else box.SQUARE,
            show_header=name is not None,
            expand=True)

        if name is None:
            self.add_row(" ")
            self.thread = Operation(self)

    def debug(self, message, silent=False):
        self.logger.debug(message)
        if not silent:
            self._annotate(message, style="dim")

    def info(self, message):
        self.logger.info(message)
        if not self._verbose:
            self._annotate(message, "dim")

    def notice(self, message, silent=False):
        if self.logger.isEnabledFor(25):
            self.logger._log(25, message, args=None)

        if not silent:
            self._annotate(message, style="dim")

    def warn(self, message):
        self.logger.warn(message)
        if not self._verbose:
            self._annotate(message, "dark_red")

    def error(self, message):
        self.logger.error(message)
        if not self._verbose:
            self._annotate(message, "bold red")

    def critical(self, message):

        if isinstance(message, str):
            self.logger.critical(message)
            if not self._verbose:
                self._annotate(message, "bold red")
        else:
            self.stop()
            try:
                self.console.print_exception()
            except ValueError:
                self.console.print(message.__repr__())

        os._exit(1)

    def item(self, message):

        self.notice(message, silent=True)

        if self._verbose:
            return self

        service = self.__class__(name=message)
        service.add_column(message, justify="center")
        service.thread = self.thread

        self.add_row(service)
        self.spacer()

        return service

    def spacer(self):
        self.add_row()

    def task(self, message, function=None, args=[], done=None):

        self.notice(message, silent=True)

        (text, progress, busy) = self._add(message)

        results = function(*args)

        if done.__class__.__name__ == 'function':
            done = done(results)

        if done is not None:
            text._text = [done]
            self.notice(done, silent=True)

        busy._text = [""]
        progress.pulse = False
        progress.update(completed=progress.total)

        self._annotate()

        return results

    def tasklist(self, message, iterables=[], wait=None, done=None):

        if '__len__' in dir(iterables) and not len(iterables) > 0:
            return

        self.notice(message, silent=True)

        (text, progress, busy) = self._add(message, iterables=iterables)

        if wait is not None:
            self.debug(wait)
        else:
            self._annotate()

        for completed, iterable in enumerate(iterables, 1):

            if wait is not None:
                self._annotate()

            yield iterable

            if wait is not None:
                self.debug(wait)

            progress.update(completed=completed)

        if done is not None:
            self.notice(done, silent=True)
            text._text = [done]

        busy._text = [""]
        progress.pulse = False
        progress.update(completed=progress.total)

        self._annotate()

    def list(self, dictionaries=[]):

        if not isinstance(dictionaries, list):
            dictionaries = [dictionaries]

        if not len(dictionaries) > 0:
            return

        t = Table.grid(expand=True)

        for k in dictionaries[0].keys():
            t.add_column(str(k))

        for d in dictionaries:
            t.add_row(*d.values())

        if self._verbose:
            self.console.print(t)
        else:
            self.add_row(t)

    def input(self, message):

        def readchar():

            fd = sys.stdin.fileno()
            settings = termios.tcgetattr(fd)

            try:
                tty.setraw(sys.stdin.fileno())
                char = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, settings)

            if char == '\x03':
                raise KeyboardInterrupt

            elif char == '\x04':
                raise EOFError

            return char

        def read(main, message, value):

            (text, value, _) = self._add(message, override=value)
            text.style = "b"
            value.style = "i"

            try:
                self.refresh()
                char = None

                while True:

                    with console.thread._lock:
                        char = readchar()
                        # Enter
                        if ord(char) == 13:
                            break
                        # Delete
                        elif ord(char) in [27]:
                            continue
                        # Backspace
                        elif ord(char) == 127:
                            value._text = [''.join(value._text)[:-1]]

                        else:
                            value._text = [''.join([*value._text, char])]

                        self.refresh()

            except (KeyboardInterrupt, EOFError) as e:
                value.style = None
                self.stop()
                os._exit(0)

        if not self._verbose:
            value = Text("")

            input_thread = threading.Thread(target=read,
                                            args=(self, message, value))
            input_thread.start()
            input_thread.join()

            return ''.join(value._text)
        else:
            sys.stdout.write(message)
            sys.stdout.flush()
            return input()

    def verbose(self):

        if self._verbose:
            return

        log = Log(console=self.console, level=self.level)

        self.stop()
        self.logger.addHandler(log)
        self._verbose = True

    def _add(self, message, iterables=[], override=None):

        key = Text(message, overflow='ellipsis', no_wrap=True)
        busy = Text()

        if override is None:

            total = 1
            pulse = True

            try:
                total = len(iterables) if iterables != [] else 1
                pulse = iterables == []

            # Not all iterables have a length
            except TypeError:
                pass

            busy._text = ["→"]
            color = Style(color="rgb(161, 209, 255)", dim=True)
            value = Bar(total=total, pulse=pulse,
                        complete_style=color,
                        finished_style=color,
                        pulse_style=color)
        else:
            value = override

        operation = Table(box=None, show_header=False,
                          show_footer=False, show_edge=True,
                          padding=(0, 0 if self.show_header else 1))

        operation.add_column(width=3 if self.show_header else 2,
                             justify="center")
        operation.add_column(width=62 if self.show_header else 60)
        operation.add_column()
        operation.add_row(busy, key, value)

        self.add_row(operation)
        return (key, value, busy)

    def _annotate(self, message="", style=None):

        if self._verbose:
            return

        self.caption = message
        self.caption_style = style
        self.refresh()

    def start(self):
        if not console.thread._started:
            self.thread.start()

    def refresh(self):
        if self.thread is not None and self.thread._started:
            self.thread.refresh()

    def stop(self):
        if console.thread._started:
            self.thread.stop()
            self.console.print()


console = Console()
