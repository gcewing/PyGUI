from GUI import Window, TableView, TextColumn, Model, TextField, run

class Row(object):

	def __init__(self, code, name, price):
		self.code = code
		self.name = name
		self.price = price

class TestModel(Model):
	
	def __init__(self, data):
		Model.__init__(self)
		self.data = data
	
	def __len__(self):
		return len(self.data)
	
	def __getitem__(self, i):
		return self.data[i]

model = TestModel([
	Row("1000", "Screw", 0.50),
	Row("1001", "Nut", 0.25),
	Row("1002", "Washer", 0.10),
	Row("2000", "Axle", 2.00),
	Row("2100", "Wheel", 3.50),
	Row("3000", "Small Gear", 5.00),
	Row("3010", "Medium Gear", 7.50),
	Row("3020", "Large Gear", 10.00),
])

class TestTableView(TableView):
	
	def mouse_down(self, e):
		p = e.position
		row_num = self.find_row(p)
		col_id = self.find_column(p)
		print "Mouse down at", p, "in cell", (row_num, col_id)
		if row_num >= 0 and col_id:
			print "Cell rect =", self.cell_rect(row_num, col_id)
		TableView.mouse_down(self, e)
	
	def navigate_outside(self):
		print "Navigate outside"
		

view = TestTableView(size = (300, 150), scrolling = 'hv', model = model)
view.add_column(TextColumn('code', "Code", 60))
view.add_column(TextColumn('name', "Name", 100, editable = True)) #@editor = TextField()))
view.add_column(TextColumn('price', "Price", 50, 'right', format = "%.2f", parser = float, editable = True))

win = Window(title = "Table")
win.add(view)
view.anchor = 'ltrb'
win.shrink_wrap()
view.become_target()
view.selected_row_num = 0
win.show()

instructions = """
There should be a window containing a table with the following columns:

   "Code", left justified, not editable
   "Name", left justified, editable
   "Price", right justified, format "%.2f", editable

Mouse-down events should be reported together with the row number and
column id of the clicked cell.

Clicking or tabbing beyond the last row should be reported as "Navigate
outside".
"""

print instructions
run()
