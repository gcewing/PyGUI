#--------------------------------------------------------------------
#
#   PyGUI - File Dialogs - Win32
#
#--------------------------------------------------------------------

import win32con as wc, win32ui as ui, win32api as api
from GUI.Files import FileRef, DirRef

win_ofn_flags = wc.OFN_FILEMUSTEXIST | wc.OFN_PATHMUSTEXIST | wc.OFN_HIDEREADONLY \
	| wc.OFN_NOCHANGEDIR | wc.OFN_OVERWRITEPROMPT

def win_filter(file_types):
	filters = []
	if file_types:
		for ftype in file_types:
			suffix = ftype.suffix
			if suffix:
				pattern = "*.%s" % suffix
				filters.append("%s (%s)|%s" % (ftype.name, pattern, pattern))
	return "|".join(filters) + "||"

def win_fix_prompt(prompt):
	for s in ("as:", ":"):
		if prompt.lower().endswith(s):
			prompt = prompt[:-len(s)]
	return prompt.strip()

def win_set_prompt(dlog, prompt):
	dlog.SetOFNTitle(win_fix_prompt(prompt))

def fileref(path, file_type = None):
	if file_type:
		suffix = file_type.suffix
		if suffix:
			ext = "." + suffix
			if not path.endswith(suffix):
				path += ext
	return FileRef(path = path)

def _request_old_file(prompt, default_dir, file_types, multiple):
	flags = win_ofn_flags
	if multiple:
		flags |= wc.OFN_ALLOWMULTISELECT
	filter = win_filter(file_types)
	dlog = ui.CreateFileDialog(True, None, None, flags, filter)
	win_set_prompt(dlog, prompt)
	if default_dir:
		dlog.SetOFNInitialDir(default_dir.path)
	code = dlog.DoModal()
	if code == 1: # IDOK
		if multiple:
			return map(fileref, dlog.GetPathNames())
		else:
			return fileref(dlog.GetPathName())

def _request_old_dir(prompt, default_dir):
	from win32com.shell import shell as sh
	import win32com.shell.shellcon as sc
	win_bif_flags = sc.BIF_RETURNONLYFSDIRS # | sc.BIF_EDITBOX | wc.BIF_VALIDATE
	if default_dir:
		def callback(hwnd, msg, lp, data):
			if msg == sc.BFFM_INITIALIZED:
				api.SendMessage(hwnd, sc.BFFM_SETSELECTION, True, default_dir.path)
	else:
		callback = None
	(idl, name, images) = sh.SHBrowseForFolder(None, None,
		win_fix_prompt(prompt), win_bif_flags, callback)
	if idl:
		return DirRef(sh.SHGetPathFromIDList(idl))

def _request_old_dirs(prompt, default_dir):
	raise NotImplementedError("Requesting multiple directories")

def _request_old(prompt, default_dir, file_types, dir, multiple):
	if dir:
		if multiple:
			return _request_old_dirs(prompt, default_dir)
		else:
			return _request_old_dir(prompt, default_dir)
	else:
		return _request_old_file(prompt, default_dir, file_types, multiple)

def _request_new(prompt, default_dir, default_name, file_type, dir):
	if file_type:
		filter = win_filter([file_type])
	else:
		filter = "" # None
	dlog = ui.CreateFileDialog(False, None, default_name, win_ofn_flags, filter)
	win_set_prompt(dlog, prompt)
	if default_dir:
		dlog.SetOFNInitialDir(default_dir.path)
	code = dlog.DoModal()
	if code == 1: # IDOK
		return fileref(dlog.GetPathName(), file_type)
