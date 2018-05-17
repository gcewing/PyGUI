from testing import say

class TestKeyEvents:

	def key_down(self, event):
		which = self.which_key(event)
		if event.auto:
			say("Auto key:", which)
		else:
			say("Key down:", which)
	
	def key_up(self, event):
		say("Key up:", self.which_key(event))
	
	def which_key(self, event):
		return repr(event.key or event.char)


class TestMouseEvents:
	
	def mouse_down(self, event):
		self.report_mouse_event(
			"Mouse down: %s button: %s clicks: %s" % (event.position, event.button, event.num_clicks))

	def mouse_drag(self, event):
		self.report_mouse_event("Mouse drag: %s %s" % (event.position, event.delta))

	def mouse_up(self, event):
		self.report_mouse_event("Mouse up: %s button: %s" % (event.position, event.button))

	def mouse_move(self, event):
		self.report_mouse_event("Mouse move: %s %s" % (event.position, event.delta))

#	def mouse_enter(self, event):
#		self.report_mouse_event("Mouse enter: %s" % (event.position,))
#
#	def mouse_leave(self, event):
#		self.report_mouse_event("Mouse leave: %s" % (event.position,))
	
	def report_mouse_event(self, mess):
		say(mess)


class TestTrackMouse:

	def mouse_down(self, event):
		say("Mouse down:", event.position)
		for event in self.track_mouse():
			if event.kind == 'mouse_drag':
				say("Mouse drag:", event.position)
			elif event.kind == 'mouse_up':
				say("Mouse up:", event.position)
			else:
				say("Other event:", event.kind)
