"""
    ResolveURL Addon for Kodi
    Copyright (C) 2016 t0mm0, tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import six
from resolveurl.lib import log_utils

logger = log_utils.Logger.get_logger(__name__)
# addon = xbmcaddon.Addon('script.module.resolveurl')
DIALOG_XML = 'ProgressDialog.xml' if six.PY2 else 'ProgressDialog2.xml'


class ProgressDialog(object):
    dialog = None

    def get_path(self):
        return #addon.getAddonInfo('path')

    def create(self, heading, line1='', line2='', line3=''):
        return
        try:
            self.dialog = ProgressDialog.Window(DIALOG_XML, addon.getSetting('xml_folder'))
        except:
            self.dialog = ProgressDialog.Window(DIALOG_XML, self.get_path())
        self.dialog.show()
        self.dialog.setHeading(heading)
        self.dialog.setLine1(line1)
        self.dialog.setLine2(line2)
        self.dialog.setLine3(line3)

    def update(self, percent, line1='', line2='', line3=''):
        if self.dialog is not None:
            self.dialog.setProgress(percent)
            if line1:
                self.dialog.setLine1(line1)
            if line2:
                self.dialog.setLine2(line2)
            if line3:
                self.dialog.setLine3(line3)

    def iscanceled(self):
        if self.dialog is not None:
            return self.dialog.cancel
        else:
            return False

    def close(self):
        if self.dialog is not None:
            self.dialog.close()
            del self.dialog


