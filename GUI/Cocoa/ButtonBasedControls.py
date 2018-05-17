#------------------------------------------------------------------------------
#
#   Python GUI - PyObjC version
#
#   Mixin class for controls based on NSButton
#
#------------------------------------------------------------------------------

from Foundation import NSMutableDictionary, NSAttributedString
from AppKit import NSMutableParagraphStyle, NSFontAttributeName, \
	NSForegroundColorAttributeName, NSParagraphStyleAttributeName, \
	NSButton
from GUI.Utils import NSMultiClass, PyGUI_NS_EventHandler, \
	ns_set_action, ns_size_to_fit
from GUI import Control
from GUI.StdColors import black

#------------------------------------------------------------------------------

class ButtonBasedControl(object):

	_ns_handle_mouse = True

	_color = None

	def _create_ns_button(self, title, font, ns_button_type, ns_bezel_style,
			padding = (0, 0)):
		ns_button = PyGUI_NSButton.alloc().init()
		ns_button.pygui_component = self
		ns_button.setButtonType_(ns_button_type)
		ns_button.setBezelStyle_(ns_bezel_style)
		ns_button.setTitle_(title)
		ns_button.setFont_(font._ns_font)
		num_lines = title.count("\n") + 1
		ns_size_to_fit(ns_button, padding = padding,
			height = font.line_height * num_lines + 5)
		ns_set_action(ns_button, 'doAction:')
		return ns_button

	def set_title(self, title):
		Control.set_title(self, title)
		self._ns_update_attributed_title()
	
	def set_font(self, font):
		Control.set_font(self, font)
		self._ns_update_attributed_title()
	
	def set_just(self, just):
		Control.set_just(self, just)
		self._ns_update_attributed_title()
	
	def get_color(self):
		if self._color:
			return self._color
		else:
			return black
	
	def set_color(self, color):
		self._color = color
		self._ns_update_attributed_title()
	
	#  There is no direct way of setting the text colour of the title;
	#  it must be done using an attributed string. But when doing
	#  this, the attributes must include the font and alignment
	#  as well. So when using a custom color, we construct a new
	#  attributed string whenever the title, font, alignment or color
	#  is changed.

	def _ns_update_attributed_title(self):
		if self._color:
			ns_button = self._ns_view
			ns_attrs = NSMutableDictionary.alloc().init()
			ns_attrs[NSFontAttributeName] = ns_button.font()
			ns_attrs[NSForegroundColorAttributeName] = self._color._ns_color
			ns_parstyle = NSMutableParagraphStyle.alloc().init()
			ns_parstyle.setAlignment_(ns_button.alignment())
			ns_attrs[NSParagraphStyleAttributeName] = ns_parstyle
			ns_attstr = NSAttributedString.alloc().initWithString_attributes_(
				ns_button.title(), ns_attrs)
			ns_button.setAttributedTitle_(ns_attstr)
	
#------------------------------------------------------------------------------

class PyGUI_NSButton(NSButton, PyGUI_NS_EventHandler):
	__metaclass__ = NSMultiClass
	__slots__ = ['pygui_component']
