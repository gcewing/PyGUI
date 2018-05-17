#
#   PyGUI - Tasks - Gtk
#

import gobject
from GUI.GTasks import Task as GTask

class Task(GTask):

	def __init__(self, proc, interval, repeat = 0, start = 1):
		self._proc = proc
		self._gtk_interval = int(interval * 1000)
		self._repeat = repeat
		self._gtk_timeout_id = None
		if start:
			self.start()
	
	def get_scheduled(self):
		return self._gtk_timeout_id is not None
	
	def start(self):
		if self._gtk_timeout_id is None:
			self._gtk_timeout_id = GObject.timeout_add(self._gtk_interval,
				self._gtk_fire)
	
	def stop(self):
		id = self._gtk_timeout_id
		if id is not None:
			GObject.source_remove(id)
			self._gtk_timeout_id = None
	
	def _gtk_fire(self):
		self._proc()
		if self._repeat:
			return 1
		else:
			self._gtk_timeout_id = None
