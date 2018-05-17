#
#		Exceptions.py - GUI exception classes
#

class Cancel(Exception):
	"""Exception raised when user cancels an operation."""
	pass


#class Quit(Exception):
#	"""Exception raised to exit the main event loop."""
#	pass


class Error(StandardError):

	def __init__(self, obj, mess):
		self.obj = obj
		self.mess = mess
		Exception.__init__(self, "%s: %s" % (obj, mess))


class ApplicationError(StandardError):
	"""Exception used for reporting errors to the user."""
	
	def __init__(self, message, detail = None):
		self.message = message
		self.detail = detail
		if detail:
			message = "%s\n\n%s" % (message, detail)
		StandardError.__init__(self, message)


class InternalError(Exception):
	pass


class UnimplementedMethod(NotImplementedError):

	def __init__(self, obj, meth_name):
		self.obj = obj
		StandardError.__init__(self, "%s.%s not implemented" % \
			(obj.__class__.__name__, meth_name))


class ArgumentError(TypeError):

	def __init__(self, obj, meth_name, arg_name, value):
		self.obj = obj
		self.meth_name = meth_name
		self.arg_name = arg_name
		self.value = value
		TypeError.__init__(self, 
			"%s: Invalid value %s for argument %s of method %s",
				(obj, value, arg_name, meth_name))


class SetAttributeError(AttributeError):

	def __init__(self, obj, attr):
		self.obj = obj
		self.attr = attr
		AttributeError.__init__(self, "Attribute '%s' of %s cannot be set" % (attr, obj))


class UsageError(StandardError):
	pass
