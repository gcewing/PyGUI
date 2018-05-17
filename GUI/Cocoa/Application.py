#------------------------------------------------------------------------------
#
#		Python GUI - Application class - PyObjC
#
#------------------------------------------------------------------------------

import os, sys, traceback
import objc
from Foundation import NSObject, NSBundle, NSDefaultRunLoopMode, NSData, NSDate
import AppKit
from AppKit import NSApplication, NSResponder, NSScreen, NSMenu, NSMenuItem, \
	NSKeyDown, NSKeyUp, NSMouseMoved, NSLeftMouseDown, NSSystemDefined, \
	NSCommandKeyMask, NSPasteboard, NSStringPboardType, NSModalPanelRunLoopMode
NSAnyEventMask = 0xffffffff
from GUI import Globals, GApplications
from GUI import application, export
from GUI.GApplications import Application as GApplication
from GUI import Event

#------------------------------------------------------------------------------

Globals.ns_screen_height = None
Globals.ns_last_mouse_moved_event = None
Globals.pending_exception = None
Globals.ns_application = None

ns_distant_future = NSDate.distantFuture()

#------------------------------------------------------------------------------

class Application(GApplication):
	#  _ns_app          _PyGui_NSApplication
	#  _ns_pasteboard   NSPasteboard
	#  _ns_key_window   Window
	
	_ns_menubar_update_pending = False
	_ns_files_opened = False
	_ns_using_clargs = False
	_ns_menus_updated = False

	def __init__(self, **kwds):
		self._ns_app = Globals.ns_application
		self._ns_app.pygui_app = self
		self._ns_pasteboard = NSPasteboard.generalPasteboard()
		self._ns_key_window = None
		GApplication.__init__(self, **kwds)
		self.ns_init_application_name()
	
	def destroy(self):
		del self.menus[:]
		import Windows
		Windows._ns_zombie_window = None
		self._ns_app.pygui_app = None
		self._ns_app = None
		self._ns_pasteboard = None
		GApplication.destroy(self)
	
	def set_menus(self, menu_list):
		GApplication.set_menus(self, menu_list)
		self._update_menubar()
	
	def _update_menubar(self):
		ns_app = self._ns_app
		ns_menubar = NSMenu.alloc().initWithTitle_("")
		menu_list = self._effective_menus()
		for menu in menu_list:
			ns_item = NSMenuItem.alloc()
			ns_item.initWithTitle_action_keyEquivalent_(menu.title, '', "")
			ns_menubar.addItem_(ns_item)
			ns_menu = menu._ns_menu
			#  An NSMenu can only be a submenu of one menu at a time, so
			#  remove it from the old menubar if necessary.
			old_supermenu = ns_menu.supermenu()
			if old_supermenu:
				i = old_supermenu.indexOfItemWithSubmenu_(ns_menu)
				old_supermenu.removeItemAtIndex_(i)
			ns_menubar.setSubmenu_forItem_(ns_menu, ns_item)
		# The menu you pass to setAppleMenu_ must *also* be a member of the
		# main menu.
		ns_app.setMainMenu_(ns_menubar)
		if menu_list:
			ns_app_menu = menu_list[0]._ns_menu
			ns_app.setAppleMenu_(ns_app_menu)

	def handle_next_event(self, modal_window = None):
		ns_app = self._ns_app
		if modal_window:
			ns_mode = NSModalPanelRunLoopMode
			ns_modal_window = modal_window._ns_window
		else:
			ns_mode = NSDefaultRunLoopMode
			ns_modal_window = None
		ns_event = ns_app.nextEventMatchingMask_untilDate_inMode_dequeue_(
			NSAnyEventMask, ns_distant_future, ns_mode, True)
		if ns_event:
			ns_window = ns_event.window()
			if not ns_window or not ns_modal_window or ns_window == ns_modal_window:
				ns_app.sendEvent_(ns_event)
	
	def get_target_window(self):
		#  NSApplication.keyWindow() isn't reliable enough. We keep track
		#  of the key window ourselves.
		return self._ns_key_window

	def zero_windows_allowed(self):
		return 1
	
	def query_clipboard(self):
		pb = self._ns_pasteboard
		pb_types = pb.types()
		return NSStringPboardType in pb_types
	
	def get_clipboard(self):
		pb = self._ns_pasteboard
		ns_data = pb.dataForType_(NSStringPboardType)
		if ns_data:
			return ns_data.bytes().tobytes()
	
	def set_clipboard(self, data):
		ns_data = NSData.dataWithBytes_length_(data, len(data))
		pb = self._ns_pasteboard
		pb.clearContents()
		pb.setData_forType_(ns_data, NSStringPboardType)
	
	def setup_menus(self, m):
		m.hide_app_cmd.enabled = True
		m.hide_other_apps_cmd.enabled = True
		m.show_all_apps_cmd.enabled = True
		if not self._ns_app.modalWindow():
			GApplication.setup_menus(self, m)
	
	def process_args(self, args):
		#  Note: When using py2app, argv_emulation should be disabled.
		if args and args[0].startswith("-psn"):
			# Launched from MacOSX Finder -- wait for file open/app launch messages
			pass
		else:
			# Not launched from Finder or using argv emulation
			self._ns_using_clargs = True
			GApplication.process_args(self, args)

	def run(self, fast_exit = True):
		try:
			GApplication.run(self)
		except (KeyboardInterrupt, SystemExit):
			pass
		except:
			traceback.print_exc()
		#  A py2app bundled application seems to crash on exit if we don't
		#  bail out really quickly here (Python 2.3, PyObjC 1.3.7, py2app 0.2.1,
		#  MacOSX 10.4.4)
		if fast_exit:
			os._exit(0)

	def event_loop(self):
		self._ns_app.run()
	
	def _quit(self):
		self._quit_flag = True
		self._ns_app.stop_(self._ns_app)

	def hide_app_cmd(self):
		self._ns_app.hide_(self)

	def hide_other_apps_cmd(self):
		self._ns_app.hideOtherApplications_(self)

	def show_all_apps_cmd(self):
		self._ns_app.unhideAllApplications_(self)

	def ns_process_key_event(self, ns_event):
		#  Perform menu setup before command-key events.
		#  Send non-command key events to associated window if any,
		#  otherwise pass them to the pygui application. This is necessary
		#  because otherwise there is no way of receiving key events when
		#  there are no windows.
		if ns_event.modifierFlags() & NSCommandKeyMask:
			NSApplication.sendEvent_(self._ns_app, ns_event)
		else:
			ns_window = ns_event.window()
			if ns_window:
				ns_window.sendEvent_(ns_event)
			else:
				event = Event(ns_event)
				self.handle(event.kind, event)
	
	def ns_menu_needs_update(self, ns_menu):
		try:
			if not self._ns_menus_updated:
				self._perform_menu_setup()
				self._ns_menus_updated = True
		except Exception:
			self.report_exception()

	def ns_init_application_name(self):
		#  Arrange for the application name to be used as the title
		#  of the application menu.
		ns_bundle = NSBundle.mainBundle()
		if ns_bundle:
			ns_info = ns_bundle.localizedInfoDictionary()
			if not ns_info:
				ns_info = ns_bundle.infoDictionary()
			if ns_info:
				if ns_info['CFBundleName'] == "Python":
					#print "GUI.Application: NSBundle infoDictionary =", ns_info ###
					ns_info['CFBundleName'] = Globals.application_name
				return
	
