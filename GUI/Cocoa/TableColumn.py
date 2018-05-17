#-------------------------------------------------------------------------------
#
#		Python GUI - Table Column - Cocoa
#
#-------------------------------------------------------------------------------

from AppKit import NSTableColumn
from GUI import export
from GUI.Utils import ns_get_just, ns_set_just
from GUI import Font
from GUI.GTableViews import TableColumn as GTableColumn

class TableColumn(GTableColumn):

	def __init__(self, column_id, *args, **kwds):
		self._ns_column = NSTableColumn.alloc().initWithIdentifier_(column_id)
		GTableColumn.__init__(self, *args, **kwds)
	
	def get_column_id(self):
		return self._ns_column.identifier()
	
	def get_title(self):
		return self._ns_column.headerCell().stringValue()
	
	def set_title(self, x):
		self._ns_column.headerCell().setStringValue_(x)
	
	def get_width(self):
		return self._ns_column.width()
	
	def set_width(self, x):
		self._ns_column.setWidth_(x)
	
	def get_font(self):
		return Font._from_ns_font(self._ns_column.dataCell().font())
	
	def set_font(self, x):
		self._ns_column.dataCell().setFont_(x._ns_font)

	def get_header_font(self):
		return Font._from_ns_font(self._ns_column.headerCell().font())
	
	def set_header_font(self, x):
		self._ns_column.headerCell().setFont_(x._ns_font)

	def get_just(self):
		return ns_get_just(self._ns_column.dataCell())
	
	def set_just(self, x):
		ns_column = self._ns_column
		ns_set_just(ns_column.headerCell(), x)
		ns_set_just(ns_column.dataCell(), x)

#-------------------------------------------------------------------------------

class PyNSTableColumn(NSTableColumn):

	pass

#-------------------------------------------------------------------------------

export(TableColumn)

