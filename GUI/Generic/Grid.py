#---------------------------------------------------------------------------
#
#   PyGUI - Grid layout component - Generic
#
#---------------------------------------------------------------------------

from LayoutUtils import equalize_components
from GUI import Frame, export

class Grid(Frame):

	def __init__(self, items, row_spacing = 5, column_spacing = 10,
			align = 'l', equalize = '', expand_row = None, expand_column = None,
			padding = (0, 0), **kwds):
		Frame.__init__(self)
		hpad, vpad = padding
		num_rows = len(items)
		num_cols = max([len(row) for row in items])
		col_widths = [0] * num_cols
		row_heights = [0] * num_rows
		for i, row in enumerate(items):
			for j, item in enumerate(row):
				if item:
					row_heights[i] = max(row_heights[i], item.height)
					col_widths[j] = max(col_widths[j], item.width)
		tot_width = 0
		row_top = 0
		row_gap = 0
		vanchor = 't'
		for i, row in enumerate(items):
			row_height = row_heights[i]
			row_top += row_gap
			col_left = 0
			col_gap = 0
			hanchor = 'l'
			if i == expand_row:
				vanchor = 'tb'
			for j, item in enumerate(row):
				col_width = col_widths[j]
				col_left += col_gap
				if item:
					if 'l' in align:
						x = 0
					elif 'r' in align:
						x = col_width - item.width
					else:
						x = (col_width - item.width) // 2
					if 't' in align:
						y = 0
					elif 'b' in align:
						y = row_height - item.height
					else:
						y = (row_height - item.height) // 2
					item.position = (hpad + col_left + x, vpad + row_top + y)
					if j == expand_column:
						item.anchor = 'lr' + vanchor
					else:
						item.anchor = hanchor + vanchor
					self.add(item)
				if j == expand_column:
					hanchor = 'r'
				col_left += col_width
				col_gap = column_spacing
				tot_width = max(tot_width, col_left)
			if i == expand_row:
				vanchor = 'b'
			row_top += row_height
			row_gap = row_spacing
		tot_height = row_top
		self.size = (tot_width + 2 * hpad, tot_height + 2 * vpad)
		self.set(**kwds)

export(Grid)
