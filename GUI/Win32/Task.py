#--------------------------------------------------------------------
#
#   PyGUI - Task - Win32
#
#--------------------------------------------------------------------

from weakref import WeakValueDictionary
import win32con as wc, win32ui as ui
from GUI import export, application
from GUI.WinUtils import win_none
from GUI.GTasks import Task as GTask

#--------------------------------------------------------------------

class TimerWnd(object):

	def __init__(self):
		win = ui.CreateFrame()
		win.CreateWindow(None, "", 0, (0, 0, 0, 0))
		win.AttachObject(self)
		self._win = win
		self.tasks = WeakValueDictionary()
	
	def schedule(self, task):
		self.cancel(task)
		event_id = id(task)
		timer_id = self._win.SetTimer(event_id, task._milliseconds)
		if not timer_id:
			raise ValueError("Out of timers")
		task._win_timer_id = timer_id
		self.tasks[event_id] = task
	
	def cancel(self, task):
		timer_id = task._win_timer_id
		if timer_id:
			self._win.KillTimer(timer_id)
			task._win_timer_id = None
	
	def OnTimer(self, event_id):
		#print "TimerWnd.OnTimer:", event_id
		task = self.tasks.get(event_id)
		if task:
			if not task._repeat:
				self.cancel(task)
			task._proc()
			#  We do this so that the application can't get starved of idle time
			#  by a repeatedly-firing Task:
			application()._win_idle()

timer_wnd = TimerWnd()

#--------------------------------------------------------------------

class Task(GTask):

	_win_timer_id = 0
	
	def __init__(self, proc, interval, repeat = False, start = True):
		self._proc = proc
		self._milliseconds = int(1000 * interval)
		self._repeat = repeat
		if start:
			self.start()
	
	def __del__(self, timer_wnd = timer_wnd):
		timer_wnd.cancel(self)
	
	def get_interval(self):
		return self._milliseconds / 1000.0
	
	def get_repeat(self):
		return self._repeat
	
	def start(self):
		timer_wnd.schedule(self)
	
	def stop(self):
		timer_wnd.cancel(self)

export(Task)
