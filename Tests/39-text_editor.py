from GUI import TextEditor, Window, Menu, Font, StdFonts, application
from GUI.StdMenus import basic_menus
from testing import say

font_size = StdFonts.application_font.size
mono_font = Font("Courier", font_size)
sans_font = Font("Helvetica", font_size)

tab_text = \
"""X----X----X
A\tB\tC"""

test_text = \
"""There was a young man from Gossage,
Who was awfully fond of a sausage.
He ate them in bed
Between slices of bread
And lay wake all night trying to think of something to rhyme with 'sausage', but couldn't.
"""

menus = [
	Menu("Test", [
		("Show Selection/1", 'show_selection_cmd'),
		("Select 3 to 7/2", 'set_selection_cmd'),
		("Show Text/3", 'show_text_cmd'),
		("Set Text/4", 'set_text_cmd'),
		("Monospaced Font/5", 'mono_cmd'),
		("Sans-Serif Font/6", 'sans_cmd'),
		("Show Tab Spacing/7", 'show_tab_spacing_cmd'),
	]),
]

class TestWindow(Window):

	def setup_menus(self, m):
		Window.setup_menus(self, m)
		m.show_selection_cmd.enabled = True
		m.set_selection_cmd.enabled = True
		m.show_text_cmd.enabled = True
		m.set_text_cmd.enabled = True
		m.mono_cmd.enabled = True
		m.sans_cmd.enabled = True
		m.show_tab_spacing_cmd.enabled = True
		#m..enabled = True
	
	def show_selection_cmd(self):
		say(self.view.selection)
	
	def set_selection_cmd(self):
		self.view.selection = (3, 7)
	
	def show_text_cmd(self):
		say(repr(self.view.text))
	
	def set_text_cmd(self):
		self.view.text = test_text
	
	def mono_cmd(self):
		self.view.font = mono_font
		self.setup_tabs()
	
	def sans_cmd(self):
		self.view.font = sans_font
		self.setup_tabs()
	
	def show_tab_spacing_cmd(self):
		say("Tab spacing =", self.view.tab_spacing)
	
	def setup_tabs(self):
		self.view.tab_spacing = self.view.font.width("X----")

def make_window(x, scrolling, title):
	win = TestWindow(position = (x + 10, 50), size = (300, 400),
		auto_position = False, title = title)
	view = TextEditor(width = 300, height = 400, scrolling = scrolling,
		anchor = 'ltrb')
	win.view = view
	win.setup_tabs()
	view.text = tab_text
	win.add(view)
	view.become_target()
	win.show()

say("""
There should be three text editing areas, one with no scrolling, one with
vertical scrolling and with both horizontal and vertical scrolling.

The ones without horizontal scrolling should wrap text to the width of the
visible area. Text should re-wrap when the window is resized.

There should be tab stops set at the spacing of the X characters in the
top line, and the characters in the next line should line up with them.
""")

make_window(0, '', "No Scrolling")
make_window(310, 'v', "Vertical Scrolling")
make_window(620, 'hv', "Full Scrolling")

app = application()
app.menus = basic_menus() + menus
app.run()
