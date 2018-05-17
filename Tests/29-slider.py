#
#   PyGUI - Slider test
#

from GUI import Slider, Window, run
from testing import say

def slid(slider, orient, number):
	name = "%s%s" % (orient.upper(), number)
	def action():
		say("Slider %s value = %s" % (name, slider.value))
	return action

def test(orient, pos, pad):
	win = Window(title = "%s Sliders" % orient.upper(), position = pos,
		auto_position = False)
	sliders = []
	if 1:
		#say("Creating slider 1")
		sl1 = sl2 = sl3 = None
		sl1 = Slider(orient = orient, max_value = 100)
		sl1.action = slid(sl1, orient, 1)
		sliders.append(sl1)
	if 1:
		#say("Creating slider 2")
		sl2 = Slider(orient = orient, max_value = 100, ticks = 6, live = False)
		sl2.value = 50
		sl2.action = slid(sl2, orient, 2)
		sliders.append(sl2)
	if 1:
		#say("Creating slider 3")
		sl3 = Slider(orient = orient, max_value = 100, ticks = 6, discrete = True)
		sl3.value = 100
		sl3.action = slid(sl3, orient, 3)
		sliders.append(sl3)
	#say("Created sliders")
	if orient == 'h':
		win.place_column(sliders, left = 20, top = 20, spacing = 20, sticky = 'ew')
		if sl2:
			sl2.vstretch = True
		if sl3:
			sl3.vmove = True
	else:
		win.place_row(sliders, left = 20, top = 20, spacing = 20, sticky = 'ns')
		if sl2:
			sl2.hstretch = True
		if sl3:
			sl3.hmove = True
	#say("Placed sliders")
	win.shrink_wrap()
	win.show()

instructions = """
There should be two windows, one containing horizontal sliders and
one containing vertical sliders. In each window, there should be
three sliders:

1. No tick marks, continuous range 0 to 100,
   initial value 0, live.

2. 6 tick marks, continuous range 0 to 100,
   initial value 50, non-live.

3. 6 tick marks, discrete range 0 to 100 in steps of 20,
   initial value 100, live.

The 'live' sliders should report their values continuously while
the mouse is dragged; the others should report their values only
when the mouse is released.
"""

say(instructions)
test('h', (20, 60), (30, 30))
test('v', (200, 60), (60, 30))
run()
