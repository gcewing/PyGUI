#------------------------------------------------------------------------------
#
#   PyGUI - GLContext - Win32
#
#------------------------------------------------------------------------------

import OpenGL as gl
from OpenGL import WGL as wgl
import WGL
from GUI.GGLContexts import GLContext as GGLContext

class GLContext(GGLContext):
	#  _win_context  WGL context
	#  _win_dblbuf   Is double buffered
	
	def __init__(self, share_group, config, hdc, mode):
		print "GLContext: mode =", mode ###
		GGLContext.__init__(self, share_group)
		shared_context = self._get_shared_context()
		if shared_context:
			share_ctx = shared_context._win_context
		else:
			share_ctx = None
		ipf, act_attrs = config._win_supported_pixelformat(hdc, mode)
		if ipf is None:
			raise GLConfigError
		#config._check_win_pixelattrs(act_attrs, mode)
		print "GLContext: Setting pixel format", ipf, "for hdc", hdc ###
		WGL.SetPixelFormat(hdc, ipfs)
		ctx = wgl.wglCreateContext(hdc)
		if share_ctx:
			wgl.wglShareLists(share_ctx, ctx)
		self._win_context = ctx
		self._win_dblbuf = actpf.dwFlags & wgl.PFD_DOUBLEBUFFER != 0
	
	def destroy(self):
		wgl.wglDeleteContext(self._win_context)
	
	def _with_context(self, hdc, proc, flush = False):
		old_hdc = wgl.wglGetCurrentDC()
		old_ctx = wgl.wglGetCurrentContext()
		result = wgl.wglMakeCurrent(hdc, self._win_context)
		try:
			self._with_share_group(proc)
			if flush:
				if self._win_dblbuf:
					wgl.SwapBuffers(hdc)
				else:
					gl.glFlush()
		finally:
			wgl.wglMakeCurrent(old_hdc, old_ctx)
	