#------------------------------------------------------------------------------

_ns_key_event_mask = AppKit.NSKeyDownMask | AppKit.NSKeyUpMask

#------------------------------------------------------------------------------

class _PyGui_NSApplication(NSApplication):

	pygui_app = None

	def sendEvent_(self, ns_event):
		#  Perform special processing of key events.
		#  Perform menu setup when menu bar is clicked.
		#  Remember the most recent mouse-moved event to use as the
		#  location of event types which do not have a location themselves.
		if Globals.pending_exception:
			raise_pending_exception()
		ns_type = ns_event.type()
		self.pygui_app._ns_menus_updated = False
		if (1 << ns_type) & _ns_key_event_mask:
			self.pygui_app.ns_process_key_event(ns_event)
		else:
			if ns_type == NSMouseMoved:
				Globals.ns_last_mouse_moved_event = ns_event
				ns_window = ns_event.window()
				if ns_window:
					ns_view = ns_window.contentView().hitTest_(ns_event.locationInWindow())
					if ns_view:
						ns_view.mouseMoved_(ns_event)
			else:
				NSApplication.sendEvent_(self, ns_event)

	def menuNeedsUpdate_(self, ns_menu):
		self.pygui_app.ns_menu_needs_update(ns_menu)

	def menuSelection_(self, ns_menu_item):
		try:
			command = ns_menu_item.representedObject()
			index = ns_menu_item.tag()
			if index >= 0:
				dispatch_to_app(self, command, index)
			else:
				dispatch_to_app(self, command)
		except:
			self.pygui_app.report_error()
	
	def validateMenuItem_(self, item):
		return False
	
	def undo_(self, sender):
		dispatch_to_app(self, 'undo_cmd')

	def redo_(self, sender):
		dispatch_to_app(self, 'redo_cmd')

	def cut_(self, sender):
		dispatch_to_app(self, 'cut_cmd')

	def copy_(self, sender):
		dispatch_to_app(self, 'copy_cmd')

	def paste_(self, sender):
		dispatch_to_app(self, 'paste_cmd')

	def clear_(self, sender):
		dispatch_to_app(self, 'clear_cmd')

	def selectAll_(self, sender):
		dispatch_to_app(self, 'select_all_cmd')

	def application_openFile_(self, ns_app, path):
		app = self.pygui_app
		if app._ns_using_clargs:
			return True
		# Bizarrely, argv[0] gets passed to application_openFile_ under
		# some circumstances. We don't want to try to open it!
		if path == sys.argv[0]:
			return True
		app._ns_files_opened = True
		try:
			app.open_path(path)
			return True
		except Exception, e:
			app.report_error()
			return False
	
	def applicationDidFinishLaunching_(self, notification):
		app = self.pygui_app
		if app._ns_using_clargs:
			return
		try:
			if not app._ns_files_opened:
				app.open_app()
		except Exception, e:
			app.report_error()
			return False

