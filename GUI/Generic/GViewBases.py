#
#		Python GUI - View Base - Generic
#

from GUI.Properties import overridable_property

class ViewBase(object):
	"""ViewBase is an abstract base class for user-defined views.
	It provides facilities for handling mouse and keyboard events
	and associating the view with one or more models, and default
	behaviour for responding to changes in the models."""

	models = overridable_property('models',
		"List of Models being observed. Do not modify directly.")
	
	model = overridable_property('model',
		"Convenience property for views which observe only one Model.")

	cursor = overridable_property('cursor',
		"The cursor to display over the view.")

	#  _models               [Model]

	_cursor = None

	def __init__(self):
		self._models = []

	def destroy(self):
		#print "GViewBase.destroy:", self ###
		for m in self._models[:]:
			#print "GViewBase.destroy: removing model", m ###
			self.remove_model(m)

	def setup_menus(self, m):
		pass

	#
	#		Getting properties
	#
	
	def get_model(self):
		models = self._models
		if models:
			return self._models[0]
		else:
			return None

	def get_models(self):
		return self._models

	#
	#		Setting properties
	#

	def set_model(self, new_model):
		models = self._models
		if not (len(models) == 1 and models[0] == new_model):
			for old_model in models[:]:
				self.remove_model(old_model)
			if new_model:
				self.add_model(new_model)

	#
	#   Model association
	#
	
	def add_model(self, model):
		"""Add the given Model to the set of models being observed."""
		if model not in self._models:
			self._models.append(model)
			add_view = getattr(model, 'add_view', None)
			if add_view:
				add_view(self)
			self.model_added(model)
	
	def remove_model(self, model):
		"""Remove the given Model from the set of models being observed."""
		if model in self._models:
			self._models.remove(model)
			remove_view = getattr(model, 'remove_view', None)
			if remove_view:
				remove_view(self)
			self.model_removed(model)
	
	def model_added(self, model):
		"""Called after a model has been added to the view."""
		pass

	def model_removed(self, model):
		"""Called after a model has been removed from the view."""
		pass

	#
	#   Input event handling
	#

	def track_mouse(self):
		"""Following a mouse_down event, returns an iterator which can be used
		to track the movements of the mouse until the mouse is released.
		Each call to the iterator's next() method returns a mouse_drag
		event, except for the last one, which returns a mouse_up event."""
		raise NotImplementedError

# 	def targeted(self):
# 		"""Called when the component becomes the target within its Window."""
# 		pass
# 
# 	def untargeted(self):
# 		"""Called when the component ceases to be the target within its Window."""
# 		pass

	#
	#   Cursors
	#
	
	def get_cursor(self, x):
		return self._cursor
	
	def set_cursor(self, x):
		self._cursor = x
		self._cursor_changed()

	#
	#		Callbacks
	#

	def model_changed(self, model, *args, **kwds):
		"""Default method called by the attached Model's notify_views
		method. Default is to invalidate the whole view."""
		self.invalidate()

	def model_destroyed(self, model):
		"""Called when an attached model is destroyed. Default is to
		destroy the window containing this view."""
		win = self.window
		if win:
			win.destroy()

