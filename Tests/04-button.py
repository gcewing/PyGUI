from GUI import Window, Button, Font, application
from GUI.StdFonts import system_font
from GUI.StdColors import red, black
from testing import say

def say_hello():
  say("Hello, world!")
  btn2.enabled = 1

def say_goodbye():
  say("Goodbye, world!")
  btn2.enabled = 0

def simulate_hello():
	btn1.activate()

btn1 = Button(position = (30, 30), 
	title = "Hello", action = say_hello, style = 'default')
	
btn2 = Button(x = 30, y = btn1.bottom + 30, width = 200, 
	title = "Goodbye", just = 'centre',
	action = say_goodbye,
	enabled = 0)
btn2.font = Font("Times", 1.2 * system_font.size, [])

btn3 = Button(x = 30, y = btn2.bottom + 30, width = 200,
	font = Font("Times", 1.2 * system_font.size, ['italic']),
	action = simulate_hello, title = "Wrong", style = 'cancel')
btn3.color = red
btn3.just = 'right'
btn3.title = "Gidday Mate"

class TWindow(Window):

	def key_down(self, e):
		say(e)
		Window.key_down(self, e)

win = TWindow(width = 260, height = btn3.bottom + 30, title = "Btns", 
	resizable = 0, zoomable = 0)
	
win.add(btn1)
win.add(btn2)
win.add(btn3)
win.show()

instructions = """
There should be 3 buttons arranged vertically:
1. Title "Hello", natural width, style 'default'
2. Title "Goodbye" in a serif font, width 200, initially disabled
3. Title "Gidday Mate" in red italic, width 200, style 'cancel', right aligned
Pressing button 1 should print "Hello, world!" and enable button 2.
Pressing button 2 should print "Goodbye, world!" and disable button 2.
Pressing button 3 should simulate pressing button 1.
"""

say(instructions)
say("Testing readback of button 3 properties:")
say("title =", btn3.title)
say("font =", btn3.font)
say("color =", btn3.color)
say("just =", btn3.just)
say("End of readback test")
say()

application().run()
