from GUI import Window, CheckBox, Label, TextField, Grid, application
from testing import say

items = [
	[Label("Name"), TextField(width = 100)],
	[Label("Age"), TextField(width = 50)],
	[Label("Language"), CheckBox("Python")],
]

grid = Grid(items)

win = Window(title = "Grid")
grid.position = (10, 10)
win.add(grid)
win.shrink_wrap()
win.show()

instructions = """
There should be six components laid out in a grid of three rows
and two columns. Each component should be centre-left aligned
within its cell.
"""

say(instructions)
application().run()
