from GUI import Window, Button, CheckBox, Label, TextField, Row, application
from testing import say

def make_row(align):
	return Row(
		[
			CheckBox("One"),
			Label("Two"),
			TextField(text = "Three", size = (100, 50)),
			Button("Four"),
		],
		expand = 2,
		align = align)

rows = []
for align in ['t', 'c', 'b']:
	row = make_row(align)
	rows.append([row, "align = '%s'" % align])

row = Row([Button("Buckle"), Button("My"), Button("Shoe")],
	equalize = 'w')
rows.append([row, "equalize = 'w'"])

y = 50
for row, title in rows:
	row.position = (10, 10)
	row.anchor = 'ltrb'
	win = Window(title = title, position = (10, y),
		auto_position = False)
	win.add(row)
	win.shrink_wrap()
	win.show()
	y = win.bottom + 50

instructions = """
Check that the text field in the first three rows expands horizontally
when the window is resized.

Check that the components in the third row are anchored to the bottom
of the window.

The buttons in the fourth row should all be the same width.
"""

say(instructions)
app = application()
app.run()
