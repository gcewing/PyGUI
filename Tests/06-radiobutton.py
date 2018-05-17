from GUI import Window, RadioButton, application
from testing import say

btn = RadioButton(x = 30, y = 30, width = 150, title = "Radio Button")

win = Window(width = 200, height = btn.bottom + 30, title = "Radio Button")

win.add(btn)
win.show()

say("The radio button probably won't do anything on its own.")

application().run()
