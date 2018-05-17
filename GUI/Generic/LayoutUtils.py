#---------------------------------------------------------------------------
#
#   PyGUI - Utilities for use by layout components - Generic
#
#---------------------------------------------------------------------------

def equalize_components(items, flags):
	if items:
		if 'w' in flags:
			width = max([item.width for item in items if item])
			for item in items:
				if item:
					item.width = width
		if 'h' in flags:
			height = max([item.height for item in items if item])
			for item in items:
				if item:
					item.height = height
