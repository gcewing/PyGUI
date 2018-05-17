#
#   Python GUI - File selection dialogs - Gtk
#

import os
from gi.repository import Gtk
from GUI.Files import FileRef
from GUI.AlertFunctions import confirm
from GUI.Applications import application

#------------------------------------------------------------------

class _FileDialog(Gtk.FileChooserDialog):

	def __init__(self, ok_label, **kwds):
		Gtk.FileChooserDialog.__init__(self, **kwds)
		self.add_button(Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT)
		self.add_button(ok_label, Gtk.ResponseType.ACCEPT)
		self.connect('response', self.response)
		self.set_default_size(600, 600)
		self.set_position(Gtk.WindowPosition.CENTER)

	def add_file_type(self, file_type):
		suffix = file_type.suffix
		if suffix:
			filter = Gtk.FileFilter()
			name = file_type.name
			if name:
				filter.set_name(name)
			filter.add_pattern("*.%s" % suffix)
			self.add_filter(filter)

	def present_modally(self):
		return self.run() == Gtk.ResponseType.ACCEPT

	def response(self, _, id):
		#print "_FileDialog.response:", id ###
		if id == Gtk.ResponseType.ACCEPT:
			if not self.check():
				self.stop_emission('response')
	
	def check(self):
		return True

#------------------------------------------------------------------

class _SaveFileDialog(_FileDialog):
	
	def check(self):
		path = self.get_filename()
		print "_SaveFileDialog.ok: checking path %r" % path ###
		#if path is None:
		#	return False
		if not os.path.exists(path):
			return True
		else:
			result = confirm("Replace existing '%s'?" % os.path.basename(path),
				"Cancel", "Replace", cancel = None)
			return result == 0

#------------------------------------------------------------------

def _request_old(prompt, default_dir, file_types, dir, multiple):

	if prompt.endswith(":"):
		prompt = prompt[:-1]
	if dir:
		action = Gtk.FileChooserAction.SELECT_FOLDER
	else:
		action = Gtk.FileChooserAction.OPEN
	dlog = _FileDialog(title = prompt, action = action,
		ok_label = Gtk.STOCK_OPEN)
	dlog.set_select_multiple(multiple)
	if file_types:
		for file_type in file_types:
			dlog.add_file_type(file_type)
	if default_dir:
		dlog.set_current_folder(default_dir.path)
	if dlog.present_modally():
		if multiple:
			result = [FileRef(path = path) for path in dlog.get_filenames()]
		else:
			result = FileRef(path = dlog.get_filename())
	else:
		result = None
	dlog.destroy()
	return result

#------------------------------------------------------------------

def _request_new(prompt, default_dir, default_name, file_type, dir):
#	if dir:
#		action = Gtk.FileChooserAction.CREATE_FOLDER
#	else:
	action = Gtk.FileChooserAction.SAVE
	if prompt.endswith(":"):
		prompt = prompt[:-1]
	dlog = _SaveFileDialog(title = prompt, action = action,
		ok_label = Gtk.STOCK_SAVE)
	if file_type:
		dlog.add_file_type(file_type)
	if default_dir:
		dlog.set_current_folder(default_dir.path)
	if default_name:
		dlog.set_current_name(default_name)	
	if dlog.present_modally():
		path = dlog.get_filename()
		if file_type:
			path = file_type._add_suffix(path)
		result = FileRef(path = path)
	else:
		result = None
	dlog.destroy()
	return result

#------------------------------------------------------------------

#def request_new_file(prompt = "Save File", default_dir = None,
#		default_name = "", file_type = None):
#	"""Present a dialog requesting a name and location for a new file.
#	Returns a FileRef, or None if cancelled."""
#
#	if prompt.endswith(":"):
#		prompt = prompt[:-1]
#	dlog = _SaveFileDialog(title = prompt, ok_label = Gtk.STOCK_SAVE,
#		action = Gtk.FileChooserAction.SAVE)
#	if file_type:
#		dlog.add_file_type(file_type)
#	if default_dir:
#		dlog.set_current_folder(default_dir.path)
#	if default_name:
#		dlog.set_current_name(default_name)	
#	if dlog.present_modally():
#		path = dlog.get_filename()
#		if file_type:
#			path = file_type._add_suffix(path)
#		result = FileRef(path = path)
#	else:
#		result = None
#	dlog.destroy()
#	return result

#------------------------------------------------------------------

#def request_new_directory(prompt = "Create Folder", default_dir = None,
#		default_name = ""):
#	"""Present a dialog requesting a name and location for a new directory.
#	Returns a FileRef, or None if cancelled."""
#
#	if prompt.endswith(":"):
#		prompt = prompt[:-1]
#	dlog = _SaveFileDialog(title = prompt, ok_label = Gtk.STOCK_SAVE,
#		action = Gtk.FileChooserAction.CREATE_FOLDER)
#	if default_dir:
#		dlog.set_current_folder(default_dir.path)
#	if default_name:
#		dlog.set_current_name(default_name)	
#	if dlog.present_modally():
#		path = dlog.get_filename()
#		result = FileRef(path = path)
#	else:
#		result = None
#	dlog.destroy()
#	return result
