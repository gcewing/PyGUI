#------------------------------------------------------------------------------
#
#   Python GUI - Slider - Cocoa
#
#------------------------------------------------------------------------------

from AppKit import NSSlider
from GUI import export
from GUI.StdFonts import system_font
from GUI.Utils import NSMultiClass, PyGUI_NS_EventHandler, \
	ns_set_action, ns_size_to_fit
from GUI.GSliders import Slider as GSlider

class Slider(GSlider):

	_ns_handle_mouse = True

	def __init__(self, orient = 'h', ticks = 0, **kwds):
		length = 100
		if ticks:
			breadth = 30
		else:
			breadth = 22 # Same as default height of a text-containing control
		if orient == 'h':
			ns_frame = ((0, 0), (length, breadth))
		elif orient == 'v':
			ns_frame = ((0, 0), (breadth, length))
		else:
			raise ValueError("Invalid orientation, should be 'h' or 'v'")
		ns_slider = PyGUI_NSSlider.alloc().initWithFrame_(ns_frame)
		ns_slider.pygui_component = self
		ns_set_action(ns_slider, 'doAction:')
		GSlider.__init__(self, _ns_view = ns_slider, **kwds)
		self.set_ticks(ticks)
		self._last_value = None

	def get_min_value(self):
		return self._ns_view.minValue()

	def set_min_value(self, x):
		self._ns_view.setMinValue_(x)

	def get_max_value(self):
		return self._ns_view.maxValue()

	def set_max_value(self, x):
		self._ns_view.setMaxValue_(x)

	def get_value(self):
		return self._ns_view.doubleValue()
	
	def set_value(self, x):
		self._ns_view.setDoubleValue_(x)
	
	def get_ticks(self):
		return self._ns_view.numberOfTickMarks()
	
	def set_ticks(self, x):
		self._ns_view.setNumberOfTickMarks_(x)
	
	def get_discrete(self):
		return self._ns_view.allowsTickMarkValuesOnly()
	
	def set_discrete(self, x):
		self._ns_view.setAllowsTickMarkValuesOnly_(x)

	def get_live(self):
		return self._ns_view.isContinuous()

	def set_live(self, x):
		self._ns_view.setContinuous_(x)

	def do_action(self):
		value = self._ns_view.doubleValue()
		if value <> self._last_value:
			self._last_value = value
			GSlider.do_action(self)

#------------------------------------------------------------------------------

class PyGUI_NSSlider(NSSlider,  PyGUI_NS_EventHandler):
	__metaclass__ = NSMultiClass
	__slots__ = ['pygui_component']

export(Slider)
