from GUI import Window, View, CheckBox, Button, Label, \
		 RadioButton, RadioGroup, TextField
from TestViews import TestDrawing
from TestScrollableViews import TestScrollableDrawing
from testing import say

def pushed_it():
	say("Button pushed.")

def checked_it():
	say("Check boxes changed to:", cb1.on, cb2.on)

def option_chosen():
	say("Hoopy option %d chosen" % rg.value)

def main():
	global cb1, cb2, rg
	
	win = Window(title = "Place Me By Your Side", width = 720, height = 500)

	view1 = TestDrawing(width = 320, height = 200)

	cb1 = CheckBox(title = "Check Me!", action = checked_it)

	cb2 = CheckBox(title = "Check Me Too!", action = checked_it)

	rbs = []
	for i in range(1, 4):	
		rb = RadioButton(title = "Hoopy Option %d" % i, value = i)
		rbs.append(rb)

	rg = RadioGroup(rbs, action = option_chosen)

	pb = Button(title = "Push Me!", action = pushed_it)

	view2 = TestScrollableDrawing(width = 300, height = 300)

	label = Label(text = "Flavour:")

	entry = TextField(width = 200)

	win.place(view1, left = 10, top = 10, border = 1)

	win.place_row([cb1, cb2], left = 10, top = (view1, 20), spacing = 20)
	
	win.place_column(rbs, left = view1 + 20, top = 10)

	win.place(pb, right = -20, bottom = -10, anchor = 'rb')

	win.place(view2, 
		left = rbs[0] + 20, top = 10, 
		right = -20,
		bottom = pb - 10,
		scrolling = 'hv',
		anchor = 'ltrb',
		border = 1)
	
	win.place(label, left = 10, top = (cb1, 20))

	win.place(entry, left = 10, top = (label, 10), 
		#border = 1
	)
	entry.become_target()

	win.show()

	import GUI
	GUI.run()

instructions = """
There should be a window containing:

1. A 320x200 view, 10 pixels from the left and top, containing some drawing.

2. Below the view, aligned with its left edge:

   2a. A row of two check boxes

   2b. A label
   
   2c. A text field
 
3. To the right of the view, aligned with its top edge, a column
   of three radio buttons.

4. To the right of the radio buttons, a scrolling view, 10 pixels from the
   top of the window and 20 from the right edge.

5. In the bottom right corner of the window, a button, 10 pixels from the
   scrolling view and from the bottom of the window, and 20 pixels from the
   right edge.

When the window is resized, the scrolling view should resize with it,
and the button should remain the same distance from the bottom right
corner.

Check that the layout remains correct when the window is obscured and
then revealed again.

Check that the layout remains correct when the window is made too small
to display all of the items and then enlarged again.
"""

say(instructions)
main()
