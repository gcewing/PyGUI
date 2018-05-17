#
#   Python GUI - File references and types - Cocoa
#

from struct import unpack
from Foundation import NSFileTypeForHFSTypeCode, \
	NSFileManager, NSFileHFSCreatorCode, NSFileHFSTypeCode
from GUI.GFiles import FileRef as GFileRef, DirRef, FileType as GFileType

class FileType(GFileType):

	def _ns_file_types(self):
		#  Return list of Cocoa file type specifications matched
		#  by this file type.
		result = []
		mac_type = self._mac_type
		if mac_type:
			result.append(NSFileTypeForHFSTypeCode(mac_type))
		suffix = self._suffix
		if suffix:
			result.append(suffix)
		return result


class FileRef(GFileRef):

	def _set_type(self, file_type):
		creator = file_type.mac_creator
		type = file_type.mac_type
		if creator is not None or type is not None:
			fm = NSFileManager.defaultManager()
			attrs = {}
			if creator is not None:
				attrs[NSFileHFSCreatorCode] = four_char_code(creator)
			if type is not None:
				attrs[NSFileHFSTypeCode] = four_char_code(type)
			#print "FileRef: Setting attributes of %r to %s" % ( ###
			#	self.path, attrs) ###
			fm.changeFileAttributes_atPath_(attrs, self.path)


def four_char_code(chars):
	return unpack(">L", chars)[0]
