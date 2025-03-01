#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getpass
import re
import subprocess
import sys
import time
from typing import Callable

from sun.__metadata__ import __version__
from sun.configs import Configs
from sun.utils import Fetch, Utilities


class Tools(Configs):

    """SUN Utilities.

    Attributes:
        fetch (TYPE): Fetch the packages.
        utils (TYPE): Utilities.
    """

    def __init__(self) -> None:
        super().__init__()
        self.utils = Utilities()
        self.fetch = Fetch()

    @staticmethod
    def su() -> None:
        """Root privileges not required.

        Raises:
            SystemExit: Exit.
        """
        if getpass.getuser() == 'root':
            raise SystemExit('sun: Error: It should not be run as root')

    @staticmethod
    def usage() -> None:
        """Usage help menu.
        """
        args: str = (f'SUN (Slackware Update Notifier) - Version: {__version__}\n'
                     '\nUsage: sun [OPTIONS]\n'
                     '\nOptional arguments:\n'
                     '  help       Display this help and exit.\n'
                     '  start      Start sun daemon.\n'
                     '  stop       Stop sun daemon.\n'
                     '  restart    Restart sun daemon.\n'
                     '  check      Check for software updates.\n'
                     '  status     Sun daemon status.\n'
                     '  info       Os and machine information.\n'
                     '\nStart tray app from the terminal: sun start --tray')
        print(args)

    def check_updates(self) -> tuple:
        """Returns the count of the packages and the message.

        Returns:
            tuple: The notify message and the package names.
        """
        message: str = 'No news is good news!'
        packages: list[str] = list(self.fetch.updates())
        count_packages: int = len(packages)
        repositories_message: str = ''

        if count_packages > 0:
            message = f'{count_packages} software updates are available {repositories_message}\n'

        return message, packages

    def view_updates(self) -> None:
        """Prints the updates packages to the terminal.
        """
        message, packages = self.check_updates()
        print(message)
        if len(packages) > 0:
            for package in packages:
                print(package)

    def daemon_status(self) -> bool:
        """Returns the daemon status.

        Returns:
            bool: True | False
        """
        output = subprocess.run(self.sun_daemon_running, shell=True, check=False)
        if output.returncode == 0:
            return True
        return False

    def daemon_process(self, arg: str, message: str) -> str:
        """Returns the daemon status message.

        Args:
            arg (str): Argument command.
            message (str): Message for view.

        Returns:
            str: Message fro print.
        """
        output: int = 1

        command: dict[str, str] = {
            'start': self.sun_daemon_start,
            'stop': self.sun_daemon_stop,
            'restart': self.sun_daemon_restart
        }

        if self.daemon_status() and arg == 'start':
            message = 'SUN is already running'
        elif not self.daemon_status() and arg == 'stop':
            message = 'SUN is not running'
        elif not self.daemon_status() and arg == 'restart':
            message = 'SUN is not running'
        else:
            output = subprocess.call(command[arg], shell=True)

        if output > 0:
            message = f'FAILED [{output}]: {message}'

        return message


class Cli(Tools, Configs):
    """Command line control menu.

    Attributes:
        utils (TYPE): Utilities.
    """

    def __init__(self) -> None:
        super().__init__()
        self.args: list[str] = sys.argv
        self.utils = Utilities()

    def menu(self) -> None:
        """Menu call methods.

        Raises:
            SystemExit: Exit.
        """
        self.su()
        self.args.pop(0)

        process: dict[str, Callable] = {
            'start': self.view_start,
            'stop': self.view_stop,
            'restart': self.view_restart,
            'status': self.view_status,
            'check': self.view_updates,
            'info': self.view_os_info,
            'help': self.usage
        }

        if len(self.args) == 1:
            try:
                process[self.args[0]]()
            except KeyError as e:
                raise SystemExit("try: 'sun help'") from e

        elif len(self.args) == 2 and self.args[0] == 'start' and self.args[1] == '--tray':
            subprocess.call('sun-tray &', shell=True)

        else:
            raise SystemExit("try: 'sun help'")

    def view_start(self) -> None:
        """View starting message.
        """
        result = self.daemon_process(self.args[0], 'Starting SUN daemon:  /usr/bin/sun-daemon')
        self.print_result(result)

    def view_stop(self) -> None:
        """View stopping message.
        """
        pid = self.utils.get_daemon_pid()
        if pid:
            pid = f' (PID {pid})'
        result = self.daemon_process(self.args[0],
                                     f'Stopping SUN daemon:  /usr/bin/sun-daemon{pid}')
        self.print_result(result)

    def view_restart(self) -> None:
        """View restarting message.
        """
        pid = self.utils.get_daemon_pid()
        if pid:
            pid = f' (PID {pid})'
        result = self.daemon_process(self.args[0],
                                     f'Restarting SUN daemon:  /usr/bin/sun-daemon{pid}')
        self.print_result(result)

    def view_status(self) -> None:
        """View status message.
        """
        pid = self.utils.get_daemon_pid()
        print(f'SUN is running as PID {pid}' if self.daemon_status() else 'SUN is not running')

    def view_os_info(self) -> None:
        """View info message.
        """
        html_text: str = self.utils.os_info_html()
        clean_text = re.sub(r'<[^>]+>', '', html_text)
        text = clean_text.replace('<br>', '\n').strip()
        print(text)

    def print_result(self, result: str) -> None:
        """Print result with delay 1 second.

        Args:
            result (str): Message for print.
        """
        if result.startswith('FAILED'):
            print(result)
        else:
            print(result, end=' ', flush=True)
            time.sleep(1)
            print(f'{self.bgreen}Done{self.endc}')


def main() -> None:
    """Call menu object.

    Raises:
        SystemExit: Exit.
    """
    try:
        cli = Cli()
        cli.menu()
    except KeyboardInterrupt as e:
        raise SystemExit(1) from e
