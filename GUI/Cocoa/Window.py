#------------------------------------------------------------------------------
#
#   Python GUI - Windows - PyObjC version
#
#------------------------------------------------------------------------------

from Foundation import NSRect, NSPoint, NSSize, NSObject
import AppKit
from AppKit import NSWindow, NSScreen, NSTextView, NSMenu
from GUI import export
from GUI import Globals
from GUI.Utils import NSMultiClass, PyGUI_NS_EventHandler, PyGUI_Flipped_NSView
from GUI import application
from GUI import Event
from GUI.GWindows import Window as GWindow

_default_options_for_style = {
	'standard':
		{'movable': 1, 'closable': 1, 'hidable': 1, 'resizable': 1},
	'nonmodal_dialog':
		{'movable': 1, 'closable': 0, 'hidable': 1, 'resizable': 0},
	'modal_dialog':
		{'movable': 1, 'closable': 0, 'hidable': 0, 'resizable': 0},
	'alert':
		{'movable': 1, 'closable': 0, 'hidable': 0, 'resizable': 0},
	'fullscreen':
		{'movable': 0, 'closable': 0, 'hidable': 0, 'resizable': 0},
		#{'movable': 1, 'closable': 1, 'hidable': 1, 'resizable': 1},
}

#------------------------------------------------------------------------------

class Window(GWindow):
	#  _ns_window        PyGUI_NSWindow
	#  _ns_style_mask    int

	_ns_last_target = None

	def __init__(self, style = 'standard', zoomable = None, **kwds):
		# We ignore zoomable, since it's the same as resizable.
		self._style = style
		options = dict(_default_options_for_style[style])
		for option in ['movable', 'closable', 'hidable', 'resizable']:
			if option in kwds:
				options[option] = kwds.pop(option)
		self._ns_style_mask = self._ns_window_style_mask(**options)
		if style == 'fullscreen':
			ns_rect = NSScreen.mainScreen().frame()
		else:
			ns_rect = NSRect(NSPoint(0, 0), NSSize(self._default_width, self._default_height))
		ns_window = PyGUI_NSWindow.alloc()
		ns_window.initWithContentRect_styleMask_backing_defer_(
			ns_rect, self._ns_style_mask, AppKit.NSBackingStoreBuffered, True)
		ns_content = PyGUI_NS_ContentView.alloc()
		ns_content.initWithFrame_(NSRect(NSPoint(0, 0), NSSize(0, 0)))
		ns_content.pygui_component = self
		ns_window.setContentView_(ns_content)
		ns_window.setAcceptsMouseMovedEvents_(True)
		ns_window.setDelegate_(ns_window)
		ns_window.pygui_component = self
		self._ns_window = ns_window
		GWindow.__init__(self, style = style, closable = options['closable'],
			_ns_view = ns_window.contentView(), _ns_responder = ns_window,
			_ns_set_autoresizing_mask = False,
			**kwds)
	
	def _ns_window_style_mask(self, movable, closable, hidable, resizable):
		if movable or closable or hidable or resizable:
			mask = AppKit.NSTitledWindowMask
			if closable:
				mask |= AppKit.NSClosableWindowMask
			if hidable:
				mask |= AppKit.NSMiniaturizableWindowMask
			if resizable:
				mask |= AppKit.NSResizableWindowMask
		else:
			mask = AppKit.NSBorderlessWindowMask
		return mask

	def destroy(self):
		#print "Window.destroy:", self ###
		self.hide()
		app = application()
		if app._ns_key_window is self:
			app._ns_key_window = None
		GWindow.destroy(self)
		#  We can't drop all references to the NSWindow yet, because this method
		#  can be called from its windowShouldClose: method, and allowing an
		#  NSWindow to be released while executing one of its own methods seems
		#  to be a very bad idea (Cocoa hangs). So we hide the NSWindow and store
		#  a reference to it in a global. It will be released the next time a
		#  window is closed and the global is re-used.
		global _ns_zombie_window
		_ns_zombie_window = self._ns_window
		self._ns_window.pygui_component = None
		#self._ns_window = None

	def get_bounds(self):
		ns_window = self._ns_window
		ns_frame = ns_window.frame()
		(l, y), (w, h) = ns_window.contentRectForFrameRect_styleMask_(
			ns_frame, self._ns_style_mask)
		b = Globals.ns_screen_height - y
		result = (l, b - h, l + w, b)
		return result
	
	def set_bounds(self, (l, t, r, b)):
		y = Globals.ns_screen_height - b
		ns_rect = NSRect(NSPoint(l, y), NSSize(r - l, b - t))
		ns_window = self._ns_window
		ns_frame = ns_window.frameRectForContentRect_styleMask_(
			ns_rect, self._ns_style_mask)
		ns_window.setFrame_display_(ns_frame, False)

	def get_title(self):
		return self._ns_window.title()
	
	def set_title(self, v):
		self._ns_window.setTitle_(v)

	def get_visible(self):
		return self._ns_window.isVisible()
	
	def set_visible(self, v):
		#  At some mysterious time between creating a window and showing
		#  it for the first time, Cocoa adjusts its position so that it
		#  doesn't extend above the menu bar. This is a nuisance for
		#  our fullscreen windows, so we need to readjust the position
		#  before showing.
		if v:
			if self._style == 'fullscreen':
				self._ns_window.setFrameOrigin_(NSPoint(0, 0))
			self._ns_window.orderFront_(None)
		else:
			self._ns_window.orderOut_(None)
	
	def _show(self):
		self.visible = True
		self._ns_window.makeKeyWindow()
	
	def get_target(self):
		ns_window = self._ns_window
		ns_view = ns_window.firstResponder()
		while ns_view and ns_view is not ns_window:
			component = Globals._ns_view_to_component.get(ns_view)
			if component:
				return component
			ns_view = ns_view.superview()
		return self
	
	def center(self):
		self._ns_window.center()
	
	def _stagger(self):
		key_win = application()._ns_key_window
		if key_win:
			(x, y), (w, h) = key_win._ns_window.frame()
			p = self._ns_window.cascadeTopLeftFromPoint_(NSPoint(x, y + h))
			self._ns_window.setFrameTopLeftPoint_(p)
		else:
			(x, y), (w, h) = NSScreen.mainScreen().visibleFrame()
			ns_vis_topleft = NSPoint(x, y + h)
			self._ns_window.setFrameTopLeftPoint_(ns_vis_topleft)

	def _document_needs_saving(self, state):
		self._ns_window.setDocumentEdited_(state)
	
