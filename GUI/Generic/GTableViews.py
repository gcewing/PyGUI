#-------------------------------------------------------------------------------
#
#		Python GUI - Table View - Generic
#
#-------------------------------------------------------------------------------

from GUI.Exceptions import UnimplementedMethod
from GUI.Properties import Properties, overridable_property
from GUI import Container
from GUI import ViewBase
from GUI import ScrollableBase
from GUI import TextField

default_size = (100, 100)

class TableView(Container, ViewBase, ScrollableBase):
	"""View for displaying and editing data in a tabular layout."""
	
	columns = overridable_property('columns', "List of TableColumn instances")
	selected_row_num = overridable_property('selected_row_num', "Row number of selected row")
	selected_column_id = overridable_property('selected_column_id', "Column id of selected column")
	editing = overridable_property('editing', "True if a cell is being edited")
	
	_selected_column_id = None
	_editor = None
	_default_editor = None
	
	def __init__(self, **kwds):
		Container.__init__(self, **kwds)
		ViewBase.__init__(self)
		self._columns_by_id = {}
	
	def get_selected_column_id(self):
		return self._selected_column_id
	
	def set_selected_column_id(self, x):
		if self._selected_column_id <> x:
			editing = self.finish_editing()
			self._selected_column_id = x
			if editing:
				self.start_editing()
	
	def _set_selected_column_id(self, x):
		self._selected_column_id = x
	
	def set_selected_row_num(self, x):
		if self.selected_row_num <> x:
			editing = self.finish_editing()
			self._set_selected_row_num(x)
			if editing:
				self.start_editing()
	
	def get_editing(self):
		return self._editor is not None
	
	def column(self, column_id):
		"""Return the TableColumn object for the specified column id, or None
		if there is no such column."""
		return self._columns_by_id.get(column_id)
	
	def column_is_editable(self, column_id):
		"""Return true if the specified column can be edited."""
		column = self.column(column_id)
		return column is not None and column.editable
	
	def start_editing(self):
		#print "GTableView.start_editing" ###
		if not self._editor:
			#print "GTableView.start_editing: Creating editor" ###
			row_num = self.selected_row_num
			if 0 <= row_num < self.get_num_rows():
				col_id = self.selected_column_id
				if self.column_is_editable(col_id):
					column = self.column(col_id)
					value = self.get_cell_value(row_num, col_id)
					editor = column.editor
					if editor:
						editor.value = value
					else:
						editor = self._get_default_editor()
						editor.value = column.format_value(value)
					rect = self.cell_rect(row_num, col_id)
					editor.pass_tabs = True
					editor.bounds = self._editor_rect(editor, rect)
					editor.container = self
					editor._intercept_tab_key = True
					editor.become_target()
					self._editor = editor
	
	def _get_default_editor(self):
		editor = self._default_editor
		if not editor:
			editor = TextField()
			self._default_editor = editor
		return editor

	def finish_editing(self):
		editor = self._editor
		if editor:
			row_num = self.selected_row_num
			col_id = self.selected_column_id
			column = self.column(col_id)
			if column:
				value = editor.value
				#print "GTableView.finish_editing: Storing ", repr(value), "in cell", (row_num, col_id) ###
				if not column.editor:
					value = column.parse_value(value)
				self.set_cell_value(row_num, col_id, value)
			self.cancel_editing()
			return True
		else:
			return False
	
	def cancel_editing(self):
		editor = self._editor
		if editor:
			self.remove(editor)
			self._editor = None
			self.become_target()	

	def mouse_down(self, e):
		outside = False
		self.become_target()
		p = e.position
		row_num = self.find_row(p)
		col_id = self.find_column(p)
		self.finish_editing()
		if row_num < 0:
			outside = True
			self.navigate_outside()
			row_num = self.get_num_rows() - 1
		self.selected_row_num = row_num
		self.selected_column_id = col_id
		if not outside:
			self.start_editing()
	
	def key_down(self, e):
		#print "GTableView.key_down: %r %r shift=%s" % (e.char, e.key, e.shift) ###
		c = e.char
		k = e.key
		if c == '\x1b':
			self.cancel_editing()
			return
		elif k == 'enter':
			self.finish_editing()
			return
		d = movement_map.get((c or k, e.shift))
		if d:
			self._move_to_adjacent_cell(*d)
		else:
			Container.key_down(self, e)
	
	def _editable_column_ids(self):
		cols = []
		for col in self.columns:
			col_id = col.column_id
			if self.column_is_editable(col_id):
				cols.append(col_id)
		return cols
	
	def _move_to_adjacent_cell(self, dx, dy):
		if dx and not self._editor:
			dy = dx
			dx = 0
		row_num = self.selected_row_num
		col_id = self.selected_column_id
		cols = self._editable_column_ids()
		if cols:
			try:
				col_index = cols.index(col_id)
			except ValueError:
				col_index = 0
			new_col_index = col_index + dx
			if new_col_index < 0:
				new_col_index = len(cols) - 1
				dy = -1
			elif new_col_index >= len(cols):
				new_col_index = 0
				dy = 1
			new_col_id = cols[new_col_index]
		else:
			new_col_id = col_id
		new_row_num = row_num + dy
		if new_row_num >= self.get_num_rows():
			self.navigate_outside()
			return
		if new_row_num < 0:
			return
		if row_num <> new_row_num or col_id <> new_col_id:
			editing = self.finish_editing()
			self.selected_row_num = new_row_num
			self.selected_column_id = new_col_id
			if editing:
				self.start_editing()
			
	def _add_column(self, column):
		id = column.column_id
		cols = self._columns_by_id
		if id in cols:
			raise ValueError("Column %r already exists" % id)
		cols[id] = column
	
	def _get_formatted_value(self, row_num, column_id):
		data = self.get_cell_value(row_num, column_id)
		column = self.column(column_id)
		if column:
			data = column.format_value(data)
		return data

	def _editor_rect(self, editor, cell_rect):
		"""Implementations can override this to adjust the rect within which
		an editor is positioned to allow for borders, etc."""
		return cell_rect

	#
	#   Abstract Methods
	#
	
	def get_num_rows(self):
		"""Should return the total number of rows."""
		model = self.model
		if model:
			return len(model)
		else:
			return 0

	def get_cell_value(self, row_num, column_id):
		"""Should return the data for the specified cell."""
		model = self.model
		if model:
			row = model[row_num]
			if column_id is None:
				return row
			elif isinstance(column_id, int):
				return row[column_id]
			else:
				return getattr(row, column_id)

	def set_cell_value(self, row_num, column_id, value):
		"""Should set the data for the specified cell."""
		model = self.model
		if model:
			if column_id is None:
				model[row_num] = value
			else:
				row = model[row_num]
				if isinstance(column_id, int):
					row[column_id] = value
				else:
					setattr(row, column_id, value)
			notify = getattr(model, 'notify_views', None)
			if notify:
				notify()
	
	def navigate_outside(self):
		"""Called when an attempt is made to select a cell beyond the last row
		of the table."""
		pass

