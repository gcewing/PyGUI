#
#   Python GUI - Controls - PyObjC
#

from math import ceil
from Foundation import NSSize
import AppKit
from GUI import export
from GUI import StdColors
from GUI import Color
from GUI import Font
from GUI.GControls import Control as GControl
from GUI.Utils import ns_get_just, ns_set_just

class Control(GControl):

	#_vertical_padding = 5

	def get_title(self):
		return self._ns_cell().title()
	
	def set_title(self, v):
		self._ns_cell().setTitle_(v)
	
	def get_enabled(self):
		return self._ns_cell().enabled()
	
	def set_enabled(self, v):
		self._ns_cell().setEnabled_(v)
	
	def get_color(self):
		return StdColors.black
	
	def set_color(self, v):
		pass
			
	def get_font(self):
		return Font._from_ns_font(self._ns_cell().font())
	
	def set_font(self, f):
		self._ns_cell().setFont_(f._ns_font)
		
	def get_just(self):
		return ns_get_just(self._ns_cell())
		#return _ns_alignment_to_just[self._ns_cell().alignment()]
	
	def set_just(self, v):
		ns_set_just(self._ns_cell(), v)
		#self._ns_cell().setAlignment_(_ns_alignment_from_just[v])
	
	def _ns_cell(self):
		return self._ns_inner_view.cell()

export(Control)
