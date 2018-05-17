from GUI import Window, Button, RadioGroup, RadioButton, \
	application
from GUI.Alerts import alert, alert2, alert3, note_alert, stop_alert, \
	ask, confirm, ask_or_cancel, confirm_or_cancel
from testing import say

kinds = ['stop', 'caution', 'note', 'query']

def the_kind():
	return rg.value

def do_alert():
	alert(the_kind(), "The pudding factory is haunted.")

def do_alert2():
	say("Doing alert2")
	result = alert2(the_kind(),
		"Do you really want to visit the haunted pudding factory?")
	say("Result =", result)

def do_alert3():
	say("Doing alert3")
	result = alert3(the_kind(), "Exorcise the haunted pudding factory?")
	say("Result =", result)

def do_note_alert():
	note_alert("The pudding is lumpy.")

def do_stop_alert():
	stop_alert("Too much tapioca.")

def do_ask():
	say("Doing ask")
	result = ask("Stir the pudding?")
	say("Result =", result)

def do_ask_or_cancel():
	say("Doing ask_or_cancel")
	result = ask_or_cancel("How quickly do you want to stir the pudding?",
		"Fast", "Slow")
	say("Result =", result)

def do_confirm():
	say("Doing confirm")
	result = confirm("Attack Orpuddex?")
	say("Result =", result)

def do_confirm_or_cancel():
	say("Doing confirm_or_cancel")
	result = confirm_or_cancel(
		"Orpuddex is attacking.\nWhat is your response?",
		"Retaliate", "Surrender", "Run Away")
	say("Result =", result)

win = Window(title = "Alerts")
rg = RadioGroup()
rb = []
for kind in kinds:
	rb.append(RadioButton(kind.capitalize(), value = kind, group = rg))
rg.set_value('stop')
pb = [
	Button(title = "Alert", action = do_alert),
	Button(title = "Alert2", action = do_alert2),
	Button(title = "Alert3", action = do_alert3),
]
pb2 = [
	Button("Note Alert", action = do_note_alert),
	Button("Stop Alert", action = do_stop_alert),
	Button("Ask", action = do_ask),
	Button("Confirm", action = do_confirm),
	Button("Ask or Cancel", action = do_ask_or_cancel),
	Button("Confirm or Cancel", action = do_confirm_or_cancel),
]
win.place_column(pb, left = 20, top = 20)
win.place_column(rb, left = pb[2] + 20, top = 20)
win.place_column(pb2, left = rb[1].right + 20, top = 20)
win.size = (pb2[-1].right + 20, pb2[-1].bottom + 20)
win.show()

instructions = """
This lets you play around with the various standard dialog functions.
Consult the documentation for details of how they should behave. Check
that appropriate icons are displayed for the different flavours according
to platform conventions.
"""

say(instructions)
application().run()
