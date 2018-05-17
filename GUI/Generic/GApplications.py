#
#		Python GUI - Application class - Generic
#

import os, sys, traceback
from GUI import Globals
from GUI.Properties import Properties, overridable_property
from GUI import MessageHandler
from GUI.Exceptions import Cancel, UnimplementedMethod, UsageError, \
	ApplicationError #, Quit
from GUI.StdMenus import basic_menus
from GUI.GMenus import MenuState
from GUI.Files import FileRef
from GUI.Printing import PageSetup, present_page_setup_dialog

class Application(Properties, MessageHandler):
	"""The user should create exactly one Application object,
	or subclass thereof. It implements the main event loop
	and other application-wide behaviour."""
	
	_windows = None				# List of all existing Windows
	_documents = None			# List of all existing Documents
	_menus = None					# Menus to appear in all Windows
	_clipboard = None
	_save_file_type = None
	_exit_event_loop_flag = False
	_last_directory = None

	windows = overridable_property('windows',
		"""A list of all existing Windows.""")

	documents = overridable_property('documents',
		"""A list of all existing documents.""")

	menus = overridable_property('menus',
		"""A list of Menus that are to be available from all Windows.""")
	
	open_file_types = overridable_property('open_file_types',
		"""List of FileTypes openable by the default Open... command.""")
	
	save_file_type = overridable_property('save_file_type',
		"""Default FileType for Documents that do not specify their own.""")
	
	file_type = overridable_property('file_type',
		"""Write only. Sets open_file_types and save_file_type.""")
	
	target = overridable_property('target',
		"""Current target for key events and menu messages.""")

	target_window = overridable_property('target_window',
		"""Window containing the current target, or None if there are no windows.""")

	page_setup = overridable_property('page_setup',
		"""Default PageSetup instance.""")

	def __init__(self, title = None):
		if Globals._application is not None:
			raise UsageError("More than one Application instance created")
		if title:
			Globals.application_name = title
		self._open_file_types = []
		self._windows = []
		self._documents = []
		self._update_list = []
		self._idle_tasks = []
		self._page_setup = None
		Globals._application = self
		self._quit_flag = False
	
	def destroy(self):
		Globals._application = None

	#
	#		Constants
	#

#	def get_std_menus(self):
#		"""Returns a list of Menus containing the standard
#		framework-defined menu commands in their standard 
#		positions."""
#		return basic_menus()
#	
#	std_menus = property(get_std_menus)

	#
	#		Properties
	#

	def get_windows(self):
		return self._windows
	
	def get_documents(self):
		return self._documents
	
	def get_menus(self):
		menus = self._menus
		if menus is None:
			menus = []
		return menus

	def set_menus(self, menus):
		self._menus = menus

	def get_open_file_types(self):
		return self._open_file_types
	
	def set_open_file_types(self, x):
		self._open_file_types = x
	
	def get_save_file_type(self):
		return self._save_file_type
	
	def set_save_file_type(self, x):
		self._save_file_type = x
	
	def set_file_type(self, x):
		self._open_file_types = [x]
		self._save_file_type = x
	
	def get_page_setup(self):
		#  This property is initialised lazily, because on Windows it turn out
		#  that calling PageSetupDlg() before the application's first window is
		#  created causes the app not to be brought to the foreground initially.
		ps = self._page_setup
		if not ps:
			ps = PageSetup()
			self._page_setup = ps
		return ps
	
	def set_page_setup(self, x):
		self._page_setup = x

	#
	#		Event loop
	#

	def run(self):
		"""The main event loop. Runs until _quit() is called, or
		KeyboardInterrupt or SystemExit is raised."""
		#  Implementations may override this together with _quit() to use
		#  a different means of causing the main event loop to exit.
		self.process_args(sys.argv[1:])
		if self._menus is None:
			self.menus = basic_menus()
		while not self._quit_flag:
			try:
				self.event_loop()
			#except (KeyboardInterrupt, Quit), e:
			except KeyboardInterrupt:
				return
			except SystemExit:
				raise
			except:
				self.report_error()
	
	def _quit(self):
		#  Causes the main event loop to exit.
		self._quit_flag = True
		self._exit_event_loop()
	
	def event_loop(self):
		"""Loop reading and handling events until exit_event_loop() is called."""
		#  Implementations may override this together with exit_event_loop() to
		#  implement non-modal event loops in a different way.
		self._event_loop(None)
	
	def _event_loop(self, modal_window):
		#  Generic modal and non-modal event loop.
		#  Loop reading and handling events for the given window, or for all
		#  windows if window is None, until exit_event_loop() is called.
		#  Enabled application-wide menu items should be selectable in any case.
		#  If an exception other than Cancel is raised, it should either be
		#  reported using report_error() or propagated. Implementations may
		#  override this together with _exit_event_loop() if handling events
		#  individually is not desirable.
		save = self._exit_event_loop_flag
		self._exit_event_loop_flag = False
		try:
			while not self._exit_event_loop_flag:
				try:
					self.handle_next_event(modal_window)
				except Cancel:
					pass
		finally:
			self._exit_event_loop_flag = save
	
	def exit_event_loop(self):
		"""Cause the current call to event_loop() or modal_event_loop()
		to exit."""
		self._exit_event_loop()
	
	def _exit_event_loop(self):
		#  Exit the generic _event_loop implementation.
		self._exit_event_loop_flag = True
	
