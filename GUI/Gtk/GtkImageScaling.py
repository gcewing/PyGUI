#
#   Python GUI - Image scaling utilities - Gtk
#

from gtk import gdk

def gtk_scale_pixbuf(src_pixbuf, sx, sy, sw, sh, dw, dh):
	"""Return a new pixbuf containing the specified part of
	the given pixbuf scaled to the specified size."""
	dst_pixbuf = gdk.Pixbuf(
		src_pixbuf.get_colorspace(), src_pixbuf.get_has_alpha(),
		src_pixbuf.get_bits_per_sample(), dw, dh)
	xscale = float(dw) / sw
	yscale = float(dh) / sh
	xoffset = - xscale * sx
	yoffset = - yscale * sy
	src_pixbuf.scale(dst_pixbuf, 0, 0, dw, dh,
		xoffset, yoffset, xscale, yscale, gdk.INTERP_BILINEAR)
	return dst_pixbuf
