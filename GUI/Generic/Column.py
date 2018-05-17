#---------------------------------------------------------------------------
#
#   PyGUI - Column layout component - Generic
#
#---------------------------------------------------------------------------

from LayoutUtils import equalize_components
from GUI import Frame, export

class Column(Frame):

	def __init__(self, items, spacing = 10, align = 'l', equalize = '',
			expand = None, padding = (0, 0), **kwds):
		Frame.__init__(self)
		hpad, vpad = padding
		if expand is not None and not isinstance(expand, int):
			expand = items.index(expand)
		equalize_components(items, equalize)
		width = 0
		for item in items:
			if item:
				width = max(width, item.width)
		y = vpad
		gap = 0
		vanchor = 't'
		hanchor = align
		for i, item in enumerate(items):
			if item:
				y += gap
				if 'l' in align:
					x = 0
					if 'r' in align:
						item.width = width
				elif align == 'r':
					x = width - item.width
				else:
					x = (width - item.width) // 2
				item.position = (x + hpad, y)
				if i == expand:
					item.anchor = 'tb' + hanchor
					vanchor = 'b'
				else:
					item.anchor = vanchor + hanchor
				y += item.height
			if i == expand:
				vanchor = 'b'
			gap = spacing
		self.size = (width + 2 * hpad, y + vpad)
		self.add(items)
		self.set(**kwds)

export(Column)
