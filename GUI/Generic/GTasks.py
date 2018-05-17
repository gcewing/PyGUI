#
#   PyGUI - Tasks - Generic
#

from GUI.Properties import Properties, overridable_property

class Task(Properties):
	"""A Task represents an action to be performed after a specified
	time interval, either once or repeatedly.
	
	Constructor:
		Task(proc, interval, repeat = False, start = True)
			Creates a task to call the given proc, which should be
			a callable object of no arguments, after the specified
			interval in seconds from the time the task is scheduled.
			If repeat is true, the task will be automatically re-scheduled
			each time the proc is called. If start is true, the task will be 
			automatically scheduled upon creation; otherwise the start()
			method must be called to schedule the task.
	"""
	
	interval = overridable_property('interval', "Time in seconds between firings")
	repeat = overridable_property('repeat', "Whether to fire repeatedly or once only")
	
	def __del__(self):
		self.stop()

	scheduled = overridable_property('scheduled',
		"True if the task is currently scheduled. Read-only.")
	
	def start(self):
		"""Schedule the task if it is not already scheduled."""
		raise NotImplementedError("GUI.Task.start")
	
	def stop(self):
		"""Unschedules the task if it is currently scheduled."""
		raise NotImplementedError("GUI.Task.stop")
