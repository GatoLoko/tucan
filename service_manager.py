###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2009 Fran Lupion Crakotak(at)yahoo.es
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

import urlparse
import re
import sys

from config import SECTION_MAIN, OPTION_MAX_DOWNLOADS
from download_manager import DownloadManager

import cons

class Service:
	""""""
	def __init__(self, name):
		""""""
		self.name = name
		self.anonymous_download_plugin = None
		self.user_download_plugin = None
		self.premium_download_plugin = None
		self.check_links = None
		self.anonymous_upload_plugins = None
		self.user_upload_plugins = None
		self.premium_upload_plugins = None
		self.check_files = None

class ServiceManager:
	""""""
	def __init__(self, configuration):
		""""""
		self.download_manager = DownloadManager(configuration.get(SECTION_MAIN, OPTION_MAX_DOWNLOADS))
		self.services = []
		if not configuration.plugins_path in sys.path:
			sys.path.append(configuration.plugins_path)
		for package, icon, service, enabled, config in configuration.get_services():
			s = Service(service)
			if enabled:
				#download plugins
				check_module, check_name = config.check_links()
				if check_name:
					module = __import__(package + "." + check_module, None, None, [''])
					s.check_links = eval("module" + "." + check_name + "()")
				for plugin_module, plugin_name, plugin_type in config.get_download_plugins():
					module = __import__(package + "." + plugin_module, None, None, [''])
					if plugin_type == cons.TYPE_ANONYMOUS:
						s.anonymous_download_plugin = eval("module" + "." + plugin_name + "()")
					elif plugin_type == cons.TYPE_USER:
						s.user_download_plugin = eval("module" + "." + plugin_name + "()")
					elif plugin_type == cons.TYPE_PREMIUM:
						s.premium_download_plugin = eval("module" + "." + plugin_name + "(config)")
				check_module, check_name = config.check_files()
				#upload plugins
				if check_name:
					module = __import__(package + "." + check_module, None, None, [''])
					s.check_files = eval("module" + "." + check_name + "()")
				for plugin_module, plugin_name, plugin_type in config.get_upload_plugins():
					module = __import__(package + "." + plugin_module, None, None, [''])
					if plugin_type == cons.TYPE_ANONYMOUS:
						s.anonymous_upload_plugin = eval("module" + "." + plugin_name + "()")
					elif plugin_type == cons.TYPE_USER:
						s.user_upload_plugin = eval("module" + "." + plugin_name + "()")
					elif plugin_type == cons.TYPE_PREMIUM:
						s.premium_upload_plugin = eval("module" + "." + plugin_name + "(config)")
				self.services.append(s)

	def prueba(self):
		""""""
		import time
		link = "http://www.gigasize.com/get.php?d=726jhznl0pc"
		service = "gigasize.com"
		name, size, unit = self.get_check_links(service)(link)
		if name:
			plugin, plugin_type = self.get_download_plugin(service)
			print plugin_type
			print plugin.add("/home/crak/downloads/", link, name)
		while len(plugin.active_downloads) > 0:
			print plugin.get_status(name)
			time.sleep(2)

	def get_download_plugin(self, service_name):
		""""""
		for service in self.services:
			if service.name == service_name:
				if ((service.premium_download_plugin) and (service.premium_download_plugin.active)):
					return service.premium_download_plugin, cons.TYPE_PREMIUM
				else:
					return service.anonymous_download_plugin, cons.TYPE_ANONYMOUS

	def get_upload_plugin(self, service_name):
		""""""
		for service in self.services:
			if service.name == service_name:
				return service.anonymous_upload_plugin
		
	def get_check_links(self, service_name):
		""""""
		for service in self.services:
			if service.name == service_name:
				return service.check_links.check

	def get_check_files(self, service_name):
		""""""
		for service in self.services:
			if service.name == service_name:
				return service.check_files.check

	def filter_service(self, links):
		""""""
		services = {cons.TYPE_UNSUPPORTED: []}
		for link in links:
			found = False
			print link
			if urlparse.urlparse(link).scheme == "http":
				link = "http" + link.split("http").pop()
				for service in self.services:
					if link.find(service.name) > 0:
						found = True
						if service.name in services:
							services[service.name].append(link)
						else:
							services[service.name] = [link]
				if not found:
						services[cons.TYPE_UNSUPPORTED].append(link)
		return services

	def create_packages(self, dict):
		""""""
		packages = []
		files = []
		for service, links in dict.items():
			for link in links:
				found = False
				for tmp_link in files:
					if link[1] == tmp_link[1]:
						found = True
						if service not in tmp_link[2]:
							tmp_link[2].append(service)
							tmp_link[0].append(link[0])
							tmp_link[5].append(link[4])
				if not found:
					files.append(([link[0]], link[1], [service], link[2], link[3], [link[4]]))
		while len(files) > 0:
			tmp_name = []
			first = files[0]
			others = files[1:]
			for link in others:
				chars = re.split("[0-9]+", link[1])
				nums = re.split("[^0-9]+", link[1])
				tmp = ""
				for i in chars:
					if tmp+i == first[1][0:len(tmp+i)]:
						tmp += i
						for j in nums:
							if tmp+j == first[1][0:len(tmp+j)]:
								tmp += j
				tmp_name.append(tmp)
			final_name = ""
			for name in tmp_name:
				if len(name) > len(final_name):
					final_name = name
			if len(final_name) > 0:
				packages.append((final_name, [first]))
				del files[files.index(first)]
				tmp_list = []
				for link in files:
					if final_name in link[1]:
						tmp_list.append(link)
				for package_name, package_files in packages:
					if package_name == final_name:
						package_files += tmp_list
				for i in tmp_list:
					del files[files.index(i)]
			else:
				alone_name = first[1]
				alone_name = alone_name.split(".")
				alone_name.pop()
				alone_name = ".".join(alone_name)
				packages.append((alone_name, [first]))
				del files[files.index(first)]
		return packages

	def stop_all(self):
		""""""
		self.download_manager.quit()

if __name__ == "__main__":
	from config import Config
	s = ServiceManager(Config())
	s.prueba()