from GUI import Window, TextView, TextModel, Font, application
from TestViews import TestView

app = application()
app.set_menus(app.std_menus())

win = Window(width = 300, height = 200)
text = TextModel()
text.set_text("Hello\nWorld!")
view = TextView(width = 300, height = 200, model = text)
view.set_font(Font("Helvetica", 14, []))
win.add(view)
view.become_target()
win.show()

app.run()
