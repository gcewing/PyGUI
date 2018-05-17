#--------------------------------------------------------------------------
#
#   PyGUI - Grid View - Generic
#
#--------------------------------------------------------------------------

from GUI import export
from GUI.Properties import overridable_property
from GUI import ScrollableView, rgb

class GridView(ScrollableView):
	"""A ScrollableView consisting of a grid of equal-sized cells."""
	
	num_columns = overridable_property('num_columns',
		"Width of the view in columns")
	
	num_rows = overridable_property('num_rows',
		"Height of the view in rows")
	
	cell_size = overridable_property('cell_size',
		"Size of each cell")
	
	backcolor = overridable_property('backcolor',
		"Background fill colour")
	
	_cell_size = (32, 32)
	_num_rows = 0
	_num_columns = 0
	_backcolor = rgb(1, 1, 1, 1)
	
	def __init__(self, num_rows, num_columns, cell_size, **kwds):
		ScrollableView.__init__(self)
		self._num_rows = num_rows
		self._num_columns = num_columns
		self._cell_size = cell_size
		self._update_extent()
		self.set(**kwds)

	def get_cell_size(self):
		return self._cell_size
	
	def set_cell_size(self, x):
		self._cell_size = x
		self._update_extent()

	def get_num_rows(self):
		return self._num_rows
	
	def set_num_rows(self, x):
		self._num_rows = x
		self._update_extent()
	
	def get_num_columns(self):
		return self._num_columns
	
	def set_num_columns(self, x):
		self._num_columns = x
		self._update_extent()
	
	def _update_extent(self):
		cw, ch = self._cell_size
		nr = self._num_rows
		nc = self._num_columns
		self.extent = (cw * nc, ch * nr)
	
	def cell_rect(self, row, col):
		w, h = self._cell_size
		l = col * w
		t = row * h
		return (l, t, l + w, t + h)
	
	def get_backcolor(self):
		return self._backcolor
	
	def set_backcolor(self, x):
		self._backcolor = x
	
	def cell_containing_point(self, p):
		x, y = p
		cw, ch = self.cell_size
		return (int(y // ch), int(x // cw))

	def draw(self, canvas, update_rect):
		canvas.backcolor = self.backcolor
		canvas.erase_rect(update_rect)
		ul, ut, ur, ub = update_rect
		nr = self._num_rows
		nc = self._num_columns
		cw, ch = self.cell_size
		row0 = max(0, int(ut // ch))
		row1 = min(nr, int(ub // ch) + 1)
		col0 = max(0, int(ul // cw))
		col1 = min(nc, int(ur // cw) + 1)
		row_range = xrange(row0, row1)
		col_range = xrange(col0, col1)
		for row in row_range:
			for col in col_range:
				rect = self.cell_rect(row, col)
				self.draw_cell(canvas, row, col, rect)
	
	def draw_cell(self, canvas, row, col, rect):
		"""Should draw the cell at the given row and colum inside the given rect."""
		pass
	
	def mouse_down(self, event):
		row, col = self.cell_containing_point(event.position)
		nr = self._num_rows
		nc = self._num_columns
		if 0 <= row < nr and 0 <= col < nc:
			self.click_cell(row, col, event)
	
	def click_cell(self, row, col, event):
		"""Called when a mouse_down event has occured in the indicated cell."""
		pass

export(GridView)
