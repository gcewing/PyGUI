#
#   Python GUI - File selection dialogs - Generic
#

from GUI.BaseFileDialogs import _request_old, _request_new


def request_old_file(prompt = "Open File", default_dir = None, file_types = None):
	"""Present a dialog for selecting an existing file.
	Returns a FileRef, or None if cancelled."""
	
	return _request_old(prompt, default_dir, file_types,
		dir = False, multiple = False)


def request_old_files(prompt = "Choose Files", default_dir = None, file_types = None):
	"""Present a dialog for selecting a set of existing files.
	Returns a list of FileRefs, or None if cancelled."""
	
	return _request_old(prompt, default_dir, file_types,
		dir = False, multiple = True)


def request_old_directory(prompt = "Choose Folder", default_dir = None):
	"""Present a dialog for selecting an existing directory.
	Returns a FileRef, or None if cancelled."""
	
	return _request_old(prompt, default_dir, file_types = None,
		dir = True, multiple = False)
	

def request_old_directories(prompt = "Choose Folders", default_dir = None,
		multiple = False):
	"""Present a dialog for selecting a set of existing directories.
	Returns a list of FileRefs, or None if cancelled."""
	
	return _request_old(prompt, default_dir, file_types = None,
		dir = True, multiple = True)
	

def request_new_file(prompt = "Save As:", default_dir = None,
		default_name = "", file_type = None):
	"""Present a dialog requesting a name and location for a new file.
	Returns a FileRef, or None if cancelled."""
	
	return _request_new(prompt, default_dir, default_name, file_type,
		dir = False)
	

def request_new_directory(prompt = "Create Folder:", default_dir = None,
		default_name = ""):
	"""Present a dialog requesting a name and location for a new directory.
	Returns a FileRef, or None if cancelled."""
	
	return _request_new(prompt, default_dir, default_name, file_type = None,
		dir = True)
