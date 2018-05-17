#
#		Python GUI - DrawableContainers - PyObjC
#

from Foundation import NSMakeRect
from AppKit import NSView, NSScrollView, NSColor
from GUI import export
from GUI.Utils import PyGUI_Flipped_NSView
from GUI import Canvas
from GUI.Geometry import rect_to_ns_rect
from GUI.Utils import NSMultiClass, PyGUI_NS_ViewBase
from GUI.GDrawableContainers import default_size, \
	DrawableContainer as GDrawableContainer

ns_gray = NSColor.grayColor()

class DrawableContainer(GDrawableContainer):

	def __init__(self, **kwds):
		width, height = default_size
		ns_frame = NSMakeRect(0, 0, width, height)
		ns_inner_view = PyGUI_User_NSView.alloc().initWithFrame_(ns_frame)
		if self._ns_scrollable:
			ns_view = NSScrollView.alloc().initWithFrame_(ns_frame)
			ns_view.setDocumentView_(ns_inner_view)
			ns_view.setBackgroundColor_(ns_gray)
		else:
			ns_view = ns_inner_view
		ns_inner_view.pygui_component = self
		GDrawableContainer.__init__(self, _ns_view = ns_view, _ns_inner_view = ns_inner_view)
		self.set(**kwds)
	
	def destroy(self):
		#print "View.destroy:", self ###
		ns_inner_view = self._ns_inner_view
		GDrawableContainer.destroy(self)
		if ns_inner_view:
			#print "View.destroy: breaking back link from", ns_inner_view ###
			ns_inner_view.pygui_component = None
	
	def get_background_color(self):
		ns_view = self._ns_inner_view
		if ns_view.drawsBackground():
			return Color._from_ns_color(ns_view.backgroundColor())
	
	def set_background_color(self, x):
		ns_view = self._ns_inner_view
		if x:
			ns_view.setBackgroundColor_(x._ns_color)
			ns_view.setDrawsBackground_(True)
		else:
			ns_view.setDrawsBackground_(False)
	
	def invalidate(self):
		self._ns_inner_view.setNeedsDisplay_(True)
	
	def invalidate_rect(self, r):
		self._ns_inner_view.setNeedsDisplayInRect_(rect_to_ns_rect(r))

	def with_canvas(self, proc):
		ns_view = self._ns_view
		ns_view.lockFocus()
		proc(Canvas())
		ns_view.unlockFocus()
	
	def update(self):
		self._ns_view.displayIfNeeded()
	
	def track_mouse(self):
		return self._ns_track_mouse(self._ns_inner_view)
	
#------------------------------------------------------------------------------

class PyGUI_User_NSView(PyGUI_Flipped_NSView, PyGUI_NS_ViewBase):
	#
	#  pygui_component   View
	
	__metaclass__ = NSMultiClass
	__slots__ = ['pygui_component']
	
	def drawRect_(self, ns_rect):
		(l, t), (w, h) = ns_rect
		rect = (l, t, l + w, t + h)
		self.pygui_component.draw(Canvas(), rect)

export(DrawableContainer)