export(Application)

#------------------------------------------------------------------------------

def raise_pending_exception():
	exc_type, exc_value, exc_tb = Globals.pending_exception
	Globals.pending_exception = None
	raise exc_type, exc_value, exc_tb

def create_ns_application():
	ns_app = _PyGui_NSApplication.sharedApplication()
	ns_app.setDelegate_(ns_app)
	Globals.ns_application = ns_app

def dispatch_to_app(ns_app, *args):
	app = ns_app.pygui_app
	if app:
		app.dispatch(*args)

Globals.ns_screen_height = NSScreen.mainScreen().frame().size.height

create_ns_application()

#------------------------------------------------------------------------------

# Disable this for now, since MachSignals.signal segfaults. :-(
#
#def _install_sigint_handler():
#		print "_install_sigint_handler" ###
#		from Foundation import NSRunLoop
#		run_loop = NSRunLoop.currentRunLoop()
#		if not run_loop:
#			print "...No current run loop" ###
#			sys.exit(1) ###
#		MachSignals.signal(signal.SIGINT, _sigint_handler)
#		#from PyObjCTools.AppHelper import installMachInterrupt
#		#installMachInterrupt()
#		print "...done" ###
#
#def _sigint_handler(signum):
#	print "_sigint_handler" ###
#	raise KeyboardInterrupt

#def _install_sigint_handler():
#	import signal
#	signal.signal(signal.SIGINT, _raise_keyboard_interrupt)
#
#def _raise_keyboard_interrupt(signum, frame):
#	raise KeyboardInterrupt

#_install_sigint_handler()
