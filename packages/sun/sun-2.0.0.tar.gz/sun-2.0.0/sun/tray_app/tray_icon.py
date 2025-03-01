#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
from typing import Any, Union

from PyQt5 import QtCore, QtGui, QtWidgets
from sun.__metadata__ import __prgnam__, get_os_info
from sun.about import about_text
from sun.cli.tool import Tools
from sun.configs import Configs
from sun.utils import Utilities


def get_theme_colors() -> tuple[Union[str, None], Union[str, None]]:
    """Get background and text color from enable gtk theme.
    This will work with both GTK3 and GTK4 themes with gtk.css file.

    Returns:
        tuple[Union[str, None], Union[str, None]]: (bg_color, text_color)
    """
    theme_name = subprocess.check_output(['gsettings', 'get', 'org.gnome.desktop.interface',
                                          'gtk-theme']).decode().strip().strip("'")

    gtk3_path = f'/usr/share/themes/{theme_name}/gtk-3.0/gtk.css'
    gtk4_path = f'/usr/share/themes/{theme_name}/gtk-4.0/gtk.css'

    if os.path.exists(gtk3_path):
        theme_path = gtk3_path
    elif os.path.exists(gtk4_path):
        theme_path = gtk4_path
    else:
        return None, None

    with open(theme_path, 'r', encoding='utf-8') as file:
        content = file.read()

        bg_color_match = re.search(r'@define-color\s+theme_base_color\s+(#\w+);', content)
        bg_color = bg_color_match.group(1) if bg_color_match else None

        fg_color_match = re.search(r'@define-color\s+theme_fg_color\s+(#\w+);', content)
        text_color = fg_color_match.group(1) if fg_color_match else None

        return bg_color, text_color


