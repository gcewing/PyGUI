#------------------------------------------------------------------------------
#
#   PyGUI - OpenGL - Win32
#
#------------------------------------------------------------------------------

import win32con as wc, win32ui as ui, win32gui as gui
import GDIPlus as gdi
import WGL
from GUI.Components import win_none
from GUI.OpenGL import WGL as wgl
from GUI.GGLViews import GLView as GGLView
from GUI.GGLPixmaps import GLPixmap as GGLPixmap
from GUI.GGLConfig import GLConfig as GGLConfig, GLConfigError
from GUI.GLContexts import GLContext
from GUI.GLTextures import Texture

win_style = wc.WS_VISIBLE | wc.WS_CLIPCHILDREN | wc.WS_CLIPSIBLINGS
win_default_size = GGLView._default_size
win_default_rect = (0, 0, win_default_size[0], win_default_size[1])

#------------------------------------------------------------------------------

class GLConfig(GGLConfig):

	def _as_win_pixelattrs(self, mode):
		print "GLConfig._as_arb_pixelattrs: mode =", mode ###
		attrs = {}
		attrs[wgl.WGL_SUPPORT_OPENGL_ARB] = True
		if mode == 'screen' or mode == 'both':
			print "GLConfig: requesting screen drawing" ###
			attrs[wgl.WGL_DRAW_TO_WINDOW_ARB] = True
			if self._double_buffer:
				attrs[wgl.WGL_DOUBLE_BUFFER_ARB] = True
		if mode == 'pixmap' or mode == 'both':
			print "GLConfig: requesting pixmap drawing" ###
			attrs[wgl.WGL_DRAW_TO_PBUFFER_ARB] = True
		if self._stereo:
			attrs[wgl.WGL_STEREO_ARB] = True
		attrs[wgl.WGL_PIXEL_TYPE_ARB] = wgl.WGL_TYPE_RGBA_ARB
		bits = self._color_size
		attrs[wgl.WGL_RED_BITS_ARB] = bits
		attrs[wgl.WGL_GREEN_BITS_ARB] = bits
		attrs[wgl.WGL_BLUE_BITS_ARB] = bits
		if self._alpha:
			attrs[wgl.WGL_ALPHA_BITS_ARB] = self._alpha_size
		attrs[wgl.WGL_AUX_BUFFERS_ARB] = self._aux_buffers
		if self._depth_buffer:
			attrs[wgl.WGL_DEPTH_BITS_ARB] = self._depth_size
		if self._stencil_buffer:
			attrs[wgl.WGL_STENCIL_BITS_ARB] = self._stencil_size
		if self._accum_buffer:
			bits = self._accum_size
			attrs[wgl.WGL_ACCUM_RED_BITS_ARB] = bits
			attrs[wgl.WGL_ACCUM_GREEN_BITS_ARB] = bits
			attrs[wgl.WGL_ACCUM_BLUE_BITS_ARB] = bits
		return attrs
	
	def _from_win_pixelattrs(cls, attrs):
		self = cls.__new__(cls)
		self._double_buffer = attrs[wgl.WGL_DOUBLE_BUFFER_ARB]
		self._color_size = attrs[wgl.WGL_COLOR_BITS_ARB] // 3
		self._alpha_size = attrs[wgl.WGL_ALPHA_BITS_ARB]
		self._alpha = self._alpha_size > 0
		self._stereo = attrs[wgl.WGL_STEREO_ARB] #flags & wgl.PFD_STEREO != 0
		self._aux_buffers = attrs[wgl.WGL_AUX_BUFFERS_ARB] > 0
		self._depth_size = attrs[wgl.WGL_DEPTH_BITS_ARB]
		self._depth_buffer = self._depth_size > 0
		self._stencil_size = attrs[wgl.WGL_STENCIL_BITS_ARB]
		self._stencil_buffer = self._stencil_bits > 0
		self._accum_size = attrs[wgl.WGL_ACCUM_BITS_ARB] // 3
		self._accum_buffer = self._accum_size > 0
		self._multisample = False
		self._samples_per_pixel = 1
		return self
	
