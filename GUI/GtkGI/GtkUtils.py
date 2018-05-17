#-----------------------------------------------------------------------------
#
#   Python GUI - Gtk - Utilities
#
#-----------------------------------------------------------------------------

class GtkFixedSize(object):
	#  Mixin for Gtk widgets to force them to always request exactly the
	#  size set using set_size_request().
	
	def do_get_preferred_width(self):
		w = self.get_size_request()[0]
		#print "GtkFixedSize.do_get_preferred_width:", w ###
		return w, w

	def do_get_preferred_height(self):
		h = self.get_size_request()[1]
		#print "GtkFixedSize.do_get_preferred_height:", h ###
		return h, h

	def do_get_preferred_height_for_width(self, width):
		#print "GtkFixedSize.do_get_preferred_height_for_width:", width ###
		return self.do_get_preferred_height()

	def do_get_preferred_width_for_height(self, height):
		#print "GtkFixedSize.do_get_preferred_width_for_height:", height ###
		return self.do_get_preferred_width()

#-----------------------------------------------------------------------------

def mix_in(*src_classes):
	#  Workaround for do_xxx method overrides not working properly
	#  with multiple inheritance.
	#
	#  Usage:
	#
	#    class MyClass(Gtk.SomeBaseClass):
	#      mix_in(Class1, Class2, ...)
	#
	import sys
	frame = sys._getframe(1)
	dst_dict = frame.f_locals
	for src_class in src_classes:
		for name, value in src_class.__dict__.iteritems():
			if name not in dst_dict:
				dst_dict[name] = value
