#
#		Python GUI - Documents - Generic
#

import os, tempfile
from GUI import export
from GUI.Alerts import confirm, confirm_or_cancel
from GUI.Properties import overridable_property
from GUI import Model
from GUI import MessageHandler
from GUI.Files import FileRef, DirRef
from GUI.FileDialogs import request_new_file
from GUI import application
from GUI.Exceptions import Cancel, UnimplementedMethod, ApplicationError
from GUI.Printing import PageSetup, present_page_setup_dialog

_next_doc_number = 1	# Counter for generating default titles

class Document(Model, MessageHandler):
	"""A Document represents an
	application data structure that can be stored in a file. It
	implements the standard parts of asking the user for file names and
	reading and writing files.

	Each Document can have one or more windows associated with it. When
	the last window belonging to a document is closed, the document itself
	is closed.

	A Document provides support for keeping track of whether it has been
	edited, and asking the user whether to save changes when it is
	closed."""
	
	#  The following attribute prevents a Document that is the parent
	#  of a Model from being pickled along with that Model.
	pickle_as_parent_model = False
	
	needs_saving = overridable_property('needs_saving',
		"True if the document has been edited and needs to be saved.")
		
	file = overridable_property('file', 
		"""FileRef of the file that the document was read from or last written
		to, or None. Changing this causes update_title to be called.""")
	
	file_type = overridable_property('file_type',
		"""FileType specifying the type of file handled by this document.""")
		
	title = overridable_property('title',
		"""The title of the document. Changing this causes update_title of each
		associated window to be called.""")

	windows = overridable_property('windows',
		"List of windows associated with the document. Do not modify directly.")
		
	page_setup = overridable_property('page_setup',
		"The PageSetup to be used for printing this document.")
	
	binary = True       # True if files are to be opened in binary mode

	_file_type = None   # Type of file to create when saving
	_needs_saving = 0   # True if has been edited
	_file = None		    # FileRef of associated file, if any
	_title = None		    # Title for use in window banners, etc.
	_windows = None     # List of associated windows
	_page_setup = None  # Document-specific PageSetup instance

	#
	#		Initialisation and destruction
	#

	def __init__(self, **kwds):
		self._windows = []
		Model.__init__(self, **kwds)
		application()._add_document(self)

	def destroy(self):
		"""Destroy any associated windows, then destroy document contents."""
		#print "Document.destroy:", self ###
		for win in self._windows[:]:
			win.destroy()
		application()._remove_document(self)
		self.destroy_contents()
		Model.destroy(self)

	#
	#		Properties
	#

	def get_needs_saving(self):
		return self._needs_saving

	def set_needs_saving(self, x):
		if self._needs_saving <> x:
			self._needs_saving = x
			for window in self._windows:
				window._document_needs_saving(x)

	def get_file(self):
		return self._file

	def set_file(self, x):
		self._file = x
		if x is not None:
			application()._last_directory = x.dir
		self.update_title()
	
	def get_file_type(self):
		return self._file_type
	
	def set_file_type(self, x):
		self._file_type = x

	def get_title(self):
		t = self._title
		if t == None:
			t = self.make_title()
			self._title = t
		return t

	def set_title(self, x):
		self._title = x
		for win in self._windows:
			win.update_title()

	def get_windows(self):
		return self._windows
	
	def get_page_setup(self):
		ps = self._page_setup
		if not ps:
			ps = PageSetup()
			self._page_setup = ps
		return ps
	
	def set_page_setup(self, ps):
		self._page_setup = ps

	#
	#		Methods
	#

	def changed(self):
		"Set the needs_saving property to true."
		self.needs_saving = 1

	def new_contents(self):
		"""Should initialise the document to the appropriate state following a New
		command."""
		pass

	def read_contents(self, file):
		"""Should initialise the document's contents by reading it from the given
		file object."""
		raise UnimplementedMethod(self, 'read_contents')

	def write_contents(self, file):
		"""Should write the document's contents to the given file object."""
		raise UnimplementedMethod(self, 'write_contents')

	def destroy_contents(self):
		"""Called when the contents of the document are about to be discarded. 
		If the contents contains any Model objects, they should be destroyed."""
	
	def save_changes(self):
		"""If the document has been edited, ask the user whether to save changes,
		and do so if requested."""
		if self._needs_saving:
			result = confirm_or_cancel('Save changes to "%s"?' % self.title,
				"Save", "Don't Save", "Cancel")
			if result < 0:
				raise Cancel
			if result:
				self._save()

	def save_cmd(self):
		"""Implements the standard Save command. Writes the document to its
		associated file, asking the user for one first if necessary."""
		self._save()
	
	def _save(self):
		for window in self.windows:
			window.broadcast('flush')
		if self._file == None:
			self.get_new_file_name()
		try:
			self.write()
		except EnvironmentError, e:
			raise ApplicationError("Unable to save '%s'." % self._file.name, e)

	def save_as_cmd(self):
		"""Implements the standard Save As... command. Asks the user for a new file
		and writes the document to it."""
		self.get_new_file_name()
		self._save()

	def revert_cmd(self):
		"""Implements the standard Revert command. Discards the current contents
		of the document and re-reads it from the associated file."""
		if self._file != None:
			if confirm(
					'Revert to the last saved version of "%s"?' % self.title,
					"Revert", "Cancel"):
				self.destroy_contents()
				self.read()

	def close_cmd(self):
		"""Implements the standard Close command. Asks whether to save any
		changes, then destroys the document."""
		self.save_changes()
		self.destroy()

	def page_setup_cmd(self):
		if present_page_setup_dialog(self.page_setup):
			self.changed()

	def make_title(self):
		"""Generates a title for the document. If associated with a file,
		uses its last pathname component, else generates 'Untitled-n'."""
		global _next_doc_number
		if self._file != None:
			return os.path.basename(self._file)
		else:
			n = _next_doc_number
			_next_doc_number = n + 1
			return "Untitled-%d" % n

	def update_title(self):
		"""Called when the file property changes, to update the
		title property appropriately."""
		file = self._file
		if file:
			self.title = file.name
	
	def get_default_save_directory(self):
		"""Called when the user is about to be asked for a location in which
		to save a document that has not been saved before, to find a default
		directory for request_new_file(). Should return a DirRef or FileRef,
		or None if there is no particular preferred location."""
		return None
	
	def get_default_save_filename(self):
		"""Called when the user is about to be asked for a location in which
		to save a document that has not been saved before, to find a default
		file name for request_new_file(). Should return a suggested file name,
		or an empty string to require the user to enter a file name."""
		return ""

	#
	#		Internal methods
	#

	def get_new_file_name(self):
		"""Ask the user for a new file and associate the document with it."""
		old_file = self.file
		if old_file:
			old_name = old_file.name
			old_dir = old_file.dir
		else:
			old_name = self.get_default_save_filename()
			old_dir = self.get_default_save_directory()
		#print "Document.get_new_file_name: old_dir =", old_dir, "old_name =", old_name ###
		new_file = request_new_file(
			#'Save "%s" as:' % self.title,
			default_dir = old_dir,
			default_name = old_name,
			file_type = self.file_type or application().save_file_type)
		if new_file is None:
			raise Cancel()
		self.file = new_file

	def read(self):
		"""Read the document from its currently associated file. The
		document must be associated with a file and not have any existing
		contents when this is called."""
		if self.binary:
			mode = "rb"
		else:
			mode = "rU"
		file = self.file.open(mode)
		try:
			self.read_contents(file)
		finally:
			file.close()
		self.needs_saving = 0

	def write(self):
		"""Write the document to its currently associated file. The
		document must be associated with a file when this is called.
		The document is initially written to a temporary file which
		is then renamed, so if writing fails part way through, the
		original file is undisturbed."""
		if self.binary:
			mode = "wb"
		else:
			mode = "w"
		dir_path = self.file.dir.path
		fd, temp_path = tempfile.mkstemp(dir = dir_path, text = not self.binary)
		file = os.fdopen(fd, mode)
		try:
			try:
				self.write_contents(file)
			finally:
				file.close()
		except EnvironmentError:
			os.unlink(fd)
			raise
		path = self.file.path
		try:
			os.unlink(path)
		except EnvironmentError:
			pass
		os.rename(temp_path, path)
		self.needs_saving = 0

	def setup_menus(self, m):
		#print "Document.setup_menus" ###
		if self._needs_saving or not self._file:
			m.save_cmd.enabled = 1
		if self._needs_saving and self._file:
			m.revert_cmd.enabled = 1
		m.save_as_cmd.enabled = 1
		m.page_setup_cmd.enabled = 1

	def next_handler(self):
		return application()

export(Document)