#	def _check_win_pixelattrs(self, attrs, mode):
#		if mode == 'screen' or mode == 'both':
#			if not attrs[wgl.WGL_DRAW_TO_WINDOW_ARB]:
#				raise GLConfigError("Rendering to screen not supported")
#		if mode == 'pixmap' or mode == 'both':
#			if not attrs[wgl.WGL_DRAW_TO_PBUFFER_ARB]:
#				raise GLConfigError("Rendering to pixmap not supported")
#		if self._alpha and attrs[wgl.WGL_ALPHA_BITS_ARB] == 0:
#			raise GLConfigError("Alpha channel not available")
#		if self._stereo and not attrs[wgl.WGL_STEREO_ARB]:
#			raise GLConfigError("Stereo buffer not available")
#		if self._aux_buffers and attrs]wgl.WGL_AUX_BUFFERS_ARB] == 0:
#			raise GLConfigError("Auxiliary buffers not available")
#		if self._depth_buffer and attrs[wgl.WGL_DEPTH_BITS_ARB] == 0:
#			raise GLConfigError("Depth buffer not available")
#		if self._stencil_buffer and attrs[wgl.WGL_STENCIL_BITS] == 0:
#			raise GLConfigError("Stencil buffer not available")
#		if self.accum_buffer and attrs[wgl.WGL_ACCUM_BITS] == 0:
#			raise GLConfigError("Accumulation buffer not available")

	_win_query_pixelattr_keys = [
		wgl.WGL_SUPPORT_OPENGL_ARB,
		wgl.WGL_DRAW_TO_WINDOW_ARB,
		wgl.WGL_DOUBLE_BUFFER_ARB,
		wgl.WGL_DRAW_TO_PBUFFER_ARB,
		wgl.WGL_STEREO_ARB,
		wgl.WGL_PIXEL_TYPE_ARB,
		wgl.WGL_COLOR_BITS_ARB,
		wgl.WGL_ALPHA_BITS_ARB,
		wgl.WGL_AUX_BUFFERS_ARB,
		wgl.WGL_DEPTH_BITS_ARB,
		wgl.WGL_STENCIL_BITS_ARB,
		wgl.WGL_ACCUM_BITS_ARB,
	]
		
	def _win_supported_pixelformat(self, hdc, mode):
		req_attrs = self._as_win_pixelattrs(mode)
		print "GLConfig: Choosing pixel format for hdc", hdc ###
		print "Requested attributes:", req_attrs ###
		req_array = WGL.attr_array(req_attrs)
		print "Requested array:", req_array ###
		ipfs, nf = wgl.wglChoosePixelFormatEXT(hdc, req_array, None, 1)
		print "Pixel formats:", ipfs ###
		print "No. of formats:", nf ###
		if not ipfs:
			req_attrs[wgl.WGL_DOUBLE_BUFFER_ARB] = not self._double_buffer
			req_array = WGL.attr_array(req_attrs)
			ipfs, nf = wglChoosePixelFormatARB(hdc, req_array, None, 1)
		if not ipfs:
			return None, None
		print "GLConfig: Describing pixel format", ipf, "for hdc", hdc ###
		keys = _win_query_pixelattr_keys
		values = wglGetPixelFormatAttribivARB(hdc, ipf, 0, keys)
		print "Actual values:", values ###
		act_attrs = WGL.attr_dict(keys, values)
		print "Actual attrs:", act_attrs ###
		return ipfs[0], act_attrs
	
	def supported(self, mode = 'both'):
		dc = win_none.GetDC()
		hdc = dc.GetSafeHdc()
		ipf, act_attrs = self._win_supported_pixelformat(hdc, mode)
		win_none.ReleaseDC(dc)
		if ipf is None:
			return None
		return GLConfig._from_win_pixelattrs(act_attrs)

#------------------------------------------------------------------------------

