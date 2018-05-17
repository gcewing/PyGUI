from GUI import Window, CheckBox, Button, rgb, application
from testing import say

def report():
  say("Check box set to", box.on)
 
def change_auto_toggle():
	box.auto_toggle = auto.on
	say("Auto toggling =", box.auto_toggle)

box = CheckBox(
	x = 20, y = 20,
	title = "Check Box", action = report)

auto = CheckBox(x = 20, y = box.bottom + 10,
	title = "Auto Toggle",
	action = change_auto_toggle,
	color = rgb(1, 0, 0),
	on = 1)

def update_allow_mixed():
	state = allow_mixed.on
	box.mixed = state
	mixed.enabled = state

allow_mixed = CheckBox(x = 20, y = auto.bottom + 10,
	title = "Allow Mixed",
	action = update_allow_mixed)
	
def make_mixed():
	try:
		box.on = 'mixed'
	except ValueError:
		e = sys.exc_info()[1]
		say(e)
	report()

mixed = Button("Make Mixed",
	x = 20, y = allow_mixed.bottom + 10,
	action = make_mixed,
	enabled = False)

def do_show_hide():
	if box.container:
		box.container = None
	else:
		box.container = win

show_hide = Button("Show/Hide",
	x = 20, y = mixed.bottom + 10,
	action = do_show_hide)

win = Window(width = 200, height = show_hide.bottom + 20,
	title = "Check Boxes")

win.add(box)
win.add(auto)
win.add(allow_mixed)
win.add(mixed)
win.add(show_hide)
win.show()

instructions = """
There should be two check boxes titled "Check Box" and "Auto Toggle".
Clicking in the top check box should cause its state to be reported.
Clicking in the bottom check box should turn auto-toggling behaviour
of the top check box on and off.

Clicking the "Show/Hide" button should make the top check box
visible or invisible.

On platforms which support it, the label of the second check box
should be red.

On platforms which support it, the Allow Mixed check box should enable
pressing the Mixed button to set the top check box to a mixed state.
"""

say(instructions)

application().run()