#------------------------------------------------------------------------------

class PyGUI_NSWindow(NSWindow, PyGUI_NS_EventHandler):
	#  pygui_component   Window
	#  resize_delta      point or None
	
	__metaclass__ = NSMultiClass
	__slots__ = ['pygui_component', 'resize_delta', 'pygui_field_editor']
	
#	pygui_component = None
#	resize_delta = None
#	pygui_field_editor = None
	
	def _ns_event_position(self, ns_event):
		return ns_event.locationInWindow()

	def windowShouldClose_(self, sender):
		#  We use this to detect when the Aqua window closing button
		#  is pressed, and do the closing ourselves.
		self.pygui_component.close_cmd()
		return False
	
	#  The NSWindow is made its own delegate.

	def windowWillResize_toSize_(self, ns_win, new_ns_size):
		w0, h0 = self.frame().size
		w1, h1 = new_ns_size
		self.resize_delta = (w1 - w0, h1 - h0)
		return new_ns_size
	
	def windowDidResize_(self, notification):
		delta = getattr(self, 'resize_delta', None)
		if delta:
			self.pygui_component._resized(delta)
			self.resize_delta = None

	def windowDidBecomeKey_(self, notification):
		app = application()
		app._ns_key_window = self.pygui_component
		app._update_menubar()

	def windowDidResignKey_(self, notification):
		app = application()
		app._ns_key_window = None
		app._update_menubar()
	
	def windowWillReturnFieldEditor_toObject_(self, ns_window, ns_obj):
		#  Return special field editor for newline handling in text fields.
		#print "Window: Field editor requested for", object.__repr__(ns_obj) ###
		#editor = self.pygui_field_editor
		#if not editor:
		try:
			editor = self.pygui_field_editor
		except AttributeError:
			#print "...creating new field editor" ###
			editor = PyGUI_FieldEditor.alloc().initWithFrame_(
				NSRect(NSPoint(0, 0), NSSize(0, 0)))
			editor.setFieldEditor_(True)
			editor.setDrawsBackground_(False)
			self.pygui_field_editor = editor
		return editor
	
	#  Need the following two methods so that a fullscreen window can become
	#  the main window. Otherwise it can't, because it has no title bar.

	def canBecomeKeyWindow(self):
		return self.isVisible()
	
	def canBecomeMainWindow(self):
		#print "PyGUI_NSWindow.canBecomeMainWindow"
		return self.isVisible()
	
	def windowDidBecomeMain_(self, notification):
		#print "PyGUI_NSWindow.windowDidBecomeMain_:",  self.pygui_component.title ###
		comp = self.pygui_component
		if comp and comp._style == 'fullscreen':
			#print "...hiding menu bar" ###
			NSMenu.setMenuBarVisible_(False)
			#self.setFrameOrigin_(NSPoint(0, 0))

	def windowDidResignMain_(self, notification):
		#print "PyGUI_NSWindow.windowDidResignMain_:",  self.pygui_component.title ###
		comp = self.pygui_component
		if comp and comp._style == 'fullscreen':
			#print "...showing menu bar" ###
			NSMenu.setMenuBarVisible_(True)

#------------------------------------------------------------------------------

class PyGUI_NS_ContentView(PyGUI_Flipped_NSView, PyGUI_NS_EventHandler):
	#  pygui_component   Window

	__metaclass__ = NSMultiClass
	__slots__ = ['pygui_component']

	def acceptsFirstResponder(self):
		return False

#------------------------------------------------------------------------------

class PyGUI_FieldEditorBase(NSTextView):
	#  Special field editor for use by TextFields. Intercepts
	#  return key events and handles them our own way.
	
	#ns_base_class = NSTextView

	def keyDown_(self, ns_event):
		#print "PyGUI_FieldEditorBase.keyDown_ for", self.pygui_component ###
		if ns_event.characters() == "\r":
			if self.pygui_component._multiline:
				self.insertText_("\n")
				return
		NSTextView.keyDown_(self, ns_event)

#------------------------------------------------------------------------------

class PyGUI_FieldEditor(PyGUI_FieldEditorBase, PyGUI_NS_EventHandler):
	
	__metaclass__ = NSMultiClass
	
# 	def resignFirstResponder(self):
# 		ok = PyGUI_FieldEditorBase.resignFirstResponder(self)
# 		if ok:
# 		    component = self.pygui_component
# 		    if component:
# 		        component.untargeted()
# 		return ok

	def get_pygui_component(self):
		sv = self.superview()
		if sv:
			pygui_nstextfield = sv.superview()
			if pygui_nstextfield:
				return pygui_nstextfield.pygui_component
	
	pygui_component = property(get_pygui_component)

export(Window)
