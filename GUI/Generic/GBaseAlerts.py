#
#   Python GUI - Alert base class - Generic
#

import textwrap
from GUI import ModalDialog
from GUI import Label

class BaseAlert(ModalDialog):

	_wrapwidth = 50
	_minimum_width = 200
	_left_margin = 24
	_right_margin = 24
	_top_margin = 14
	_bottom_margin = 20
	_icon_spacing = 16
	_label_button_spacing = 20
	_default_width = 380
	_default_lines = 3

	yes_button = None
	no_button = None
	other_button = None

	def __init__(self, kind, prompt, width = None, lines = None,
			button_labels = None, default = None, cancel = None):
		#if width is None:
		#	width = self._default_width
		#if lines is None:
		#	lines = self._default_lines
		ModalDialog.__init__(self, style = 'alert')
		self.label = Label(text = self._wrap(prompt), lines = lines)
		if self.label.width < self._minimum_width:
			self.label.width = self._minimum_width
		self._create_buttons(*button_labels)
		#self.default_button = self._find_button(default)
		#self.cancel_button = self._find_button(cancel)
		self._layout(kind)
	
	def _layout(self, kind):
		icon_width, icon_height = self._layout_icon(kind)
		label_left = self._left_margin
		if icon_width:
			label_left += icon_width + self._icon_spacing
		if self.label.height < icon_height:
			self.label.height = icon_height
		self.place(self.label,
			left = label_left,
			top = self._top_margin)# + icon_height/4)
		#_wrap_text(self.label, self._default_width - label_left - self._right_margin)
		self._layout_buttons()
		self.shrink_wrap(padding = (self._right_margin, self._bottom_margin))
	
	def _layout_icon(self, kind):
		#  Place icon for the given alert kind, if any, and return its size.
		#  If there is no icon, return (0, 0).
		return (0, 0)

	def _wrap(self, text):
		width = self._wrapwidth
		return "\n\n".join(
			[textwrap.fill(para, width)
				for para in text.split("\n\n")])
	
	def _find_button(self, value):
		#print "BaseAlert._find_button:", value ###
		if value == 1:
			result = self.yes_button
		elif value == 0:
			result = self.no_button
		elif value == -1:
			result = self.other_button
		else:
			result = None
		#print "BaseAlert._find_button: result =", result ###
		return result
	
	def yes(self):
		self.dismiss(1)

	def no(self):
		self.dismiss(0)
	
	def other(self):
		self.dismiss(-1)

#def _wrap_text(label, label_width):
#	hard_lines = [text.split()
#		for text in label.text.split("\n")]
#	words = hard_lines[0]
#	for hard_line in hard_lines[1:]:
#		words.append("\n")
#		words.extend(hard_line)
#	font = label.font
#	space_width = font.width(" ")
#	lines = []
#	line = []
#	line_width = 0
#	for word in words:
#		word_width = font.width(word)
#		if word == "\n" or (line_width > 0
#				and line_width + space_width + word_width > label_width):
#			lines.append(line)
#			line = []
#			line_width = 0
#		if word <> "\n":
#			line.append(word)
#			if line_width > 0:
#				line_width += space_width
#			line_width += word_width
#	if line:
#		lines.append(line)
#	label.text = "\n".join([" ".join(line) for line in lines])



