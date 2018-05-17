#-------------------------------------------------------------------------------
#
#		Python GUI - Table View - Cocoa
#
#-------------------------------------------------------------------------------

import traceback
from weakref import WeakValueDictionary
from Foundation import NSMakeRect, NSIndexSet
import AppKit
from AppKit import NSScrollView, NSTableView
from GUI import export
from GUI.Geometry import inset_rect
from GUI.Utils import NSMultiClass, PyGUI_NS_EventHandler, PyGUI_NS_Target
from GUI.GTableViews import TableView as GTableView, \
	TableColumn as GTableColumn, default_size

ns_table_autoresizing_mask = (AppKit.NSViewWidthSizable | AppKit.NSViewHeightSizable)

class TableView(GTableView):

	_ns_handle_mouse = True
	_default_tab_stop = True

	def __init__(self, **kwds):
		width, height = default_size
		ns_frame = NSMakeRect(0, 0, width, height)
		ns_tableview = PyNSTableView.alloc().initWithFrame_(ns_frame)
		ns_tableview.pygui_component = self
		ns_tableview.setColumnAutoresizingStyle_(0)
		ns_scrollview = NSScrollView.alloc().initWithFrame_(ns_frame)
		ns_scrollview.setDocumentView_(ns_tableview)
		ns_scrollview.setAutoresizingMask_(ns_table_autoresizing_mask)
		GTableView.__init__(self, _ns_view = ns_scrollview, _ns_inner_view = ns_tableview)
		self.set(**kwds)
		ns_tableview.setDataSource_(ns_tableview)
		#print "TableView: _ns_responder =", self._get_ns_responder() ###
	
	def destroy(self):
		ns_tableview = self._ns_inner_view
		GTableView.destroy(self)
		if ns_tableview:
			ns_tableview.pygui_component = None

	def add_column(self, column):
		"""Adds the given column descriptor at the end."""
		self._add_column(column)
		ns_tableview = self._ns_inner_view
		ns_tableview.addTableColumn_(column._ns_column)
	
	def get_columns(self):
		ns_tableview = self._ns_inner_view
		cols = self._columns_by_id
		return [cols.get(ns_column.identifier())
			for ns_column in ns_tableview.tableColumns()]
	
	def get_selected_row_num(self):
		ns_tableview = self._ns_inner_view
		return ns_tableview.selectedRow()
	
	def _set_selected_row_num(self, x):
		ns_tableview = self._ns_inner_view
		s = NSIndexSet.indexSetWithIndex_(x)
		ns_tableview.selectRowIndexes_byExtendingSelection_(s, False)
	
#	def find_cell(self, position):
#		"""Find the row and column containing the given coordinates. Returns a
#		tuple (row_num, column_id), or None if the position is outside the bounds
#		of the table."""
#		ns_tableview = self._ns_inner_view
#		row_num = ns_tableview.rowAtPoint_(position)
#		col_num = ns_tableview.columnAtPoint_(position)
#		if row_num >= 0 and col_num >= 0:
#			column_id = ns_tableview.tableColumns()[col_num].identifier()
#			return (row_num, column_id)
	
	def find_row(self, point):
		"""Returns the row number of the row containing the given point,
		or -1 if it is outside the bounds of the table."""
		ns_tableview = self._ns_inner_view
		return ns_tableview.rowAtPoint_(point)
	
	def find_column(self, point):
		"""Returns the column id of the column containing the given point,
		or None if it is outside the bounds of the table."""
		ns_tableview = self._ns_inner_view
		col_num = ns_tableview.columnAtPoint_(point)
		if col_num >= 0:
			return ns_tableview.tableColumns()[col_num].identifier()
	
	def cell_rect(self, row_num, column_id):
		"""Return the bounding rectangle of the specified table cell."""
		ns_tableview = self._ns_inner_view
		col_num = ns_tableview.columnWithIdentifier_(column_id)
		ns_row_rect = ns_tableview.rectOfRow_(row_num)
		ns_col_rect = ns_tableview.rectOfColumn_(col_num)
		x = ns_col_rect.origin.x
		y = ns_row_rect.origin.y
		w = ns_col_rect.size.width
		h = ns_row_rect.size.height
		return (x, y, x + w, y + h)

	def _editor_rect(self, editor, cell_rect):
		if editor.border:
			cell_rect = inset_rect(cell_rect, (-1, -2))
		return cell_rect
	
	def invalidate(self):
		ns_tableview = self._ns_inner_view
		ns_tableview.reloadData()
	
#-------------------------------------------------------------------------------

class PyNSTableView(NSTableView, PyGUI_NS_EventHandler, PyGUI_NS_Target):
	__metaclass__ = NSMultiClass
	
	__slots__ = ['pygui_component']
	
	def numberOfRowsInTableView_(self, v):
		return self.pygui_component.get_num_rows()
	
	def tableView_objectValueForTableColumn_row_(self, v, ns_column, row_num):
		try:
			return self.pygui_component._get_formatted_value(row_num, ns_column.identifier())
		except Exception:
			traceback.print_exc()
			return "<Error>"

#-------------------------------------------------------------------------------

export(TableView)
