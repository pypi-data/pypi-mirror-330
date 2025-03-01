#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import platform
import re
import socket
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

import psutil

__prgnam__: str = 'sun'
__author__: str = 'dslackw'
__copyright__: str = '2015-2025'
__version__: str = '2.0.0'
__license__: str = 'GNU General Public License v3 (GPLv3)'
__license_link__: str = 'https://www.gnu.org/licenses/gpl-3.0.html'
__email__: str = 'dslackw@gmail.com'
__website__: str = 'https://dslackw.gitlab.io/sun/'


def get_os_info() -> dict[str, Any]:
    """System information.

    Returns:
        dict[str, Any]: System OS data.
    """
    # Get OS release and version.
    with open('/etc/os-release', 'r', encoding='utf-8') as release_file:
        for line in release_file:
            if line.startswith('PRETTY_NAME='):
                os_name = line.split('=', 1)[1].strip().strip('"')

    # Get VGA information.
    command: str = "lspci -mm | grep 'VGA'"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True, check=True)
    pattern = r'"[^"]+"\s+"([^"]+)"\s+"([^"]+)"'
    matches: list[str] = re.findall(pattern, result.stdout)
    gpu_info: str = "\n     ".join([f"{m[0]}, {m[1]}" for m in matches])

    # Get and calculate the uptime.
    boot_time = psutil.boot_time()
    current_time = datetime.now()
    uptime = str(current_time - datetime.fromtimestamp(boot_time))

    data_configs: dict[str, Any] = {
        'bin_path': Path('/', 'usr', 'bin'),
        'pkg_path': Path('/', 'var', 'log', 'packages'),
        'icon_path': Path('/', 'usr', 'share', 'pixmaps'),
        'desktop_path': Path('/', 'usr', 'share', 'applications'),
        'xdg_autostart': Path('/', 'etc', 'xdg', 'autostart'),
        'sun_conf_path': Path('/', 'etc', __prgnam__),
        'os_name': os_name,
        'desktop': os.getenv('XDG_CURRENT_DESKTOP'),
        'arch': platform.machine(),
        'hostname': socket.gethostname(),
        'kernel': platform.release(),
        'cpu': platform.processor(),
        'cpu_cores': psutil.cpu_count(logical=False),
        'logical_cores': psutil.cpu_count(logical=True),
        'mem_used': psutil.virtual_memory().used,
        'mem_free': psutil.virtual_memory().free,
        'mem_total': psutil.virtual_memory().total,
        'mem_percent': psutil.virtual_memory().percent,
        'disk_total': psutil.disk_usage('/').total,
        'disk_used': psutil.disk_usage('/').used,
        'disk_free': psutil.disk_usage('/').free,
        'disk_type': psutil.disk_partitions()[0].fstype,
        'disk_percent': psutil.disk_usage('/').percent,
        'uptime': uptime.split('.', maxsplit=1)[0],
        'gpu': gpu_info
    }
    return data_configs