#-------------------------------------------------------------------------------

movement_map = {
	('\r', False): (0, 1),
	('\t', False): (1, 0),
	('\r', True): (0, -1),
	('\t', True): (-1, 0),
	('down_arrow', False): (0, 1),
	('down_arrow', True): (0, 1),
	('up_arrow', False): (0, -1),
	('up_arrow', True): (0, -1),
}

#-------------------------------------------------------------------------------

class TableColumn(Properties):
	"""Column descriptor for a TableView."""
	
	column_id = overridable_property('column_id', "Unique identifier for the column")
	title = overridable_property('title', "Title string for the column")
	width = overridable_property('width', "Width of the column")
	header_font = overridable_property('header_font', "Font for displaying the header")
	just = overridable_property('just', "Justification of the column ('l', 'c', 'r')")
	editable = overridable_property('editable', "True if column can be edited")
	editor = overridable_property('editor', "Editing control")
	
	_editable = False

	def __init__(self, title = "", width = 50, just = 'left', **kwds):
		if kwds.get('editor'):
			self.editable = True
		Properties.__init__(self, title = title, width = width, just = just, **kwds)
	
	def get_editable(self):
		return self._editable
	
	def set_editable(self, x):
		self._editable = x
	
	def get_editor(self):
		return self._editor
	
	def set_editor(self, x):
		self._editor = x
