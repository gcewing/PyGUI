import os, sys
from GUI import Window, Button, CheckBox, application
from GUI.Files import FileType, DirRef, FileRef
from testing import say

from GUI import FileDialogs
functions = {}
function_names = [
	'request_old_file',
	'request_old_files',
	'request_new_file',
	'request_old_directory',
	'request_old_directories', 
	'request_new_directory',
]
for name in function_names:
	if hasattr(FileDialogs, name):
		functions[name] = getattr(FileDialogs, name)
	else:
		say("*** Missing function:", name)
	
last_dir = DirRef(path = os.path.abspath(os.path.dirname(sys.argv[0])))
last_name = ""

say("last_dir =", last_dir) ###

class TestWindow(Window):

	file_type = FileType(name = "TIFF Image", suffix = "tiff")

	def __init__(self):
		Window.__init__(self, size = (200, 200))
		self.filt = CheckBox("%ss only" % self.file_type.name)
		#self.multi = CheckBox("Multiple Selection")
		buts = []
		if 'request_old_file' in functions:
			buts.append(Button("Old File", action = self.do_old_file))
		if 'request_old_files' in functions:
			buts.append(Button("Old Files", action = self.do_old_files))
		if 'request_new_file' in functions:
			buts.append(Button("New File", action = self.do_new_file))
		if 'request_old_directory' in functions:
			buts.append(Button("Old Directory", action = self.do_old_dir))
		if 'request_old_directories' in functions:
			buts.append(Button("Old Directories", action = self.do_old_dirs))
		if 'request_new_directory' in functions:
			buts.append(Button("New Directory", action = self.do_new_dir))
		self.place_column([self.filt] + buts, left = 20, top = 20)
		self.shrink_wrap(padding = (20, 20))

	def save_result(self, result):
		if isinstance(result, list):
			say("Result:")
			for item in result:
				say("   ", item)
		else:
			say("Result =", result)
		print
		global last_dir, last_name
		if result:
			if isinstance(result, FileRef):
				last_dir = result.dir
				last_name = result.name
			elif isinstance(result, DirRef):
				say("Setting last_dir to", result) ###
				last_dir = result
	
	#def multiple(self):
	#	return self.multi.on
	
	def do_old_file(self):
		say("Doing request_old_file")
		if self.filt.on:
			file_types = [self.file_type]
		else:
			file_types = None
		result = FileDialogs.request_old_file("Open Dusty Old File:",
			default_dir = last_dir, file_types = file_types)
		self.save_result(result)
	
	def do_old_files(self):
		say("Doing request_old_files")
		if self.filt.on:
			file_types = [self.file_type]
		else:
			file_types = None
		result = FileDialogs.request_old_files("Open Dusty Old Files:",
			default_dir = last_dir, file_types = file_types)
		self.save_result(result)
	
	def do_old_dir(self):
		say("Doing request_old_directory")
		result = FileDialogs.request_old_directory("Open Mouldy Old Directory:",
			default_dir = last_dir)
		self.save_result(result)
	
	def do_old_dirs(self):
		say("Doing request_old_directories")
		result = FileDialogs.request_old_directories("Open Mouldy Old Directories:",
			default_dir = last_dir)
		self.save_result(result)
	
	def do_new_file(self):
		say("Doing request_new_file with default_dir = %s, default_name = %r"
			% (last_dir, last_name))
		if self.filt.on:
			file_type = self.file_type
		else:
			file_type = None
		result = FileDialogs.request_new_file("Save Shiny New File:",
			default_dir = last_dir, default_name = last_name, file_type = file_type)
		self.save_result(result)

	def do_new_dir(self):
		say("Doing request_new_directory")
		result = FileDialogs.request_new_directory("Create Sparkling New Directory:",
			default_dir = last_dir, default_name = last_name)
		self.save_result(result)

def test():
	win = TestWindow()
	win.show()
	application().run()


instructions = """
Buttons should be available for the following dialogs:

  * Old File - select a single existing file
  * Old Files - select multiple existing files
  * New File - specify name and location of a new file
  * Old Directory - select a single existing directory
  * Old Directories - select multiple existing directories
  * New Directory - specify name and location of a new directory

The selected filename or list of filenames should be printed,
or None if the dialog is cancelled.

Checking 'TIFF Images Only' should restrict the files selectable
by Old File and Old Files, and force the file name returned by
New File to have a suffix of '.tiff'.
"""

say(instructions)
test()
