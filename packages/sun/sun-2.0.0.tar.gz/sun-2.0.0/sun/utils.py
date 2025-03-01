#!/usr/bin/python3
# -*- coding: utf-8 -*-

import getpass
import os
import re
from pathlib import Path
from typing import Any, Generator

import urllib3
from urllib3.exceptions import HTTPError

from sun.__metadata__ import get_os_info
from sun.configs import Configs


class Utilities(Configs):
    """General utilities.
    """

    def __init__(self) -> None:
        super().__init__()
        self.data_configs: dict[str, Any] = get_os_info()

    @staticmethod
    def read_repo_text_file(mirror: str) -> str:
        """Reads repository ChangeLog.txt file.

        Args:
            mirror (str): HTTP mirror.

        Returns:
            str: The ChangeLog.txt file lines.
        """
        log_txt: str = str()
        try:
            http = urllib3.PoolManager()
            con = http.request('GET', mirror)
            log_txt = con.data.decode()
        except KeyError:
            print('SUN: Error: Ftp mirror not supported')
        except HTTPError:
            print(f'SUN: Error: Failed to connect to {mirror}')

        return log_txt

    @staticmethod
    def read_local_text_file(registry: Path) -> str:
        """Reads the local ChangeLog.txt file.

        Args:
            registry (Path): The local file for reading.

        Returns:
            str: The ChangeLog.txt file lines.
        """
        log_txt: str = str()
        if registry.is_file():
            with open(registry, 'r', encoding='utf-8', errors='ignore') as file_txt:
                log_txt = file_txt.read()
        else:
            print(f"\nSUN: Error: Failed to find '{registry}' file.\n")

        return log_txt

    @staticmethod
    def convert_sizes(byte_size: float) -> str:
        """Convert bytes to kb, mb and gb.

        Args:
            byte_size (float): The file size in bytes.

        Returns:
            str
        """
        kb_size: float = byte_size / 1024
        mb_size: float = kb_size / 1024
        gb_size: float = mb_size / 1024

        if gb_size >= 1:
            return f"{gb_size:.0f} GB"
        if mb_size >= 1:
            return f"{mb_size:.0f} MB"
        if kb_size >= 1:
            return f"{kb_size:.0f} KB"

        return f"{byte_size} B"

    def get_daemon_pid(self) -> str:
        """Read and return the current PID of sun-daemon.

        Returns:
            str: PID of sun-daemon.
        """
        home_user = os.path.expanduser('~')
        pid_path: Path = Path(home_user, '.run', 'sun-daemon.pid')
        if pid_path.is_file():
            pid = self.read_local_text_file(pid_path)
            return pid.strip()
        return ''

    def os_info_html(self) -> str:
        """Returns the distribution information.

        Returns:
            str: System info.
        """
        html_text: str = f"""[System]<br>
<b>User</b>: {getpass.getuser()}<br>
<b>OS</b>: {self.data_configs['os_name']}<br>
<b>Desktop</b>: {self.data_configs['desktop']}<br>
<b>Hostname</b>: {self.data_configs['hostname']}<br>
<b>Arch</b>: {self.data_configs['arch']}<br>
<b>Packages</b>: {len(list(self.data_configs['pkg_path'].iterdir()))}<br>
<b>Kernel</b>: {self.data_configs['kernel']}<br>
<b>Uptime</b>: {self.data_configs['uptime']}<br><br>
[Processor]<br>
<b>CPU</b>: {self.data_configs['cpu']}<br>
<b>Cores</b>: {self.data_configs['cpu_cores']}<br>
<b>Logical Cores</b>: {self.data_configs['logical_cores']}<br><br>
[Memory]<br>
<b>Free</b>: {self.convert_sizes(self.data_configs['mem_free'])}<br>
<b>Used</b>: {self.convert_sizes(self.data_configs['mem_used'])}<br>
<b>Total</b>: {self.convert_sizes(self.data_configs['mem_total'])}<br>
<b>Percent</b>: {self.data_configs['mem_percent']}%<br><br>
[Disk]<br>
<b>Free</b>: {self.convert_sizes(self.data_configs['disk_free'])}<br>
<b>Used</b>: {self.convert_sizes(self.data_configs['disk_used'])}<br>
<b>Total</b>: {self.convert_sizes(self.data_configs['disk_total'])}<br>
<b>Percent</b>: {self.data_configs['disk_percent']}%<br>
<b>Type</b>: {self.data_configs['disk_type']}<br><br>
[GPU]<br>
<b>VGA</b>: {self.data_configs['gpu']}"""
        return html_text


class Fetch(Utilities):  # pylint: disable=[R0902]
    """Fetching how many packages and from where have upgraded,
    removed or added.

    Attributes:
        local_date (str): Date of local ChangeLog file.
        local_log (TYPE): Local ChangeLog file.
        mirror_log (TYPE): Remote ChangeLog file.
        repo_days (str): The days of repository ChangeLog file.
        repo_pattern (str): Regex pattern to match packages.
    """

    def __init__(self):
        super(Utilities).__init__()
        self.local_date = None
        self.repo_pattern = r'\.txz:\s*(Upgraded\.|Rebuilt\.|Added\.|Removed\.)$'
        self.repo_days = r'^(Mon|Tue|Wed|Thu|Fri|Sat|Sun)'
        self.mirror_log = None
        self.local_log = None

    def updates(self) -> Generator:
        """Fetching all the necessary packages.

        Yields:
            Generator: Matched packages.
        """
        if self.repo_mirror and self.repo_log_path:
            self.assign_mirror_log_file()
            self.assign_local_log_file()
            self.assign_local_date()

            for line in self.mirror_log.splitlines():
                if self.local_date == line.strip():
                    break
                if re.search(self.repo_pattern, line):
                    line = self.patch_line_for_slackware(line)
                    yield f'{line.split("/")[-1]}'

    def patch_line_for_slackware(self, line: str) -> str:
        """Patches the line for linux updates.

        Args:
            line (str): ChangeLog.txt line for patching.

        Returns:
            str: Patching line.
        """
        if line.startswith('patches/packages/linux'):
            line = line.split("/")[-2]
        return line

    def assign_local_date(self) -> None:
        """Finds the date from the local log file and assigned.
        """
        for line in self.local_log.splitlines():
            if re.match(self.repo_days, line):
                self.local_date = line.strip()
                break

    def assign_mirror_log_file(self) -> None:
        """Assign the remote ChangeLog.txt file.
        """
        self.mirror_log = self.read_repo_text_file(f'{self.repo_mirror}{self.repo_log_file}')

    def assign_local_log_file(self) -> None:
        """Assign the local ChangeLog.txt file.
        """
        self.local_log = self.read_local_text_file(Path(self.repo_log_path, self.repo_log_file))
        if not self.local_log:
            self.local_date = ''
