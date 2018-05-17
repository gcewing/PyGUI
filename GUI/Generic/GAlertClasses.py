#
#   Python GUI - Alerts - Generic
#

from GUI import BaseAlert
from GUI import Button
from GUI.StdButtons import DefaultButton, CancelButton


class Alert(BaseAlert):

	def __init__(self, kind, prompt,
			ok_label = "OK", default = 1, **kwds):
		BaseAlert.__init__(self, kind, prompt,
			button_labels = [ok_label], default = default, **kwds)

	def _create_buttons(self, ok_label):
		self.yes_button = DefaultButton(title = ok_label, action = self.yes)
		self.default_button = self.yes_button

	def _layout_buttons(self):
		self.place(self.yes_button,
			right = self.label.right,
			top = self.label + self._label_button_spacing)


class Alert2(BaseAlert):

	def __init__(self, kind, prompt,
			yes_label = "Yes", no_label = "No",
			default = 1, cancel = 0, **kwds):
		BaseAlert.__init__(self, kind, prompt,
			button_labels = [yes_label, no_label],
			default = default, cancel = cancel, **kwds)

	def _create_buttons(self, yes_label, no_label):
		self.yes_button = DefaultButton(title = yes_label, action = self.yes)
		self.no_button = CancelButton(title = no_label, action = self.no)
		self.default_button = self.yes_button
		self.cancel_button = self.no_button

	def _layout_buttons(self):
		self.place_row([self.no_button, self.yes_button],
			right = self.label.right,
			top = self.label + self._label_button_spacing)


class Alert3(BaseAlert):

	_minimum_width = 300

	def __init__(self, kind, prompt,
			yes_label = "Yes", no_label = "No", other_label = "Cancel",
			default = 1, cancel = -1, **kwds):
		BaseAlert.__init__(self, kind, prompt,
			button_labels = [yes_label, no_label, other_label],
			default = default, cancel = cancel, **kwds)

	def _create_buttons(self, yes_label, no_label, cancel_label):
		self.yes_button = DefaultButton(title = yes_label, action = self.yes)
		self.no_button = CancelButton(title = no_label, action = self.no)
		self.other_button = Button(title = cancel_label, action = self.other)
		self.default_button = self.yes_button
		self.cancel_button = self.other_button

	def _layout_buttons(self):
		self.place_row([self.other_button, self.yes_button],
			right = self.label.right,
			top = self.label + self._label_button_spacing)
		self.place(self.no_button,
			left = self._left_margin, top = self.label + self._label_button_spacing)
