#
#   Python GUI - Mouse trackers - Generic
#

from GUI import application

class MouseTracker(object):
	"""Iterator used to track movements of the mouse following a mouse_down
	event in a Views. Each call to the next() method returns a mouse_drag
	event, except for the last one, which returns a mouse_up event."""
	
	def __init__(self, view):
		self._view = view
		self._finished = 0
	
	def __iter__(self):
		return self
	
	def next(self):
		if not self._finished:
			event = self._next_mouse_event()
			event.position = event.position_in(self._view)
			if event.kind == 'mouse_up':
				self._finished = 1
			return event
		else:
			raise StopIteration
