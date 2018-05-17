#------------------------------------------------------------------------------
#
#		Python GUI - Actions - Generic
#
#------------------------------------------------------------------------------

from GUI.Properties import overridable_property
from GUI.Exceptions import ApplicationError

#------------------------------------------------------------------------------

def action_property(name, doc):
	attr = intern('_' + name)
	def getter(self):
		return getattr(self, attr)
	def setter(self, value):
		setattr(self, attr, value)
	return property(getter, setter, None, doc)

#------------------------------------------------------------------------------

class ActionBase(object):
	"""Mixin class providing base support for action properties."""

	def do_named_action(self, name):
		#print "ActionBase.do_named_action:", repr(name) ###
		action = getattr(self, name)
		#print "...action =", repr(action) ###
		if action:
			try:
				if isinstance(action, tuple):
					args = action[1:]
					action = action[0]
				else:
					args = ()
				if isinstance(action, str):
					#print "...handling", action ###
					self.handle(action, *args)
				else:
					return action(*args)
			except ApplicationError:
				raise
			except:
				import sys
				et, ev, tb = sys.exc_info()
				raise et, et("%s (while doing action %r%r)" % (ev, action, args)), tb

#------------------------------------------------------------------------------

class Action(ActionBase):
	"""Mixin class providing a single action property called 'action'."""
	
	action = action_property('action', """Action to be performed.
		May be <action> or (<action>, <arg>...) where <action> is either
		a message name or a callable object.""")

	_action = None

	def do_action(self):
		"Invoke the action."
		self.do_named_action('action')

