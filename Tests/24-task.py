from GUI import Window, Button, Task, application
from testing import say

def do_task():
	say("Doing the task")

task = Task(do_task, 1.0, repeat = 1, start = 0)

def start_task():
	task.start()
	
def stop_task():
	task.stop()

def test():
	starter = Button("Start", action = start_task)
	stopper = Button("Stop", action = stop_task)
	win = Window(title = "Tasks")
	win.place_column([starter, stopper], left = 20, top = 20, spacing = 20)
	win.shrink_wrap(padding = (20, 20))
	win.show()
	application().run()

instructions = """
Pressing the Start button should begin a task which prints a
message every second, and the Stop button should stop it.
"""

say(instructions)
test()
