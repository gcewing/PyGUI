#
#   Python GUI - File selection dialogs - Cocoa
#

from AppKit import NSOpenPanel, NSSavePanel, NSOKButton
from GUI.Files import FileRef
from GUI import application

#------------------------------------------------------------------

def _request_old(prompt, default_dir, file_types, dir, multiple):
	ns_panel = NSOpenPanel.openPanel()
	if prompt.endswith(":"):
		prompt = prompt[:-1]
	ns_panel.setTitle_(prompt)
	ns_panel.setCanChooseFiles_(not dir)
	ns_panel.setCanChooseDirectories_(dir)
	ns_panel.setAllowsMultipleSelection_(multiple)
	if default_dir:
		ns_dir = default_dir.path
	else:
		ns_dir = None
	if file_types:
		ns_types = []
		for type in file_types:
			ns_types.extend(type._ns_file_types())
	else:
		ns_types = None
	result = ns_panel.runModalForDirectory_file_types_(ns_dir, None, ns_types)
	if result == NSOKButton:
		if multiple:
			return [FileRef(path = path) for path in ns_panel.filenames()]
		else:
			return FileRef(path = ns_panel.filename())
	else:
		return None

#------------------------------------------------------------------

def _request_new(prompt, default_dir, default_name, file_type, dir):
	ns_panel = NSSavePanel.savePanel()
	#if prompt.endswith(":"):
	#	prompt = prompt[:-1]
	#if prompt.lower().endswith(" as"):
	#	prompt = prompt[:-3]
	#ns_panel.setTitle_(prompt)
	#print "_request_new: setting label to", repr(prompt) ###
	ns_panel.setNameFieldLabel_(prompt)
	if default_dir:
		ns_dir = default_dir.path
	else:
		ns_dir = None
	if file_type:
		suffix = file_type.suffix
		if suffix:
			ns_panel.setCanSelectHiddenExtension_(True)
			if not file_type.mac_type or file_type.mac_force_suffix:
				ns_panel.setRequiredFileType_(suffix)
	result = ns_panel.runModalForDirectory_file_(ns_dir, default_name)
	if result == NSOKButton:
		return FileRef(path = ns_panel.filename())
	else:
		return None
