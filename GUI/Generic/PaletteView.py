#--------------------------------------------------------------------------
#
#   PyGUI - Palette View - Generic
#
#--------------------------------------------------------------------------

from GUI import export
from GUI.Properties import overridable_property
from GUI import StdColors, GridView
from GUI.GUtils import splitdict

class PaletteView(GridView):
	"""A GridView whose cells are identified by a linear index from
	left to right and top to bottom. Also provides support for
	highlighting one or more selected cells."""
	
	num_items = overridable_property('num_items',
		"Total number of items")
		
	items_per_row = overridable_property('items_per_row',
		"Number of items displayed in one row")
	
	highlight_style = overridable_property('highlight_style',
		"Style of selection highlighting")
		
	highlight_color = overridable_property('highlight_color',
		"Color of selection highlighting")
		
	highlight_thickness = overridable_property('highlight_thickness',
		"Width of selection highlighting for 'frame' highlight mode")
	
	_highlight_style = 'fill'
	_highlight_color = StdColors.selection_backcolor
	_highlight_thickness = 4
	
	def __init__(self, num_items, items_per_row, cell_size,
			scrolling = '', **kwds):
		base_kwds = splitdict(kwds, 'border', scrolling = '')
		GridView.__init__(self, num_rows = 0, num_columns = 0, 
			cell_size = cell_size, **base_kwds)
		self._num_items = num_items
		self._items_per_row = items_per_row
		self._update_num_rows_and_columns()
		ew, eh = self.extent
		if not self.hscrolling:
			self.content_width = ew
		if not self.vscrolling:
			self.content_height = eh
		self.set(**kwds)
	
	def get_num_items(self):
		return self._num_items
	
	def set_num_items(self, n):
		self._num_items = n
		self._update_num_rows_and_columns()
	
	def get_items_per_row(self):
		return self.num_columns
	
	def set_items_per_row(self, n):
		self._items_per_row = n
		self._update_num_rows_and_columns()
	
	def _update_num_rows_and_columns(self):
		nc = self._items_per_row
		nr = (self._num_items + nc - 1) // nc
		self._num_columns = nc
		self._num_rows = nr
		self._update_extent()
	
	def get_highlight_style(self):
		return self._highlight_style
	
	def set_highlight_style(self, x):
		self._highlight_style = x
	
	def get_highlight_color(self):
		return self._highlight_color
	
	def set_highlight_color(self, x):
		self._highlight_color = x
	
	def get_highlight_color(self):
		return self._highlight_color
	
	def set_highlight_color(self, x):
		self._highlight_color = x
	
	def item_no_of_cell(self, row, col):
		i = row * self._items_per_row + col
		if 0 <= i < self._num_items:
			return i
	
	def cell_of_item_no(self, item_no):
		if 0 <= item_no < self._num_items:
			return divmod(item_no, self._items_per_row)
	
	def item_rect(self, item_no):
		cell = self.cell_of_item_no(item_no)
		if cell:
			return self.cell_rect(*cell)
	
	def draw_cell(self, canvas, row, col, rect):
		i = self.item_no_of_cell(row, col)
		if i is not None:
			highlight = self.item_is_selected(i)
			self.draw_item_and_highlight(canvas, i, rect, highlight)
	
	def draw_item_and_highlight(self, canvas, item_no, rect, highlight):
		"""Draw the specified item, with selection highlighting if highlight
		is true."""
		if highlight:
			style = self.highlight_style
			if style:
				canvas.gsave()
				if style == 'fill':
					canvas.fillcolor = self.highlight_color
					canvas.fill_rect(rect)
				else:
					canvas.pencolor = self.highlight_color
					canvas.pensize = self.highlight_thickness
					canvas.frame_rect(rect)
				canvas.grestore()
		self.draw_item(canvas, item_no, rect)
	
	def draw_item(self, canvas, item_no, rect):
		"""Should draw the specified item in the given rect."""
		pass

	def click_cell(self, row, col, event):
		i = self.item_no_of_cell(row, col)
		if i is not None:
			self.click_item(i, event)
	
	def click_item(self, item_no, event):
		"""Called when a mouse_down event has occurred in the indicated item."""
		pass
	
	def item_is_selected(self, item_no):
		"""Should return true if the indicated item is to be drawn highlighted."""
		return False

export(PaletteView)
