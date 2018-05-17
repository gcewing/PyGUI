from GUI import Window, Label, Font, application
from GUI.StdColors import red
from GUI.StdFonts import system_font
from testing import say

num_rows = 6

italic_font = Font("Times", 2 * system_font.size, ['italic'])

def dump_font(caption, f):
	say(caption, f.family, f.size, f.style)

dump_font("System font:", system_font)
dump_font("Italic font:", italic_font)

def make_label(text, **kwds):
	#say("Creating label", text)
	return Label(text = text, **kwds)

#say("Creating labels")
lbls = [
	make_label("ParrotState:"),
	make_label("Resting"),
	make_label("Spam!\nGlorious Spam!"),
	make_label("Red", color = red),
	make_label("Big Italic", font = italic_font),
	make_label("Pig in the\nMiddle", just = 'center', width = 140),
	make_label("Right\nJustified", just = 'right', width = 140),
]

#say("Setting label positions")
#say("Setting lbls[0].position to (20, 20)")
#say("Before: lbls[0].bounds =", lbls[0].bounds)
lbls[0].position = (20, 20)
#say("After: lbls[0].bounds =", lbls[0].bounds)
lbls[1].position = (lbls[0].right, lbls[0].top)
for i in range(2, len(lbls)):
	lbls[i].position = (lbls[0].left, lbls[i-1].bottom + 20)

#for lbl in lbls:
#	say(lbl.height)

#say("Creating window")
win = Window(title = "Labels")
for lbl in lbls:
	win.add(lbl)
win.size = (lbls[-1].right + 20, lbls[-1].bottom + 20)
win.show()

instructions = """
There should be six rows of labels:
1. Two labels "ParrotState:" and "Resting", abutting but not overlapping.
2. A two-line label "Spam!\\nGlorious Spam!"
3. A label "Red" in red text.
4. A label "Big Italic" in a large italic font.
5. A two-line label "Pig in the\\nMiddle" centred in the window.
6. A two-line label "Right\\nJustified" right-aligned.
All labels should remain stationary relative to the top left corner
of the window when it is resized.
"""

say(instructions)

#application().menus = []

application().run()
