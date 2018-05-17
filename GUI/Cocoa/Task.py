#
#   PyGUI - Tasks - Cocoa
#

import sys
from weakref import WeakValueDictionary
from Foundation import NSTimer, NSRunLoop, NSDefaultRunLoopMode
from AppKit import NSEventTrackingRunLoopMode, NSModalPanelRunLoopMode
from GUI import export
from GUI import Globals
from GUI.GTasks import Task as GTask

#----------------------------------------------------------------------
#
#   Doing things this convoluted way to work around a memory
#   leak in PyObjC. Need to avoid having the NSTimer trigger
#   creation of a bound method each time it fires or the bound
#   methods leak. Also can't use the userInfo of the NSTimer as
#   it seems to leak too.

ns_timer_to_task = WeakValueDictionary()

class TaskTrigger(object):
	pass

def fire_(ns_timer):
	ns_timer_to_task[ns_timer]._ns_fire()
	
trigger = TaskTrigger()
trigger.fire_ = fire_

#----------------------------------------------------------------------

class Task(GTask):

	def __init__(self, proc, interval, repeat = 0, start = 1):
		self._proc = proc
		self._interval = interval
		self._repeat = repeat
		self._ns_timer = None
		if start:
			self.start()
	
	def destroy(self):
		#print "Task.destroy:", self ###
		self.stop()
	
	def get_scheduled(self):
		return self._ns_timer is not None
	
	def get_interval(self):
		return self._interval
	
	def get_repeat(self):
		return self._repeat

	def start(self):
		self.stop()
		#ns_timer = \
		#	NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
		#		self._interval, self._target, '_ns_fire', None, self._repeat)
		ns_timer = \
			NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
				self._interval, trigger, 'fire:', None, self._repeat)
		self._ns_timer = ns_timer
		ns_timer_to_task[ns_timer] = self
		ns_run_loop = NSRunLoop.currentRunLoop()
		ns_run_loop.addTimer_forMode_(
			ns_timer, NSDefaultRunLoopMode)
		ns_run_loop.addTimer_forMode_(
			ns_timer, NSEventTrackingRunLoopMode)
		ns_run_loop.addTimer_forMode_(
			ns_timer, NSModalPanelRunLoopMode)
	
	def stop(self):
		ns_timer = self._ns_timer
		if ns_timer:
			ns_timer.invalidate()
			del ns_timer_to_task[ns_timer]
			self._ns_timer = None
	
	def _ns_fire(self):
		try:
			self._proc()
		except:
			Globals.pending_exception = sys.exc_info()
			self.stop()

export(Task)
