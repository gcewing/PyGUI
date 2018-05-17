#-----------------------------------------------------------------------
#
#   PyGUI - Alert functions - Generic
#
#-----------------------------------------------------------------------

from GUI import BaseAlertFunctions

def alert(kind, prompt, ok_label = "OK", **kwds):
	"""Displays an alert box with one button. Does not return a value.
	Kind may be 'stop' for conditions preventing continuation,
	'caution' for warning messages, 'note' for informational
	messages, and 'query' for asking a question of the user."""

	BaseAlertFunctions.alert(kind, prompt, ok_label, **kwds)


def alert2(kind, prompt, yes_label = "Yes", no_label = "No",
		**kwds):
	"""Displays an alert with two buttons. Returns 1 if the
	first button is pressed, 0 if the second button is pressed.
	The 'default' and 'cancel' arguments specify which buttons,
	if any, are activated by the standard keyboard equivalents,
	and take the values 1, 0 or None."""
	
	return BaseAlertFunctions.alert2(kind, prompt, yes_label, no_label,**kwds)
	

def alert3(kind, prompt,
		yes_label = "Yes", no_label = "No", other_label = "Cancel",
		**kwds):
	"""Displays an alert with 3 buttons. Returns 1 if the
	first button is pressed, 0 if the second button is pressed,
	and -1 if the third button is pressed. The 'default' and 'cancel'
	arguments specify which buttons, if any, are activated by the
	standard keyboard equivalents, and take the values 1, 0, -1 or None."""

	return BaseAlertFunctions.alert3(kind, prompt, yes_label, no_label, other_label, **kwds)


def stop_alert(*args, **kwds):
	"""Displays a 1-button alert of type 'stop'. See alert()."""
	alert('stop', *args, **kwds)

def note_alert(*args, **kwds):
	"""Displays a 1-button alert of type 'note'. See alert()."""
	alert('note', *args, **kwds)

def confirm(*args, **kwds):
	"""Displays a 2-button alert of type 'caution'. See alert2()."""
	return alert2('caution', *args, **kwds)

def ask(*args, **kwds):
	"""Displays a 2-button alert of type 'query'. See alert2()."""
	return alert2('query', *args, **kwds)

def confirm_or_cancel(*args, **kwds):
	"""Displays a 3-button alert of type 'caution'. See alert3()."""
	return alert3('caution', *args, **kwds)

def ask_or_cancel(*args, **kwds):
	"""Displays a 3-button alert of type 'query'. See alert3()."""
	return alert3('query', *args, **kwds)
