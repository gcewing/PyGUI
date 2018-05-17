#
#   Python GUI - Standard Buttons
#

from GUI import Button

class DefaultButton(Button):

	def __init__(self, title = "OK", **kwds):
		kwds.setdefault('style', 'default')
		kwds.setdefault('action', 'do_default_action')
		Button.__init__(self, title = title, **kwds)

class CancelButton(Button):

	def __init__(self, title = "Cancel", **kwds):
		kwds.setdefault('style', 'cancel')
		kwds.setdefault('action', 'do_cancel_action')
		Button.__init__(self, title = title, **kwds)
