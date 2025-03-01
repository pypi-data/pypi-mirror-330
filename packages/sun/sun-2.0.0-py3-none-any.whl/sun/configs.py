#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
from pathlib import Path
from typing import Any

from sun.__metadata__ import __prgnam__, get_os_info


class Configs:  # pylint: disable=[R0903]

    """General configs.
    """

    # Configuration files.
    data_configs: dict[str, Any] = get_os_info()
    config_file: str = f'{__prgnam__}.conf'
    config_path: str = data_configs['sun_conf_path']
    sun_conf: Path = Path(config_path, config_file)

    # Colors
    bold: str = '\033[1m'
    green: str = '\x1b[32m'
    bgreen: str = f'{bold}{green}'
    endc: str = '\x1b[0m'

    try:
        if sun_conf.is_file():
            configs = configparser.ConfigParser()
            configs.read(sun_conf)
        else:
            raise FileNotFoundError(f"Error: Failed to find '{sun_conf}' file.")

        # Time configs.
        interval = int(configs['TIME']['INTERVAL'])
        standby = int(configs['TIME']['STANDBY'])
        # Daemon configs.
        sun_daemon_start: str = configs['DAEMON']['START']
        sun_daemon_stop: str = configs['DAEMON']['STOP']
        sun_daemon_restart: str = configs['DAEMON']['RESTART']
        sun_daemon_running: str = configs['DAEMON']['RUNNING']
        # Repositories configs.
        repo_mirror: str = configs['REPOSITORY']['HTTP_MIRROR']
        repo_log_path: str = configs['REPOSITORY']['LOG_PATH']
        repo_log_file: str = configs['REPOSITORY']['LOG_FILE']

    except KeyError as error:
        raise SystemExit(f"Error: {error}: in the config file '{sun_conf}'.") from error
