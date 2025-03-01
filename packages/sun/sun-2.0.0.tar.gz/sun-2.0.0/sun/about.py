#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sun.__metadata__ import __copyright__, __license_link__, __website__

about_text: str = f"""
            <h3><b>SUN (Slackware Update Notifier)</b></h3><br>
            SUN is a tray notification applet and daemon for informing about package updates in Slackware.
            It also serves as a CLI tool for monitoring upgraded packages.<br><br>
            Copyright: {__copyright__} © Dimitris Zlatanidis<br><br>
            <a href='http://www.slackware.com/'>Slackware®</a> is a Registered Trademark of Patrick Volkerding.<br>
            <a href='https://www.kernel.org/'>Linux®</a> is a Registered Trademark of Linus Torvalds.<br><br>
            License: <a href='{__license_link__}'>GNU General Public License v3 or later (GPLv3+)</a><br><br>
            Home: <a href='{__website__}'>{__website__}</a><br>
        """
