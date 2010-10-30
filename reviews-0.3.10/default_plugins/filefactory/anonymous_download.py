###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
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

import urllib

import logging
logger = logging.getLogger(__name__)

from core.download_plugin import DownloadPlugin
from core.recaptcha import Recaptcha
from core.url_open import URLOpen

BASE_URL = "http://filefactory.com"
WAIT = 30 #Default, also parsed in the page if possible

class AnonymousDownload(DownloadPlugin):
	""""""
	def link_parser(self, url, wait_func, range=None):
		""""""
		link = None
		retry = 3
		try:
			opener = URLOpen()
			for line in opener.open(url).readlines():
				if 'check:' in line:
					check = line.split("check:'")[1].replace("'","").strip()
				elif "Recaptcha.create" in line:
					tmp = line.split('("')[1].split('"')[0]
					recaptcha_link = "http://www.google.com/recaptcha/api/challenge?k=%s" % tmp 
					if not wait_func():
						return
					c = Recaptcha(BASE_URL, recaptcha_link)
					while not link and retry:
						challenge, response = c.solve_captcha()
						if response:
							if not wait_func():
								return

							#Filefactory perfoms as check on its server by doing an
							#Ajax request sending the following data
							form = urllib.urlencode([("recaptcha_challenge_field", challenge), ("recaptcha_response_field", response), ("recaptcha_shortencode_field", "undefined"),("check", check)])
							url = "%s/file/checkCaptcha.php" % BASE_URL

							#Getting the result back, status:{"ok"|"fail"}
							for line in opener.open(url, form).readlines():
								if 'status:"ok"' in line:
									tmp = line.split('path:"')[1].strip('"')
									tmp_link = BASE_URL + tmp
									for line in opener.open(tmp_link).readlines():
										if '<span class="countdown">' in line:
											#Try to get WAIT from the page
											try:
												tmp = line.split('"countdown">')[1].split("</span")[0]
												tmp = int(tmp)
											except ValueError:
												pass
											else:
												if tmp > 0:
													WAIT = tmp
										if "Download with FileFactory Basic" in line:
											link = line.split('<a href="')[1].split('"')[0]
											break
						retry -= 1
					break
			if link:
				if not wait_func(WAIT):
					return
				return opener.open(link, None, range, True)
		except Exception, e:
			logger.exception("%s: %s" % (url, e))

	def check_links(self, url):
		""""""
		name = None
		size = -1
		unit = None
		try:
			it = iter(URLOpen().open(url).readlines())
			for line in it:
				if '/img/manager/mime/generic.png' in line:
					tmp = line.split('/>')[1].split("</h1>")[0]
					tmp = tmp.replace("&nbsp;","")
					name = tmp.split("&")[0]
					#File with an extension
					if ";" in tmp:
						name = name + tmp.split(";")[1]
				if '<div id="info" class="metadata">' in line:
					tmp = it.next()
					tmp = tmp.split("<span>")[1].split("file")[0].strip()
					size = int(round(float(tmp.split(" ")[0])))
					unit = tmp.split(" ")[1].upper()
		except Exception, e:
			logger.exception("%s :%s" % (url, e))
		return name, size, unit