class TrayIcon(QtWidgets.QSystemTrayIcon, Configs):

    """SUN Tray Icon App.

    Attributes:
        menu (TYPE): Menu Qt Widgets.
        msg_box (TYPE): Message box.
        tool (TYPE): Tool object.
    """

    def __init__(self) -> None:
        super().__init__()
        self.tool = Tools()
        self.data_configs: dict[str, Any] = get_os_info()
        self.icon_path: str = f"{self.data_configs['icon_path']}/{__prgnam__}"
        self.msg_box: QtWidgets.QMessageBox

        # Icon definition
        self.setIcon(QtGui.QIcon(f'{self.icon_path}/{__prgnam__}.png'))
        self.setToolTip('SUN (Slackware Update Notifier)')  # Tooltip

        # Create a main menu
        self.menu = QtWidgets.QMenu()

        # Adding submenu
        submenu = self.menu.addMenu('Daemon')
        assert submenu is not None
        submenu.setIcon(QtGui.QIcon(f'{self.icon_path}/daemon.png'))

        # Adding items to the submenu
        start = submenu.addAction('Start')
        assert start is not None
        start.setIcon(QtGui.QIcon(f'{self.icon_path}/start.png'))
        start.triggered.connect(self.daemon_start)

        stop = submenu.addAction('Stop')
        assert stop is not None
        stop.setIcon(QtGui.QIcon(f'{self.icon_path}/stop.png'))
        stop.triggered.connect(self.daemon_stop)

        restart = submenu.addAction('Restart')
        assert restart is not None
        restart.setIcon(QtGui.QIcon(f'{self.icon_path}/restart.png'))
        restart.triggered.connect(self.daemon_restart)

        status = submenu.addAction('Status')
        assert status is not None
        status.setIcon(QtGui.QIcon(f'{self.icon_path}/status.png'))
        status.triggered.connect(self.daemon_status)

        # Adding a simple item to the menu
        check_updates = self.menu.addAction('Check Updates')
        assert check_updates is not None
        check_updates.setIcon(QtGui.QIcon(f'{self.icon_path}/check.png'))
        check_updates.triggered.connect(self.show_check_updates)

        os_info = self.menu.addAction('Os Info')
        assert os_info is not None
        os_info.setIcon(QtGui.QIcon(f'{self.icon_path}/info.png'))
        os_info.triggered.connect(self.show_os_info)

        # Adding separator
        self.menu.addSeparator()

        # Add the 'About' option
        about = self.menu.addAction('About')
        assert about is not None
        about.setIcon(QtGui.QIcon(f'{self.icon_path}/about.png'))
        about.triggered.connect(self.show_about)

        # Adding 'Exit'
        exit_action = self.menu.addAction('Exit')
        assert exit_action is not None
        exit_action.setIcon(QtGui.QIcon(f'{self.icon_path}/exit.png'))
        exit_action.triggered.connect(self.exit_app)

        # Setting the menu in the tray icon
        self.setContextMenu(self.menu)

        # Event connection
        self.activated.connect(self.on_tray_icon_activated)

    def on_tray_icon_activated(self, reason: QtWidgets.QSystemTrayIcon.ActivationReason) -> None:
        """Left click.

        Args:
            reason (QtWidgets.QSystemTrayIcon.ActivationReason): Check the reason.
        """
        if reason == QtWidgets.QSystemTrayIcon.Trigger:  # type: ignore[attr-defined]
            self.show_check_updates()

    def show_message(self, data: str, title: str) -> None:
        """Summary

        Args:
            data (str): Text message.
            title (str): Window title.
        """
        icon = QtGui.QIcon(f"{self.icon_path}/{__prgnam__}")
        icon_about = QtGui.QIcon(f"{self.icon_path}/about.png")
        icon_osinfo = QtGui.QIcon(f"{self.icon_path}/info.png")
        icon_check = QtGui.QIcon(f"{self.icon_path}/check.png")

        icon_start = QtGui.QIcon(f"{self.icon_path}/start.png")
        icon_stop = QtGui.QIcon(f"{self.icon_path}/stop.png")
        icon_restart = QtGui.QIcon(f"{self.icon_path}/restart.png")
        icon_status = QtGui.QIcon(f"{self.icon_path}/status.png")

        self.msg_box = QtWidgets.QMessageBox()

        bg_color, text_color = get_theme_colors()

        self.msg_box.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                color: {text_color};
            }}
        """)

        self.msg_box.setWindowTitle(title)
        self.msg_box.setWindowIcon(icon)
        self.msg_box.setIconPixmap(icon.pixmap(72, 72))
        self.msg_box.setText(data)
        if title.endswith(('Start', 'Stop', 'Restart')) and not data.startswith('FAILED'):
            self.msg_box.setStandardButtons(QtWidgets.QMessageBox.NoButton)
        else:
            self.msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)

        icons: dict[str, Any] = {
            'SUN - About': icon_about.pixmap(42, 42),
            'SUN - OS Info': icon_osinfo.pixmap(42, 42),
            'SUN - Check Updates': icon_check.pixmap(72, 72),
            'SUN - Daemon Start': icon_start.pixmap(72, 72),
            'SUN - Daemon Stop': icon_stop.pixmap(72, 72),
            'SUN - Daemon Restart': icon_restart.pixmap(72, 72),
            'SUN - Daemon Status': icon_status.pixmap(72, 72)
        }
        self.msg_box.setIconPixmap(icons[title])

        self.msg_box.setModal(False)
        self.msg_box.show()

        if title.endswith(('Start', 'Stop', 'Restart')) and not data.startswith('FAILED'):
            QtCore.QTimer.singleShot(1000, self.show_ok_button)

    def show_ok_button(self) -> None:
        """Update message box text.
        """
        self.msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)

    def show_check_updates(self) -> None:
        """Show message updates.
        """
        title: str = 'SUN - Check Updates'
        data, packages = self.tool.check_updates()
        count: int = len(packages)
        if count > 0:
            packages = packages[:10]
            if count > 10:
                packages += ['\nand more...']
            self.show_message('{0}\n{1}'.format(data, '\n'.join(packages)), title)
        else:
            self.show_message(data, title)

    def show_os_info(self) -> None:
        """Show message OS info.
        """
        title: str = 'SUN - OS Info'
        data: str = Utilities().os_info_html()
        self.show_message(data, title)

    def daemon_start(self) -> None:
        """Show message and start the daemon.
        """
        title: str = 'SUN - Daemon Start'
        data: str = 'SUN daemon starting...'
        data = self.tool.daemon_process('start', data)
        self.show_message(data, title)

    def daemon_stop(self) -> None:
        """Show message and stop the daemon.
        """
        title: str = 'SUN - Daemon Stop'
        pid = Utilities().get_daemon_pid()
        if pid:
            pid = f' (PID {pid})'
        data: str = f'SUN daemon stopping...{pid}'
        data = self.tool.daemon_process('stop', data)
        self.show_message(data, title)

    def daemon_restart(self) -> None:
        """Show message and restart the daemon.
        """
        title: str = 'SUN - Daemon Restart'
        pid = Utilities().get_daemon_pid()
        if pid:
            pid = f' (PID {pid})'
        data: str = f'SUN daemon restarting...{pid}'
        data = self.tool.daemon_process('restart', data)
        self.show_message(data, title)

    def daemon_status(self) -> None:
        """Show message status about the daemon.
        """
        title: str = 'SUN - Daemon Status'
        pid = Utilities().get_daemon_pid()
        data: str = (f'SUN is running as PID {pid}\t' if self.tool.daemon_status()
                     else 'SUN is not running\t')
        self.show_message(data, title)

    def show_about(self) -> None:
        """Show about dialog box.
        """
        title: str = 'SUN - About'
        self.show_message(about_text, title)

    def exit_app(self) -> None:
        """Exit the app.
        """
        print('Exiting...')
        QtWidgets.qApp.quit()


def main() -> None:
    """Main function.
    """
    app = QtWidgets.QApplication(sys.argv)

    # Don't close the application when the last window is closed
    app.setQuitOnLastWindowClosed(False)

    tray_icon = TrayIcon()
    tray_icon.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
