#
#   Python GUI - Windows - Gtk version
#

import sys
import gtk
from gtk import gdk
from GUI import export
from GUI import export
from GUI.GGeometry import sub_pt
from GUI import Component
from GUI import Container
from GUI import application
from GUI.GWindows import Window as GWindow

_default_width = 200
_default_height = 200

_modal_styles = ('modal_dialog', 'alert')
_dialog_styles = ('nonmodal_dialog', 'modal_dialog', 'alert')
	
class Window(GWindow):

	#_pass_key_events_to_platform = False

	_size = (_default_width, _default_height)
	_gtk_menubar = None
	_need_menubar_update = 0
	_target = None
	
	def __init__(self, style = 'standard', title = "New Window",
			movable = 1, closable = 1, hidable = None, resizable = 1,
			zoomable = 1, **kwds):
		self._all_menus = []
		modal = style in _modal_styles
		if hidable is None:
			hidable = not modal
		self._resizable = resizable
		gtk_win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		gtk_win.set_gravity(gdk.GRAVITY_STATIC)
		gtk_win.set_decorated(style <> 'fullscreen'
			and (movable or closable or hidable or zoomable))
		gtk_win.set_resizable(resizable)
		gtk_win.set_modal(style in _modal_styles)
		gtk_content = gtk.Layout()
		gtk_content.show()
		if style in _dialog_styles:
			gtk_win.set_type_hint(gdk.WINDOW_TYPE_HINT_DIALOG)
			gtk_win.add(gtk_content)
		else:
			self._gtk_create_menubar()
			gtk_box = gtk.VBox()
			gtk_box.show()
			gtk_box.pack_start(self._gtk_menubar, expand = 0, fill = 0)
			gtk_box.pack_end(gtk_content, expand = 1, fill = 1)
			gtk_win.add(gtk_box)
		self._need_menubar_update = 1
		self._gtk_connect(gtk_win, 'configure-event', self._gtk_configure_event)
		self._gtk_connect(gtk_win, 'key-press-event', self._gtk_key_press_event)
		self._gtk_connect(gtk_win, 'delete-event', self._gtk_delete_event)
		GWindow.__init__(self, _gtk_outer = gtk_win, _gtk_inner = gtk_content, 
			_gtk_focus = gtk_content, _gtk_input = gtk_content,
			style = style, title = title, closable = closable)
		if style == 'fullscreen':
			size = (gdk.screen_width(), gdk.screen_height())
		else:
			size = (_default_width, _default_height)
		self.set_size(size)
		self.set(**kwds)
		self.become_target()
	
	def _gtk_create_menubar(self):
		gtk_menubar = gtk.MenuBar()
		gtk_dummy_item = gtk.MenuItem("")
		gtk_menubar.append(gtk_dummy_item)
		gtk_menubar.show_all()
		h = gtk_menubar.size_request()[1]
		gtk_menubar.set_size_request(-1, h)
		gtk_dummy_item.remove_submenu()
		self._gtk_menubar = gtk_menubar
		self._gtk_connect(gtk_menubar, 'button-press-event',
			self._gtk_menubar_button_press_event)
	
	def destroy(self):
		self.hide()
		GWindow.destroy(self)
	
	def set_menus(self, x):
		GWindow.set_menus(self, x)
		self._need_menubar_update = 1
		if self.visible:
			self._gtk_update_menubar()
	
	def get_title(self):
		return self._gtk_outer_widget.get_title()
	
	def set_title(self, new_title):
		self._gtk_outer_widget.set_title(new_title)
	
	def set_position(self, v):
		self._position = v
		self._gtk_outer_widget.move(*v)
	
	def set_size(self, new_size):
		w, h = new_size
		if self._resizable:
			h += self._gtk_menubar_height()
			gtk_resize = self._gtk_outer_widget.resize
		else:
			gtk_resize = self._gtk_inner_widget.set_size_request
		gtk_resize(max(w, 1), max(h, 1))
		self._size = new_size
	
	def _gtk_configure_event(self, gtk_event):
		gtk_win = self._gtk_outer_widget
		self._position = gtk_win.get_position()
		#self._update_size(gtk_win.get_size())
		w, h = gtk_win.get_size()
		#w, h = self._gtk_inner_widget.get_size()
		#w, h = self._gtk_inner_widget.size_request()
		old_size = self._size
		new_size = (w, h - self._gtk_menubar_height())
		#new_size = (w, h)
		#print "Window._gtk_configure_event:", old_size, "->", new_size ###
		self._size = new_size
		if old_size <> new_size:
			self._resized(sub_pt(new_size, old_size))	
	
	def get_visible(self):
		return self._gtk_outer_widget.get_property('visible')
	
	def set_visible(self, new_v):
		old_v = self.visible
		self._gtk_outer_widget.set_property('visible', new_v)
		if new_v and not old_v and self._need_menubar_update:
			self._gtk_update_menubar()
	
	def _show(self):
		self.set_visible(1)
		self._gtk_outer_widget.present()
	
	def get_target(self):
		target = Component._gtk_find_component(self._gtk_outer_widget.get_focus())
		return target or self

	def _screen_rect(self):
		w = gdk.screen_width()
		h = gdk.screen_height()
		return (0, 0, w, h)
	
	def _gtk_menubar_height(self):
		mb = self._gtk_menubar
		if mb:
			h = mb.size_request()[1]
		else:
			h = 0
		#print "Window._gtk_menubar_height -->", h ###
		return h
	
	def _gtk_delete_event(self, event):
		try:
			self.close_cmd()
		except:
			sys.excepthook(*sys.exc_info())
		return 1
	
	def _gtk_update_menubar(self):
		#
		#  Update the contents of the menubar after either the application
		#  menu list or this window's menu list has changed. We only add
		#  the menu titles at this stage; the menus themselves are attached
		#  during menu setup. We also attach the accel groups associated
		#  with the new menus.
		#
		#  Things would be simpler if we could attach the menus here,
		#  but attempting to share menus between menubar items provokes
		#  a warning from Gtk, even though it otherwise appears to work.
		#
		gtk_menubar = self._gtk_menubar
		gtk_window = self._gtk_outer_widget
		#  Remove old accel groups
		for menu in self._all_menus:
			gtk_window.remove_accel_group(menu._gtk_accel_group)
		#  Detach any existing menus and remove old menu titles
		if gtk_menubar:
			for gtk_menubar_item in gtk_menubar.get_children():
				gtk_menubar_item.remove_submenu()
				gtk_menubar_item.destroy()
		#  Install new menu list
		#all_menus = application().menus + self.menus
		all_menus = application()._effective_menus_for_window(self)
		self._all_menus = all_menus
		#  Create new menu titles and attach accel groups
		for menu in all_menus:
			if gtk_menubar:
				gtk_menubar_item = gtk.MenuItem(menu._title)
				gtk_menubar_item.show()
				gtk_menubar.append(gtk_menubar_item)
			gtk_window.add_accel_group(menu._gtk_accel_group)
		self._need_menubar_update = 0
	
	def _gtk_menubar_button_press_event(self, event):
		#  A button press has occurred in the menu bar. Before pulling
		#  down the menu, perform menu setup and attach the menus to
		#  the menubar items.
		self._gtk_menu_setup()
		for (gtk_menubar_item, menu) in \
			zip(self._gtk_menubar.get_children(), self._all_menus):
				gtk_menu = menu._gtk_menu
				attached_widget = gtk_menu.get_attach_widget()
				if attached_widget and attached_widget is not gtk_menubar_item:
					attached_widget.remove_submenu()
				gtk_menubar_item.set_submenu(gtk_menu)
	
	def _gtk_key_press_event(self, gtk_event):
		#  Intercept key presses with the Control key down and update
		#  menus, in case this is a keyboard equivalent for a menu command.
		if gtk_event.state & gdk.CONTROL_MASK:
			#print "Window._gtk_key_press_event: doing menu setup"
			self._gtk_menu_setup()
			#  It appears that GtkWindow caches accelerators, and updates
			#  the cache in an idle task after accelerators change. This
			#  would be too late for us, so we force it to be done now.
			self._gtk_outer_widget.emit("keys-changed")
			#print "Window._gtk_key_press_event: done menu setup"
	
	def _gtk_menu_setup(self):
		application()._perform_menu_setup(self._all_menus)

	def _default_key_event(self, event):
		#print "Window._default_key_event:", event
		self.pass_event_to_next_handler(event)
		if event._originator is self:
			event._not_handled = True

	def dispatch(self, message, *args):
		self.target.handle(message, *args)


_gtk_menubar_height = None

def _gtk_find_menubar_height():
	global _gtk_menubar_height
	if _gtk_menubar_height is None:
		print "Windows: Finding menubar height"
		item = gtk.MenuItem("X")
		bar = gtk.MenuBar()
		bar.append(item)
		bar.show_all()
		w, h = bar.size_request()
		_gtk_menubar_height = h
		print "...done"
	return _gtk_menubar_height

export(Window)
