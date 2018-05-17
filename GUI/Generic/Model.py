#
#		Python GUI - Models - Generic
#

import weakref
from GUI import export
from GUI.Properties import Properties, overridable_property

#  List of views for a model is kept separately so that models
#  can be pickled without fear of accidentally trying to pickle
#  the user interface.

_model_views = weakref.WeakKeyDictionary() # {Model: [object]}

class Model(Properties):
	"""A Model represents an application object which can appear in a View. 
	Each Model can have any number of Views attached to it. When a Model is 
	changed, it should notify all of its Views so that they can update
	themselves.
	
	The 'parent' attribute of a Model is treated specially when pickling.
	If it refers to an object having a 'pickle_as_parent_model' attribute
	whose value is false, the 'parent' attribute is not pickled. This allows
	a Model to have a Document as a parent without the Document being pickled
	along with the Model.
	"""
	
	views = overridable_property('views', 
		"List of objects observing this model. Do not modify directly.")
	
	parent = None  # Model

	def __init__(self, parent = None, **kwds):
		Properties.__init__(self, **kwds)
		if parent:
			self.parent = parent

	def destroy(self):
		"""All views currently observing this model are removed, and their
		'model_destroyed' methods, if any, are called with the model as
		an argument."""
		for view in self.views[:]:
			self.remove_view(view)
			self._call_if_present(view, 'model_destroyed', self)

	#
	#		Properties
	#

	def get_views(self):
		views = _model_views.get(self)
		if views is None:
			views = []
			_model_views[self] = views
		return views
	
	#
	#   Pickling behaviour
	#
	
	def __getstate__(self):
		state = self.__dict__
		parent = self.parent
		if not getattr(parent, 'pickle_as_parent_model', True):
			state = state.copy()
			del state['parent']
		return state
	
	def __setstate__(self, state):
		self.__dict__.update(state)
	 
	#
	#		Adding and removing views
	#
	
	def add_view(self, view):
		"""Add the given object as an observer of this model. The view will
		typically be a View subclass, but need not be. If the view is not 
		already an observer of this model and defines an 'add_model' method,
		this method is called with the model as an argument."""
		views = self.views
		if view not in views:
			views.append(view)
			self._call_if_present(view, 'add_model', self)
	
	def remove_view(self, view):
		"""If the given object is currently an observer of this model, it
		is removed, and if it defines a 'remove_model' method, this method
		is called with the model as an argument."""
		views = self.views
		if view in views:
			views.remove(view)
			self._call_if_present(view, 'remove_model', self)

	#
	#		View notification
	#

	def notify_views(self, message = 'model_changed', *args, **kwds):
		"""For each observer, if the observer defines a method with the name of the
		message, call it with the given arguments. Otherwise, if it defines a
		method called 'model_changed', call it with no arguments. Otherwise,
		do nothing for that observer."""
		for view in self.views:
			if not self._call_if_present(view, message, self, *args, **kwds):
				self._call_if_present(view, 'model_changed', self)
	
	def _call_if_present(self, obj, method_name, *args, **kwds):
		method = getattr(obj, method_name, None)
		if method:
			method(*args, **kwds)
			return 1
		else:
			return 0

	#
	#   Marking as changed
	#
	
	def changed(self):
		"Mark the containing Document as changed."
		parent = self.parent
		if parent:
			parent.changed()

export(Model)
