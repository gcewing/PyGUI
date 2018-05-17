#------------------------------------------------------------------------------
#
#   PyGUI - OpenGL - Win32
#
#------------------------------------------------------------------------------

import win32con as wc, win32ui as ui, win32gui as gui
#import OpenGL.GL as gl ###
import GUI.GDIPlus as gdi
from OpenGL import WGL as wgl
from OpenGL.WGL import ChoosePixelFormat
#print "Using ctypes ChoosePixelFormat"
#from WGL import ChoosePixelFormat
from GUI.WinUtils import win_none
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

	def _as_win_pixelformat(self, mode):
		#print "GLConfig._as_win_pixelformat: mode =", mode ###
		pf = wgl.PIXELFORMATDESCRIPTOR()
		flags = wgl.PFD_SUPPORT_OPENGL
		if mode == 'screen' or mode == 'both':
			#print "GLConfig: requesting screen drawing" ###
			flags |= wgl.PFD_DRAW_TO_WINDOW
			if self._double_buffer:
				flags |= wgl.PFD_DOUBLEBUFFER | wgl.PFD_SWAP_EXCHANGE
		else:
			flags |= wgl.PFD_DOUBLEBUFFER_DONTCARE
		if mode == 'pixmap' or mode == 'both':
			#print "GLConfig: requesting pixmap drawing" ###
			flags |= wgl.PFD_DRAW_TO_BITMAP | wgl.PFD_SUPPORT_GDI
		if not self._depth_buffer:
			flags |= wgl.PFD_DEPTH_DONTCARE
		if self._stereo:
			flags |= wgl.PFD_STEREO
		else:
			flags |= wgl.PFD_STEREO_DONTCARE
		pf.dwFlags = flags & 0xffffffff
		pf.iPixelType = wgl.PFD_TYPE_RGBA
		#pf.cColorBits = 3 * self._color_size
		#pf.cColorBits = 32 ###
		pf.cRedBits = pf.cGreenBits = pf.cBluedBits = self._color_size
		if self._alpha:
			pf.cAlphaBits = self._alpha_size
		pf.cAuxBuffers = self._aux_buffers
		if self._depth_buffer:
			pf.cDepthBits = self._depth_size
		if self._stencil_buffer:
			pf.cStencilBits = self._stencil_size
		if self._accum_buffer:
			pf.cAccumBits = 3 * self._accum_size
		pf.iLayerType = wgl.PFD_MAIN_PLANE
		return pf
	
	def _from_win_pixelformat(cls, pf):
		self = cls.__new__(cls)
		flags = pf.dwFlags
		self._double_buffer = flags & wgl.PFD_DOUBLEBUFFER != 0
		self._alpha = pf.cAlphaSize > 0
		self._color_size = pf.cColorBits
		self._alpha_size = pf.cAlphaSize
		self._stereo = flags & wgl.PFD_STEREO != 0
		self._aux_buffers = pf.cAuxBuffers
		self._depth_buffer = pf.cDepthBits > 0
		self._depth_size = pf.cDepthBits
		self._stencil_buffer = pf.cStencilBits > 0
		self._stencil_size = pf.cStencilBits
		self._accum_size = pf.cAccumBits
		self._accum_buffer = self._accum_size > 0
		self._multisample = False
		self._samples_per_pixel = 1
		return self
	
	def _check_win_pixelformat(self, pf, mode):
		flags = pf.dwFlags
		if mode == 'screen' or mode == 'both':
			if not flags & wgl.PFD_DRAW_TO_WINDOW:
				raise GLConfigError("Rendering to screen not supported")
		if mode == 'pixmap' or mode == 'both':
			if not flags & wgl.PFD_DRAW_TO_BITMAP:
				raise GLConfigError("Rendering to pixmap not supported")
		if self._alpha and pf.cAlphaBits == 0:
			raise GLConfigError("Alpha channel not available")
		if self._stereo and not flags & wgl.PFD_STEREO:
			raise GLConfigError("Stereo buffer not available")
		if self._aux_buffers and pf.cAuxBuffers == 0:
			raise GLConfigError("Auxiliary buffers not available")
		if self._depth_buffer and pf.cDepthBits == 0:
			raise GLConfigError("Depth buffer not available")
		if self._stencil_buffer and pf.cStencilBits == 0:
			raise GLConfigError("Stencil buffer not available")
		if self.accum_buffer and pf.cAccumBits == 0:
			raise GLConfigError("Accumulation buffer not available")
		
	def _win_supported_pixelformat(self, hdc, mode):
		reqpf = self._as_win_pixelformat(mode)
		#print "GLConfig._win_supported_pixelformat" ###
		#print "Requested format:" ###
		#win_dump_pixelformat(reqpf) ###
		#print "GLConfig: Choosing pixel format for hdc", hdc ###
		ipf = wgl.ChoosePixelFormat(hdc, reqpf)
		#print "... result =", ipf ###
		actpf = wgl.PIXELFORMATDESCRIPTOR()
		#print "GLConfig: Describing pixel format", ipf, "for hdc", hdc ###
		wgl.DescribePixelFormat(hdc, ipf, actpf.nSize, actpf)
		#print "Actual format:" ###
		#win_dump_pixelformat(actpf) ###
		return ipf, actpf
	
	def supported(self, mode = 'both'):
		dc = win_none.GetDC()
		hdc = dc.GetSafeHdc()
		ipf, actpf = self._win_supported_pixelformat(hdc, mode)
		win_none.ReleaseDC(dc)
		return GLConfig._from_win_pixelformat(actpf)

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
		GGLView.__init__(self, _win = win)
		self.set(**kwds)
		self._with_context(hdc, self._init_context)
		win.ReleaseDC(dc)
	
#	def _init_context(self):
#		print "GL_VENDOR:", gl.glGetString(gl.GL_VENDOR)
#		print "GL_RENDERER:", gl.glGetString(gl.GL_RENDERER)
#		print "GL_VERSION:", gl.glGetString(gl.GL_VERSION)
#		print "GL_EXTENSIONS:"
#		for name in gl.glGetString(gl.GL_EXTENSIONS).split():
#			print "   ", name
#		GGLView._init_context(self)
	
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
			self._with_context(hdc, self._render, True)
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
		#print "GLPixmap:", width, height, kwds ###
		config = GLConfig._from_args(config, kwds)
		dc0 = win_none.GetDC()
		dc = dc0.CreateCompatibleDC(dc0)
		bm = ui.CreateBitmap()
		bm.CreateCompatibleBitmap(dc0, width, height)
		win_none.ReleaseDC(dc0)
		dc.SelectObject(bm)
		self._win_dc = dc
		self._win_bm = bm
		hdc = dc.GetSafeHdc()
		win_dump_bitmap(bm) ###
		GLContext.__init__(self, share_group, config, hdc, 'pixmap')
		self._with_context(hdc, self._init_context)
		#print "GLPixmap: done" ###

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

def win_dump_bitmap(bm):
	info = bm.GetInfo()
	print "bmType =", info['bmType']
	print "bmWidth =", info['bmWidth']
	print "bmHeight =", info['bmHeight']
	print "bmWidthBytes =", info['bmWidthBytes']
	print "bmPlanes =", info['bmPlanes']
	print "bmBitsPixel =", info['bmBitsPixel']

	