from GUI import Window, Button, CheckBox, Label, TextField, Column, application
from testing import say

def make_col(align):
	return Column(
		[
			CheckBox("One"),
			Label("Two"),
			TextField(text = "Three", size = (100, 50)),
			Button("Four"),
		],
		expand = 2,
		align = align)

cols = []
for align in ['l', 'c', 'r']:
	col = make_col(align)
	cols.append([col, "align = '%s'" % align])

col = Column([Button("Buckle"), Button("My"), Button("Shoe")],
	equalize = 'w')
cols.append([col, "equalize = 'w'"])

x = 10
for col, title in cols:
	col.position = (10, 10)
	col.anchor = 'ltrb'
	win = Window(title = title, position = (x, 50),
		auto_position = False)
	win.add(col)
	win.shrink_wrap()
	win.show()
	x = win.right + 10

instructions = """
Check that the text field in the first three columns expands vertically
when the window is resized.

Check that the components in the third column are anchored to the right
of the window.

The buttons in the fourth column should all be the same width.
"""

say(instructions)
app = application()
app.run()