#	def event_loop_until(self, exit):
#		"""Loop reading and handling events until exit() returns
#		true, _quit_flag is set or an exception other than Cancel
#		is raised."""
#		while not exit() and not self._quit_flag:
#			try:
#				self.handle_next_event()
#			except Cancel:
#				pass

#	def handle_events(self):
#		"""Handle events until an exception occurs. Waits for at least one event;
#		may handle more, at the discretion of the implementation."""
#		self.handle_next_event()
	
	def handle_next_event(self, modal_window):
		#  Wait for the next event to arrive and handle it. Transparently handles 
		#  any internal events such as window updates, etc., and executes any idle
		#  tasks that become due while waiting for an event. If modal_window is
		#  not None, restrict interaction to that window (but allow use of enabled
		#  application-wide menu items).
		#
		#  This only needs to be implemented if the generic _event_loop() is being
		#  used.
		raise UnimplementedMethod(self, "handle_next_event")
	
	#
	#		Menu commands
	#

	def setup_menus(self, m):
		m.new_cmd.enabled = 1
		m.open_cmd.enabled = 1
		m.page_setup_cmd.enabled = 1
		m.quit_cmd.enabled = 1

	def new_cmd(self):
		"Handle the New menu command."
		doc = self.make_new_document()
		if not doc:
			raise UsageError(
				"Application.make_document(None) did not return a Document.")
		doc.new_contents()
		self.make_window(doc)

	def open_cmd(self):
		"Handle the Open... menu command."
		from FileDialogs import request_old_file
		dir = self.get_default_open_directory()
		fileref = request_old_file(default_dir = dir,
			file_types = self._open_file_types)
		if fileref:
			self.open_fileref(fileref)
		else:
			raise Cancel
	
	def get_default_open_directory(self):
		"""Called by the default implementation of open_cmd() to find an initial
		directory for request_old_file(). Should return a DirRef or FileRef, or
		None if there is no preferred location. By default it returns the last
		directory in which a document was opened or saved during this session,
		if any."""
		return self._last_directory
	
	def page_setup_cmd(self):
		present_page_setup_dialog(self.page_setup)

	def quit_cmd(self):
		"""Handle the Quit menu command."""
		while self._documents:
			self._documents[0].close_cmd()
		windows = self._windows
		while windows:
			window = windows[-1]
			window.destroy()
			assert not (windows and windows[-1] is window), \
				"%r failed to remove itself from application on destruction" % window
		self._quit()

	#
	#   Opening files
	#
	
	def process_args(self, args):
		"""Process command line arguments. Called by run() when the application
		is starting up."""
		if not args:
			self.open_app()
		else:
			for arg in args:
				if os.path.exists(arg):
					arg = os.path.abspath(arg)
					self.open_path(arg)
	
	def open_app(self):
		"""Called by run() when the application is opened with no arguments."""
		pass
	
	def open_path(self, path):
		"""Open document specified by a pathname. Called for each command line
		argument when the application is starting up."""
		self.open_fileref(FileRef(path = path))
	
	def open_fileref(self, fileref):
		"""Open document specified by a FileRef."""
		doc = self.make_file_document(fileref)
		if not doc:
			raise ApplicationError("The file '%s' is not recognised by %s." % (
				fileref.name, Globals.application_name))
		doc.set_file(fileref)
		try:
			doc.read()
		except EnvironmentError, e:
			raise ApplicationError("Unable to open '%s'." % fileref.name, e)
		self.make_window(doc)

	#
	#   Message dispatching
	#
	
