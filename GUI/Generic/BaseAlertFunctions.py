#
#		Python GUI - Basic alert functions - Generic
#

from GUI.GAlertClasses import Alert, Alert2, Alert3

def present_and_destroy(dlog):
	dlog.center()
	try:
		return dlog.present()
	finally:
		dlog.destroy()


def alert(kind, prompt, ok_label, **kwds):
	present_and_destroy(Alert(kind, prompt, ok_label))


def alert2(kind, prompt, yes_label, no_label, **kwds):
	return present_and_destroy(
		Alert2(kind, prompt, yes_label, no_label, **kwds))


def alert3(kind, prompt, yes_label, no_label, other_label, **kwds):
	return present_and_destroy(
		Alert3(kind, prompt, yes_label, no_label, other_label, **kwds))
