from GUI import Window, application
from TestViews import TestDrawing, fancy_font as f
from TestInput import TestKeyEvents, TestTrackMouse
from testing import say

class TestView(TestKeyEvents, TestTrackMouse, TestDrawing):
	pass

win = Window(width = 320, height = 200)
view = TestView(width = 320, height = 200)
win.add(view)
view.become_target()
win.show()

say("""
There should be a red triangle, a blue triangle and half a green
triangle, outlined in black, on a yellow background, and three
pieces of text. Each text line should sit accurately on the
baseline drawn under it.

The following events in the view should be reported: mouse down,
mouse drag, mouse up, key down, key up, auto key.
""")

say("Font ascent =", f.ascent, "descent =", f.descent, "height =", f.height)
application().run()