#	def dispatch(self, message, *args):
#		target_window = self._find_target_window()
#		if target_window:
#			target_window.dispatch(message, *args)
#		else:
#			self.handle(message, *args)
	
	def dispatch(self, message, *args):
		self.target.handle(message, *args)
	
	def dispatch_menu_command(self, command):
		if isinstance(command, tuple):
			name, index = command
			self.dispatch(name, index)
		else:
			self.dispatch(command)
	
	def get_target(self):
		#  Implementations may override this to locate the target in a
		#  different way if they choose not to implement the Window.target
		#  property. Should return self if no other target can be found.
		window = self.target_window
		if window:
			return window.target
		else:
			return self

	def get_target_window(self):
		"""Return the window to which messages should be dispatched, or None."""
		raise NotImplementedError
	
	#
	#		Abstract
	#

	def make_new_document(self):
		"""Create a new Document object of the appropriate 
		class in response to a New command."""
		return self.make_document(None)

	def make_file_document(self, fileref):
		"""Create a new Document object of the appropriate 
		class for the given FileRef."""
		return self.make_document(fileref)
	
	def make_document(self, fileref):
		"""Should create a new Document object of the appropriate 
		class for the given FileRef, or if FileRef is None, a new
		empty Document of the appropriate class for the New command."""
		return None

	def make_window(self, document):
		"""Should create a Window set up appropriately for viewing
		the given Document."""
		raise UnimplementedMethod(self, 'make_window')

	#
	#		Clipboard
	#

	def query_clipboard(self):
		"Tests whether the clipboard contains any data."
		return not not self._clipboard
	
	def get_clipboard(self):
		return self._clipboard

	def set_clipboard(self, x):
		self._clipboard = x
	
	#
	#   Window list management
	#
	
	def _add_window(self, window):
		if window not in self._windows:
			self._windows.append(window)
	
	def _remove_window(self, window):
		if window in self._windows:
			self._windows.remove(window)

	#
	#   Document list management
	#
	
	def _add_document(self, doc):
		if doc not in self._documents:
			self._documents.append(doc)
	
	def _remove_document(self, doc):
		if doc in self._documents:
			self._documents.remove(doc)
	
	#
	#   Exception reporting
	#
	
	def report_error(self):
		"""Display an appropriate error message for the most recent
		exception caught."""
		try:
			raise
		except Cancel:
			pass
		except ApplicationError, e:
			from GUI.Alerts import stop_alert
			stop_alert(str(e))
		except:
			self.report_exception()

	def report_exception(self):
		"""Display an alert box describing the most recent exception, and
		giving the options Continue, Traceback or Abort. Traceback displays
		a traceback and continues; Abort raises SystemExit."""
		try:
			exc_type, exc_val, exc_tb = sys.exc_info()
			exc_desc = "%s: %s" % (exc_type.__name__, exc_val)
			self.print_traceback(exc_desc, exc_tb)
			from GUI.Alerts import alert3
			message = "Sorry, something went wrong."
			result = alert3('stop', "%s\n\n%s" % (message, exc_desc),
				"Continue", "Abort", "Traceback",
				default = 1, cancel = None, width = 450, lines = 5)
			if result == 1: # Continue
				return
			elif result == -1: # Traceback
				self.display_traceback(exc_desc, exc_tb)
				return
			else: # Abort
				raise SystemExit
		except (KeyboardInterrupt, SystemExit):
			os._exit(1)
		except:
			print >>sys.stderr, "---------- Exception while reporting exception ----------"
			traceback.print_exc()
			print >>sys.stderr, "------------------ Original exception -------------------"
			traceback.print_exception(exc_type, exc_val, exc_tb)
			#os._exit(1)
	
	def display_traceback(self, exc_desc, exc_tb):
		"""Display an exception description and traceback.
		TODO: display this in a scrolling window."""
		self.print_traceback(exc_desc, exc_tb)

	def print_traceback(self, exc_desc, exc_tb):
		"""Print exception description and traceback to standard error."""
		import traceback
		sys.stderr.write("\nTraceback (most recent call last):\n")
		traceback.print_tb(exc_tb)
		sys.stderr.write("%s\n\n" % exc_desc)

	#
	#   Other
	#
	
	def zero_windows_allowed(self):
		"""Platforms should implement this to return false if there
		must be at least one window open at all times. Returning false 
		here forces the Quit command to be used instead of Close when 
		there is only one window open."""
		# TODO: Move this somewhere more global.
		raise UnimplementedMethod(self, 'zero_windows_allowed')
	
	def _perform_menu_setup(self, menus = None):
		"""Given a list of Menu objects, perform menu setup processing
		and update associated platform menus ready for popping up or
		pulling down."""
		if menus is None:
			menus = self._effective_menus()
		menu_state = MenuState(menus)
		menu_state.reset()
		self._dispatch_menu_setup(menu_state)
		for menu in menus:
			menu._update_platform_menu()
	
	def _dispatch_menu_setup(self, menu_state):
		self.dispatch('_setup_menus', menu_state)

	def _effective_menus(self):
		"""Return a list of the menus in effect for the currently active
		window, including both application-wide and window-specific menus,
		in an appropriate order according to platform conventions."""
		window = self.target_window
		return self._effective_menus_for_window(window)
	
	def _effective_menus_for_window(self, window):
		"""Return a list of the menus in effect for the specified
		window, including both application-wide and window-specific menus,
		in an appropriate order according to platform conventions."""
		menus = self.menus
		if window:
			menus = menus + window.menus
		regular_menus = []
		special_menus = []
		for menu in menus:
			if menu.special:
				special_menus.insert(0, menu)
			else:
				regular_menus.append(menu)
		return regular_menus + special_menus

#	def _may_close_a_window(self):
#		#  On implementations where at least one window is needed in order to
#		#  interact with the application, check whether closing a window would
#		#  leave no more visible windows.
#		if self.zero_windows_allowed():
#			return True
#		count = 0
#		for window in self.windows:
#			if window.visible:
#				count += 1
#				if count >= 2:
#					return True
#		return False

	def _check_for_no_windows(self):
		#  On implementations where at least one window is needed in order to
		#  interact with the application, check whether there are no more visible
		#  windows and take appropriate action.
		if not self.zero_windows_allowed():
			for window in self.windows:
				if window.visible:
					return
		self.no_visible_windows()

	def no_visible_windows(self):
		"""On platforms that require a window in order to interact with the
		application, this is called when there are no more visible windows.
		The default action is to close the application; subclasses may override
		it to take some other action, such as creating a new window."""
		self.quit_cmd()
