from GUI import Window, Button, RadioButton, RadioGroup, application
from testing import say

labels = ["Banana", "Chocolate", "Strawberry"]

def report():
	value = grp.value
	try:
		say(labels[value], "selected")
	except (TypeError, IndexError):
		say("Value =", value)

def set_to_chocolate():
	grp.value = 1

win = Window(width = 250, title = "Radio Groups")

grp = RadioGroup(action = report)

y = 20
for i in range(0, 3):
	rbtn = RadioButton(
		position = (20, y), 
		title = labels[i],
		group = grp, 
		value = i)
	win.add(rbtn)
	y = rbtn.bottom + 5

pbtn = Button(title = "Set to Chocolate",
	position = (20, rbtn.bottom + 20),
	action = set_to_chocolate)
win.add(pbtn)

win.height = pbtn.bottom + 20
win.show()

instructions = """
There should be three radio buttons, "Banana", "Chocolate" and "Strawberry",
and a "Set to Chocolate" button. All radio buttons should initially be off.
Turning any of the buttons on should turn the others off. Changes to the
setting should be reported.
"""

say(instructions)

application().run()
