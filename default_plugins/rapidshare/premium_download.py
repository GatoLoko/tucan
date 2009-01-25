###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion crakotaku(at)yahoo.es
## Copyright (C) 2008-2009 Paco Salido beakman(at)riseup.net
## Copyright (C) 2008-2009 JM Cordero betic0(at)gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

from accounts import Accounts
from service_config import SECTION_PREMIUM_DOWNLOAD
from download_plugin import DownloadPlugin

from premium_cookie import PremiumCookie

import cons

class PremiumDownload(DownloadPlugin, Accounts):
	""""""
	def __init__(self, config):
		""""""
		Accounts.__init__(self, config, SECTION_PREMIUM_DOWNLOAD, PremiumCookie())
		DownloadPlugin.__init__(self)
		
	def add(self, path, link, file_name):
		""""""
		cookie = self.get_cookie(link)
		if cookie:
			return self.start(path, link, file_name, None, cookie)

	def delete(self, file_name):
		""""""
		print self.stop(file_name)
