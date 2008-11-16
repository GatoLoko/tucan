###############################################################################
##	Tucan Project

##	Copyright (C) 2008 Fran Lupion Crakotak(at)yahoo.es
##	Copyright (C) 2008 Paco Salido beakman(at)riseup.net
##	Copyright (C) 2008 JM Cordero betic0(at)gmail.com

##	This program is free software; you can redistribute it and/or modify
##	it under the terms of the GNU General Public License as published by
##	the Free Software Foundation; either version 2 of the License, or
##	(at your option) any later version.

##	This program is distributed in the hope that it will be useful,
##	but WITHOUT ANY WARRANTY; without even the implied warranty of
##	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##	GNU General Public License for more details.

##	You should have received a copy of the GNU General Public License
##	along with this program; if not, write to the Free Software
##	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

from .anonymous_plugin import AnonymousPlugin

NAME = "Megaupload Anonimo"
VERSION = "0.1"
AUTHOR = "Crak"

SERVICE = "megaupload.com"
DOWNLOAD_SLOTS = 1
UPLOAD_SLOTS = 1

class AnonymousMegaupload(AnonymousPlugin):
	""""""
	def __init__(self):
		""""""
		self.service = SERVICE
		AnonymousPlugin.__init__(self, DOWNLOAD_SLOTS, UPLOAD_SLOTS)

if __name__ == "__main__":
    p = AnonymousMegaupload()