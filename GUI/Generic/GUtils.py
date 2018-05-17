#--------------------------------------------------------------------------
#
#   PyGUI - Utilities - Generic
#
#--------------------------------------------------------------------------

def splitdict(src, *names, **defaults):
	result = {}
	for name in names:
		if name in src:
			result[name] = src.pop(name)
	for name, default in defaults.iteritems():
		result[name] = src.pop(name, default)
	return result
