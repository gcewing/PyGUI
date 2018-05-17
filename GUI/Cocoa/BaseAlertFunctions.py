#
#		Python GUI - Basic alert functions - Cocoa
#

from AppKit import \
	NSRunAlertPanel, NSRunCriticalAlertPanel, NSRunInformationalAlertPanel

def alert(kind, prompt, ok_label, **kwds):
	alert_n(kind, prompt, ok_label, None, None)

def alert2(kind, prompt, yes_label, no_label, **kwds):
	return alert_n(kind, prompt, yes_label, no_label, None)

def alert3(kind, prompt, yes_label, no_label, other_label, **kwds):
	return alert_n(kind, prompt, yes_label, no_label, other_label)

def alert_n(kind, prompt, label1, label2, label3):
	splat = prompt.split("\n", 1)
	title = splat[0]
	if len(splat) > 1:
		msg = splat[1]
	else:
		msg = ""
	if kind == 'caution':
		return NSRunCriticalAlertPanel(title, msg, label1, label2, label3)
	elif kind == 'note':
		return NSRunInformationalAlertPanel(title, msg, label1, label2, label3)
	else:
		return NSRunAlertPanel(title, msg, label1, label2, label3)
