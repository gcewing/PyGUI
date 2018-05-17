#---------------------------------------------------------------------------
#
#   PyGUI - Row layout component - Generic
#
#---------------------------------------------------------------------------

from LayoutUtils import equalize_components
from GUI import Frame, export

class Row(Frame):

	def __init__(self, items, spacing = 10, align = 'c', equalize = '',
			expand = None, padding = (0, 0), **kwds):
		Frame.__init__(self)
		hpad, vpad = padding
		if expand is not None and not isinstance(expand, int):
			expand = items.index(expand)
		equalize_components(items, equalize)
		height = 0
		for item in items:
			if item:
				height = max(height, item.height)
		x = hpad
		gap = 0
		hanchor = 'l'
		vanchor = align
		for i, item in enumerate(items):
			x += gap;
			if item:
				if 't' in align:
					y = 0
					if 'b' in align:
						item.height = height
				elif align == 'b':
					y = height - item.height
				else:
					y = (height - item.height) // 2
				item.position = (x, y + vpad)
				if i == expand:
					item.anchor = 'lr' + vanchor
				else:
					item.anchor = hanchor + vanchor
				x += item.width;
			if i == expand:
				hanchor = 'r'
			gap = spacing
		self.size = (x + hpad, height + 2 * vpad)
		self.add(items)
		self.set(**kwds)

export(Row)
