#------------------------------------------------------------------------------
#
#   PyGUI - TextEditor Printing - Generic
#
#------------------------------------------------------------------------------

import re
from GUI import View

class TextEditorPrintView(View):

	def __init__(self, base_view, page_setup):
		print "TextEditorPrintView:" ###
		print "...paper_size =", page_setup.paper_size ###
		print "...margins =", page_setup.margins ###
		print "...page_size =", page_setup.page_size ###
		View.__init__(self)
		self.base_view = base_view
		self.width = page_setup.page_width
		self.page_height = page_setup.page_height
		self.lay_out_text()
		lines_per_page = int(page_setup.page_height / base_view.font.line_height)
		self.lines_per_page = lines_per_page
		num_lines = len(self.lines)
		self.num_pages = (num_lines + lines_per_page - 1) // lines_per_page
		self.height = self.num_pages * self.page_height

	def lay_out_text(self):
		base_view = self.base_view
		font = base_view.font
		space_width = font.width(" ")
		tab_spacing = base_view.tab_spacing
		page_width = self.width
		pat = re.compile(r"[ \t]|[^ \t]+")
		lines = []
		line = []
		x = 0
		for text_line in base_view.text.splitlines():
			for match in pat.finditer(text_line):
				item = match.group()
				if item == " ":
					item_width = space_width
					item = ""
				elif item == "\t":
					item_width = tab_spacing - x % tab_spacing
					item = ""
				else:
					item_width = font.width(item)
				if x + item_width > page_width and x > 0:
					lines.append(line); line = []; x = 0
				line.append((x, item))
				x += item_width
			lines.append(line); line = []; x = 0
		self.lines = lines
	
	def draw(self, canvas, page_rect):
		l, t, r, b = page_rect
		page_no = int(t / self.page_height)
		n = self.lines_per_page
		i = page_no * n
		font = self.base_view.font
		y = t + font.ascent
		dy = font.line_height
		for line in self.lines[i : i + n]:
			for x, item in line:
				canvas.moveto(x, y)
				canvas.show_text(item)
			y += dy
