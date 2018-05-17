from GUI import Font, Window, TextField, Button, application
from testing import say

fancy = Font("Times", 24, ['italic'])

win_num = 0

class TestWindow(Window):
	
	def key_down(self, event):
		c = event.char
		if c == '\r':
			print "Default"
		elif c == '\x1b':
			print "Cancel"
		else:
			Window.key_down(self, event)

class TestTextField(TextField):

	def __init__(self, number, *args, **kwds):
		TextField.__init__(self, *args, **kwds)
		self.number = number
	
	def do_text_changed_action(self):
		print "Field %s text changed" % self.number
	
	def targeted(self):
		print "Field %s targeted" % self.number

	def untargeted(self):
		print "Field %s untargeted" % self.number

def show_text(win):
	fields = [win.tf1, win.tf2, win.tf3]
	n = None
	t = application().target
	for i, f in enumerate(fields):
		say("Field %d:" % (i + 1), repr(f.text))
		if f is t:
			n = i + 1
	if n:
		say("Focus: Field %d: Selection = %r" % (n, t.selection))
	else:
		say("No focus")

def select_text(win):
	win.tf2.selection = (7, 11)

def set_text(win):
	win.tf3.text = "Surprise!"

def make_window():
	global win_num
	win_num += 1
	win = TestWindow(size = (320, 200), title = "Text fields %d" % (win_num))
	win.tf1 = TestTextField(1,
		position = (20, 20),
		width = 200)
	win.tf2 = TestTextField(2,
		position = (20, win.tf1.bottom + 10),
		width = 200,
		text = "Spam\nGlorious Spam",
		multiline = True,
		lines = 2)
	win.tf3 = TestTextField(3,
		position = (20, win.tf2.bottom + 10),
		width = 200,
		font = fancy)
	win.tf4 = TestTextField(4,
		position = (20, win.tf3.bottom + 10),
		width = 200,
		editable = False,
		value = "Read Only")
	buty = win.tf4.bottom + 20
	show_but = Button("Show",
		position = (20, buty),
		action = (show_text, win))
	sel_but = Button("Select",
		position = (show_but.right + 5, buty),
		action = (select_text, win))
	set_but = Button("Set",
		position = (sel_but.right + 5, buty),
		action = (set_text, win))
	new_but = Button("New",
		position = (set_but.right + 5, buty),
		action = make_window)
	win.add(win.tf1)
	win.add(win.tf2)
	win.add(win.tf3)
	win.add(win.tf4)
	win.add(show_but)
	win.add(sel_but)
	win.add(set_but)
	win.add(new_but)
	win.width = new_but.right + 20
	win.height = show_but.bottom + 20
	win.tf1.become_target()
	win.show()
	return win

instructions = """
There should be a window containing 3 text fields:

1. A single-line text field
2. A 2-line text field with some initial text
3. A single-line field with a large italic font

A. Field 1 should have the initial keyboard focus.

B. Field 2 should allow multi-line editing, the others should not.

C1. Tabbing between all fields should work.

C2. Changing focus from one field to another should print
"Field <m> untargeted" and "Field <n> targeted".

D. Cut, Copy, Paste, Clear, Select All commands and their keyboard equivalents
should work. Their menu items should be enabled or disabled as appropriate.

E. Pressing the Enter key on the numeric keypad should print "Default", and
pressing Escape should print "Cancel". In single-line fields, the Return key
on the main keyboard should also print "Default".

F. The Show button should report the contents of each text field and the
selection range of the field having the keyboard focus.

G. The Sel button should select characters 5 to 11 of the second text
field and focus that field. Check that typed characters are entered into
the field afterwards.

H. Changing the text in any field by typing or cut/paste should print
"Field <n> text changed".

I. Pressing the Set button should replace the text in the third field
with "Surprise!", and should NOT print a change message.

J. Use the New button to create an additional window and ensure that switching
focus between windows and cut/copy/paste between windows works correctly.
"""

say(instructions)
win = make_window()

def sigterm(*a):
	raise Exception("SIGTERM")

import signal
signal.signal(signal.SIGTERM, sigterm)

application().run()
