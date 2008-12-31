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

import pygtk
pygtk.require('2.0')
import gtk
import gobject

import cons
import config

from service_preferences import ServicePreferences
from message import Message

LANGUAGES = ["English", "French", "German", "Japanese", "Spanish"]

class Preferences(gtk.Dialog):
	""""""
	def __init__(self, configuration):
		""""""
		gtk.Dialog.__init__(self)
		self.set_icon_from_file(cons.ICON_PREFERENCES)
		self.set_title("Preferences")
		self.set_size_request(500,500)
		
		self.config = configuration
		
		self.notebook = gtk.Notebook()
		self.notebook.set_property("homogeneous", True)
		self.vbox.pack_start(self.notebook)
		self.new_page("General Configuration", cons.ICON_PREFERENCES_MAIN, self.init_main())
		self.new_page("Service Configuration", cons.ICON_PREFERENCES_SERVICES, self.init_services())
		self.new_page("Advanced Configuration", cons.ICON_PREFERENCES_ADVANCED, self.init_advanced())

		#action area
		cancel_button = gtk.Button(None, gtk.STOCK_CANCEL)
		save_button = gtk.Button(None, gtk.STOCK_SAVE)
		self.action_area.pack_start(cancel_button)
		self.action_area.pack_start(save_button)
		cancel_button.connect("clicked", self.close)
		save_button.connect("clicked", self.save)
		
		self.connect("response", self.close)
		self.show_all()
		self.run()
		
	def save(self, button):
		""""""
		self.config.set(config.SECTION_MAIN, config.OPTION_LANGUAGE, LANGUAGES[self.language.get_active()])
		self.config.set(config.SECTION_MAIN, config.OPTION_MAX_DOWNLOADS, str(self.max_downloads.get_value_as_int()))
		self.config.set(config.SECTION_MAIN, config.OPTION_MAX_UPLOADS, str(self.max_uploads.get_value_as_int()))
		self.config.set(config.SECTION_MAIN, config.OPTION_DOWNLOADS_FOLDER, self.downloads_folder.get_label())
		
		model = self.treeview.get_model()
		iter = model.get_iter_root()
		while iter:
			configuration = model.get_value(iter, 3)
			configuration.enable(model.get_value(iter, 2))
			if not self.config.has_option(config.SECTION_SERVICES, model.get_value(iter,1)):
				self.config.set(config.SECTION_SERVICES, model.get_value(iter,1), configuration.path)
			iter = model.iter_next(iter)
		
		self.config.set(config.SECTION_ADVANCED, config.OPTION_TRAY_CLOSE, str(self.tray_close.get_active()))
		self.config.set(config.SECTION_ADVANCED, config.OPTION_ADVANCED_PACKAGES, str(self.advanced_packages.get_active()))
		self.config.set(config.SECTION_ADVANCED, config.OPTION_SHOW_UPLOADS, str(self.show_uploads.get_active()))
		
		self.config.save()
		self.close()

	def new_page(self, tab_name, tab_image, page):
		""""""
		vbox = gtk.VBox()
		vbox.pack_start(gtk.image_new_from_file(tab_image))
		vbox.pack_start(gtk.Label(tab_name))
		vbox.show_all()
		self.notebook.append_page(page, vbox)
		self.notebook.set_tab_label_packing(page, True, True, gtk.PACK_START)
		
	def init_main(self):
		""""""
		vbox = gtk.VBox()
		
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_LANGUAGE))
		frame.set_border_width(5)
		vbox.pack_start(frame, False, False)
		hbox = gtk.HBox()
		vbox1 = gtk.VBox()
		frame.add(vbox1)
		hbox = gtk.HBox()
		vbox1.pack_start(hbox, False, False, 5)
		label = gtk.Label("Choose language: ")
		hbox.pack_start(label, False, False, 10)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		hbox.pack_start(aspect)
		self.language = gtk.combo_box_new_text()
		for lang in LANGUAGES:
			self.language.append_text(lang)
		self.language.set_active(LANGUAGES.index(self.config.get(config.SECTION_MAIN, config.OPTION_LANGUAGE)))
		hbox.pack_start(self.language, False, False, 10)

		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_NETWORK))
		frame.set_border_width(5)
		vbox.pack_start(frame, False, False)
		vbox1 = gtk.VBox()
		frame.add(vbox1)
		hbox = gtk.HBox()
		label = gtk.Label("Max simultaneous downloads: ")
		hbox.pack_start(label, False, False, 10)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		hbox.pack_start(aspect)
		self.max_downloads = gtk.SpinButton(None, 1, 0)
		self.max_downloads.set_range(1,10)
		self.max_downloads.set_increments(1,0)
		self.max_downloads.set_numeric(True)
		self.max_downloads.set_value(self.config.getint(config.SECTION_MAIN, config.OPTION_MAX_DOWNLOADS))
		hbox.pack_start(self.max_downloads, False, False, 10)
		vbox1.pack_start(hbox, False, False, 2)
		hbox = gtk.HBox()
		label = gtk.Label("Max simultaneous uploads: ")
		hbox.pack_start(label, False, False, 10)
		aspect = gtk.AspectFrame()
		aspect.set_shadow_type(gtk.SHADOW_NONE)
		hbox.pack_start(aspect)
		self.max_uploads = gtk.SpinButton(None, 1, 0)
		self.max_uploads.set_range(1,10)
		self.max_uploads.set_increments(1,0)
		self.max_uploads.set_numeric(True)
		self.max_uploads.set_value(self.config.getint(config.SECTION_MAIN, config.OPTION_MAX_UPLOADS))
		hbox.pack_start(self.max_uploads, False, False, 10)
		vbox1.pack_start(hbox, False, False, 2)
		
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_FOLDER))
		frame.set_border_width(5)
		vbox.pack_start(frame, False, False)
		vbox1 = gtk.VBox()
		frame.add(vbox1)
		hbox = gtk.HBox()
		vbox1.pack_start(hbox, False, False, 5)
		
		label = gtk.Label("Downloads Folder: ")
		hbox.pack_start(label, False, False, 10)
		path = self.config.get(config.SECTION_MAIN, config.OPTION_DOWNLOADS_FOLDER)
		self.downloads_folder = gtk.Label(path)
		hbox.pack_start(self.downloads_folder, False, False, 10)
		bbox = gtk.HButtonBox()
		bbox.set_layout(gtk.BUTTONBOX_END)
		hbox.pack_start(bbox, True, True, 10)
		button = gtk.Button(None, gtk.STOCK_OPEN)
		button.connect("clicked", self.choose_path, self.on_choose_folder)
		bbox.pack_start(button)
		
		vbox.show_all()
		return vbox

	def choose_path(self, button, choose_callback):
		""""""
		self.filechooser = gtk.FileChooserDialog('Select a Folder', self, gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
		#self.filechooser.set_filename(filename)
		self.filechooser.action_area.set_layout(gtk.BUTTONBOX_EDGE)
		self.filechooser.set_show_hidden(False)
		hidden_button = gtk.CheckButton("Show hidden files.")
		self.filechooser.action_area.pack_start(hidden_button)
		hidden_button.connect("clicked", self.show_hidden)
		choose_button = gtk.Button(None, gtk.STOCK_OK)
		self.filechooser.action_area.pack_start(choose_button)
		self.filechooser.connect("response", choose_callback, False)
		choose_button.connect("clicked", choose_callback, None, True)
		self.filechooser.set_position(gtk.WIN_POS_CENTER)
		self.filechooser.show_all()
		self.filechooser.run()
		
	def show_hidden(self, button):
		""""""
		self.filechooser.set_show_hidden(button.get_active())

	def on_choose_folder(self, widget, response, choosed):
		""""""
		if choosed:
			self.downloads_folder.set_label(self.filechooser.get_filename() + "/")
		self.filechooser.destroy()
		del self.filechooser

	def init_services(self):
		""""""
		vbox = gtk.VBox()
		
		frame = gtk.Frame()
		frame.set_size_request(-1, 300)
		vbox.pack_start(frame)
		frame.set_border_width(10)
		scroll = gtk.ScrolledWindow()
		frame.add(scroll)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		store = gtk.ListStore(gtk.gdk.Pixbuf, str, bool, gobject.TYPE_PYOBJECT)
		self.treeview = gtk.TreeView(store)
		scroll.add(self.treeview)
		self.treeview.connect("row-activated", self.service_preferences)
		
		self.treeview.set_rules_hint(True)
		self.treeview.set_headers_visible(False)
		
		tree_icon = gtk.TreeViewColumn('Icon') 
		icon_cell = gtk.CellRendererPixbuf()
		icon_cell.set_property("width", 100)
		tree_icon.pack_start(icon_cell, True)
		tree_icon.add_attribute(icon_cell, 'pixbuf', 0)
		self.treeview.append_column(tree_icon)
		
		tree_name = gtk.TreeViewColumn('Name')
		name_cell = gtk.CellRendererText()
		name_cell.set_property("width", 300)
		tree_name.pack_start(name_cell, True)
		tree_name.add_attribute(name_cell, 'text', 1)
		self.treeview.append_column(tree_name)
		
		tree_enable = gtk.TreeViewColumn('Enable')
		enable_cell = gtk.CellRendererToggle()
		enable_cell.connect("toggled", self.toggled)
		tree_enable.pack_start(enable_cell, False)
		tree_enable.add_attribute(enable_cell, 'active', 2)
		self.treeview.append_column(tree_enable)
		
		#fill store
		for path, icon_path, name, enabled, configuration in self.config.get_services():
			self.add_service(path, icon_path, name, enabled, configuration)
		
		frame = gtk.Frame()
		frame.set_border_width(10)
		frame.set_shadow_type(gtk.SHADOW_NONE)
		vbox.pack_start(frame, False, False)
		bbox = gtk.HButtonBox()
		bbox.set_layout(gtk.BUTTONBOX_START)
		frame.add(bbox)
		button = gtk.Button(None, gtk.STOCK_ADD)
		button.connect("clicked", self.choose_path, self.on_choose_service)
		bbox.pack_start(button)
		button = gtk.Button(None, gtk.STOCK_REMOVE)
		button.connect("clicked", self.delete_service)
		bbox.pack_start(button)
		
		return vbox
		
	def add_service(self, path, icon_path, name, enabled, configuration):
		""""""
		if configuration:
			if icon_path:
				icon = gtk.gdk.pixbuf_new_from_file(icon_path)
			else:
				icon = gtk.gdk.pixbuf_new_from_file(cons.ICON_MISSING)
			self.treeview.get_model().append((icon, name, enabled, configuration))
		else:
			Message(cons.SEVERITY_ERROR, path , "The choosed directory isn't a service, or it's not configured.")

	def on_choose_service(self, widget, response, choosed):
		""""""
		path = self.filechooser.get_filename() + "/"
		self.filechooser.destroy()
		if choosed:
			model = self.treeview.get_model()
			package, icon_path, name, enabled, configuration = self.config.service(path)
			self.add_service(path, icon_path, name, enabled, configuration)
		del self.filechooser
		
	def delete_service(self, button):
		""""""
		model, iter = self.treeview.get_selection().get_selected()
		if iter:
			next_iter = model.iter_next(iter)
			self.config.remove_option(config.SECTION_SERVICES, model.get_value(iter, 1))
			model.remove(iter)
			if next_iter:
				self.treeview.set_cursor_on_cell(model.get_path(next_iter))

	def toggled(self, button, path):
		""""""
		model = self.treeview.get_model()
		if button.get_active():
			active = False
		else:
			tos = "Before using this service, you must accept it's terms of service at " + model.get_value(model.get_iter(path), 1)
			m = Message(cons.SEVERITY_INFO, "Terms of service", tos, True)
			active = m.accepted
		button.set_active(active)
		model.set_value(model.get_iter(path), 2, active)
		
	def service_preferences(self, treeview, path, view_column):
		""""""
		model = treeview.get_model()
		icon = model.get_value(model.get_iter(path), 0)
		name = model.get_value(model.get_iter(path), 1)
		config = model.get_value(model.get_iter(path), 3)
		ServicePreferences(name, icon, config)

	def init_advanced(self):
		""""""
		frame = gtk.Frame()
		frame.set_label_widget(gtk.image_new_from_file(cons.ICON_ADVANCED))
		frame.set_border_width(10)
		hbox = gtk.HBox()
		frame.add(hbox)
		vbox = gtk.VBox()
		hbox.pack_start(vbox, True, True, 10)
		
		self.tray_close = gtk.CheckButton("Close to tray.")
		vbox.pack_start(self.tray_close, False, False, 5)
		self.tray_close.set_active(self.config.getboolean(config.SECTION_ADVANCED, config.OPTION_TRAY_CLOSE))

		self.save_session = gtk.CheckButton("Save session on close.")
		vbox.pack_start(self.save_session, False, False, 5)
		self.save_session.set_active(self.config.getboolean(config.SECTION_ADVANCED, config.OPTION_SAVE_SESSION))

		self.advanced_packages = gtk.CheckButton("Default advanced packages.")
		vbox.pack_start(self.advanced_packages, False, False, 5)
		self.advanced_packages.set_active(self.config.getboolean(config.SECTION_ADVANCED, config.OPTION_ADVANCED_PACKAGES))

		self.show_uploads = gtk.CheckButton("Show uploads.")
		vbox.pack_start(self.show_uploads, False, False, 5)
		self.show_uploads.set_active(self.config.getboolean(config.SECTION_ADVANCED, config.OPTION_SHOW_UPLOADS))
			
		return frame
		
	def close(self, widget=None, other=None):
		""""""
		self.destroy()
	
if __name__ == "__main__":
	x = Preferences(config.Config())
