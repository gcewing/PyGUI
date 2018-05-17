#
#		Python GUI - Menus - Gtk version
#

from gi.repository import Gtk
from gi.repository import Gdk
from GUI.Globals import application
from GUI.GMenus import Menu as GMenu, MenuItem

def _report_accel_changed_(*args):
	print "Menus: accel_changed:", args

class Menu(GMenu):

	def __init__(self, title, items, **kwds):
		GMenu.__init__(self, title, items, **kwds)
		self._gtk_menu = Gtk.Menu()
		self._gtk_accel_group = Gtk.AccelGroup()
		#self._gtk_accel_group.connect('accel_changed', _report_accel_changed_) ###

	def _clear_platform_menu(self):
		gtk_menu = self._gtk_menu
		for gtk_item in gtk_menu.get_children():
			gtk_item.destroy()

	def _add_separator_to_platform_menu(self):
		gtk_item = Gtk.MenuItem()
		gtk_item.set_sensitive(0)
		gtk_separator = Gtk.HSeparator()
		gtk_item.add(gtk_separator)
		self._gtk_add_item(gtk_item)
	
	def _gtk_add_item(self, gtk_item):
		gtk_item.show_all()
		self._gtk_menu.append(gtk_item)

	def _add_item_to_platform_menu(self, item, name, command = None, index = None):
		checked = item.checked
		if checked is None:
			gtk_item = Gtk.MenuItem.new_with_label(name)
		else:
			gtk_item = Gtk.CheckMenuItem.new_with_label(name)
		self._gtk_add_item(gtk_item)
		if not item.enabled:
			gtk_item.set_sensitive(0)
		if checked:
			gtk_item.set_active(1)
		if command:
			app = application()
			if index is not None:
				action = lambda widget: app.dispatch(command, index)
			else:
				action = lambda widget: app.dispatch(command)
			gtk_item.connect('activate', action)
		key = item._key
		if key:
			gtk_modifiers = Gdk.ModifierType.CONTROL_MASK
			if item._shift:
				gtk_modifiers |= Gdk.ModifierType.SHIFT_MASK
			if item._option:
				gtk_modifiers |= Gdk.ModifierType.MOD1_MASK
			gtk_item.add_accelerator('activate', self._gtk_accel_group,
				ord(key), gtk_modifiers, Gtk.AccelFlags.VISIBLE)
