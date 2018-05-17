#
#		Python GUI - View Base - PyObjC
#

import Foundation
import AppKit
from GUI import Globals, export
from GUI.Properties import overridable_property
from GUI import Event
from GUI.Utils import PyGUI_NS_EventHandler
from GUI.GViewBases import ViewBase as GViewBase

ns_tracking_mask = (
	AppKit.NSLeftMouseDraggedMask |
	AppKit.NSRightMouseDraggedMask |
	AppKit.NSOtherMouseDraggedMask |
	AppKit.NSLeftMouseUpMask |
	AppKit.NSRightMouseUpMask |
	AppKit.NSOtherMouseUpMask)

# Need to use NSDefaultRunLoopMode here otherwise timers don't fire.
ns_tracking_mode = Foundation.NSDefaultRunLoopMode # AppKit.NSEventTrackingRunLoopMode

ns_distant_future = Foundation.NSDate.distantFuture()


class ViewBase(GViewBase):

	def _change_container(self, new_container):
		self._ns_inner_view.removeCursorRects()
		super(ViewBase, self)._change_container(new_container)

	def _ns_track_mouse(self, ns_view):
		ns_app = Globals.ns_application
		tracking = True
		while tracking:
			ns_event = ns_app.nextEventMatchingMask_untilDate_inMode_dequeue_(
				ns_tracking_mask, ns_distant_future, ns_tracking_mode, True)
			event = ns_view._ns_mouse_event_to_event(ns_event)
			yield event
			tracking = event.kind <> 'mouse_up'

	def _cursor_changed(self):
		#print "ViewBase._cursor_changed:", self ###
		ns_view = self._ns_view
		ns_window = ns_view.window()
		if ns_window:
			# invalidateCursorRectsForView_ doesn't seem to trigger
			# resetCursorRects on the view.
			#ns_window.invalidateCursorRectsForView_(ns_view)
			ns_window.resetCursorRects()

	def _ns_reset_cursor_rects(self):
		#print "ViewBase._ns_reset_cursor_rects:", self ###
		cursor = self._cursor
		if cursor:
			ns_view = self._ns_inner_view
			ns_rect = ns_view.visibleRect()
			ns_view.addCursorRect_cursor_(ns_rect, cursor._ns_cursor)

export(ViewBase)
