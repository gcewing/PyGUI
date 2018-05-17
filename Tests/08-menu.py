from GUI import Window, Menu, Label, application
from testing import say

class MenuTestWindow(Window):

	is_hoopy = 1
	is_smeggy = 0

	def setup_menus(self, m):
		m.hoopy_cmd.enabled = 1
		m.smeggy_cmd.enabled = 1
		m.hoopy_cmd.checked = self.is_hoopy
		m.smeggy_cmd.checked = self.is_smeggy
		m.flavour_cmd.enabled = 1

	def hoopy_cmd(self):
		self.is_hoopy = 1
		self.is_smeggy = 0

	def smeggy_cmd(self):
		self.is_hoopy = 0
		self.is_smeggy = 1
	
	def flavour_cmd(self, i):
		if self.is_hoopy:
			hs = "Hoopy"
		else:
			hs = "Smeggy"
		lbl.text = "%s Flavour %s" % (hs, i)


menus = [
	Menu("Flavour", [
		("Hoopy/^H", 'hoopy_cmd'),
		("Smeggy/^S", 'smeggy_cmd'),
		("-"),
		(["Vanilla/^V", "Raspberry/^R", "Chocolate/^C"], 'flavour_cmd'),
		]
	)
]

win = MenuTestWindow(title = "Menus", size = (240, 60))
win.menus = menus
lbl = Label("Select a Flavour", position = (20, 20), width = 200)
win.add(lbl)
win.show()

instructions = """
In addition to the standard menus, there should be a menu "Flavours" containing
two options and three flavours. The most recently selected option should be
checked in the menu. Upon selecting a flavour, the currently selected option
and the index of the selected flavour should be displayed in the window. All
items in the Flavours menu should have shifted key equivalents.
"""

say(instructions)

application().run()