class GLView(GGLView):

	def __init__(self, config = None, share_group = None, **kwds):
		config = GLConfig._from_args(config, kwds)
		win = ui.CreateWnd()
		win.CreateWindow(None, None, win_style, win_default_rect,
			win_none, 0)
		dc = win.GetDC()
		hdc = dc.GetSafeHdc()
		GLContext.__init__(self, share_group, config, hdc, 'screen')
		GGLView.__init__(self, _win = win, **kwds)
		self._with_context(hdc, self._init_context)
		win.ReleaseDC(dc)
	
	def destroy(self):
		GLContext.destroy(self)
		GGLView.destroy(self)
	
	def with_context(self, proc, flush = False):
		win = self._win
		dc = win.GetDC()
		hdc = dc.GetSafeHdc()
		try:
			self._with_context(hdc, proc, flush)
		finally:
			win.ReleaseDC(dc)

	def OnPaint(self):
		#print "GLView.OnPaint" ###
		win = self._win
		dc, ps = win.BeginPaint()
		try:
			hdc = dc.GetSafeHdc()
			self._with_context(hdc, self.render, True)
		finally:
			win.EndPaint(ps)
	
	def _resized(self, delta):
		self.with_context(self._update_viewport)

#------------------------------------------------------------------------------

#class GLPixmap(GGLPixmap):
#
#	def __init__(self, width, height, config = None, share_group = None, **kwds):
#		print "GLPixmap:", width, height, kwds ###
#		config = GLConfig._from_args(config, kwds)
#		image = gdi.Bitmap(width, height)
#		self._win_image = image
#		graphics = gdi.Graphics.from_image(image)
#		self._win_graphics = graphics
#		hdc = graphics.GetHDC()
#		self._win_hdc = hdc
#		GLContext.__init__(self, share_group, config, hdc, 'pixmap')
#		self._with_context(hdc, self._init_context)
#		print "GLPixmap: done" ###
#	
#	def __del__(self):
#		graphics = self._win_graphics
#		graphics.ReleaseHDC(self._win_hdc)
#
#	def with_context(self, proc, flush = False):
#		try:
#			self._with_context(self._hdc, proc, flush)
#		finally:
#			graphics.ReleaseHDC(hdc)

#------------------------------------------------------------------------------

class GLPixmap(GGLPixmap):

	def __init__(self, width, height, config = None, share_group = None, **kwds):
		print "GLPixmap:", width, height, kwds ###
		config = GLConfig._from_args(config, kwds)
		pyhdc = gui.CreateCompatibleDC(0)
		dc = ui.CreateDCFromHandle(pyhdc)
		hdc = dc.GetSafeHdc()
		hbm = gui.CreateCompatibleBitmap(hdc, width, height)
		bm = ui.CreateBitmapFromHandle(hbm)
		dc.SelectObject(bm)
		self._win_dc = dc
		self._win_hbm = hbm
		self._win_bm = bm
		GLContext.__init__(self, share_group, config, hdc, 'pixmap')
		self._with_context(hdc, self._init_context)
		print "GLPixmap: done" ###

	def with_context(self, proc, flush = False):
		hdc = self._win_dc.GetSafeHdc()
		self._with_context(hdc, proc, flush)

#------------------------------------------------------------------------------

def win_dump_pixelformat(pf):
	print "nSize =", pf.nSize
	print "nVersion =", pf.nVersion
	print "dwFlags = 0x%08x" % pf.dwFlags
	print "iPixelType =", pf.iPixelType
	print "cColorBits =", pf.cColorBits
	print "cRedBits =", pf.cRedBits
	print "cRedShift =", pf.cRedShift
	print "cGreenBits =", pf.cGreenBits
	print "cGreenShift =", pf.cGreenShift
	print "cBlueBits =", pf.cBlueBits
	print "cBlueShift =", pf.cBlueShift
	print "cAlphaBits =", pf.cAlphaBits
	print "cAlphaShift =", pf.cAlphaShift
	print "cAccumBits =", pf.cAccumBits
	print "cAccumRedBits =", pf.cAccumRedBits
	print "cAccumGreenBits =", pf.cAccumGreenBits
	print "cAccumBlueBits =", pf.cAccumBlueBits
	print "cDepthBits =", pf.cDepthBits
	print "cStencilBits =", pf.cStencilBits
	print "cAuxBuffers =", pf.cAuxBuffers
	print "iLayerType =", pf.iLayerType
	print "bReserved =", pf.bReserved
	print "dwLayerMask =", pf.dwLayerMask
	print "dwVisibleMask =", pf.dwVisibleMask
	print "dwDamageMask =", pf.dwDamageMask
