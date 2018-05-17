#
#   PyGUI - OpenGL Display Lists - Generic
#

from weakref import WeakKeyDictionary
from OpenGL.GL import glGenLists, glNewList, glEndList, glCallList, \
	glDeleteLists, GL_COMPILE
from GUI.Properties import Properties, overridable_property
from GUI.GGLContexts import current_share_group

#----------------------------------------------------------------------

class DisplayListIdMap(WeakKeyDictionary):

	def __del__(self):
		#  Delete any display lists that have been allocated for this map.
		#print "GL.DisplayListIdMap.__del__:", self ###
		def free_display_list():
			glDeleteLists(gl_id, 1)
		for share_group, gl_id in self.items():
			context = share_group._some_member()
			if context:
				#print "...freeing display list id", gl_id, "for", share_group, "using", context ###
				context.with_context(free_display_list)

#----------------------------------------------------------------------

class DisplayList(Properties):
	"""This class encapsulates an OpenGL display list and maintains a
	representation of it for each OpenGL context with which it is used.
	Allocation and maintentance of display list numbers is handled
	automatically."""
	#
	#   _gl_id   ShareGroup -> int   Mapping from OpenGL share group to
	#                                display list number
	
	setup = overridable_property('setup',
		"""Function to set up the display list by making the necessary
		OpenGL calls, excluding glNewList and glEndList.""")
	
	def __init__(self, setup = None):
		self._gl_id = DisplayListIdMap()
		self._setup = setup
	
	def deallocate(self):
		"""Deallocate any OpenGL resources that have been allocated for this
		display list in any context."""
		self._gl_id.__del__()

	def get_setup(self):
		return self._setup
	
	def set_setup(self, x):
		self._setup = x
	
	def call(self):
		"""Calls the display list using glCallList(). If this display list
		has not previously been used with the current context, allocates
		a display list number and arranges for do_setup() to be called
		to compile a representation of the display list."""
		share_group = current_share_group()
		gl_id = self._gl_id.get(share_group)
		if gl_id is None:
			gl_id = glGenLists(1)
			#print "GLDisplayList: assigned id %d for %s in share group %s" % (
			#	gl_id, self, share_group) ###
			self._gl_id[share_group] = gl_id
			call_when_not_compiling_display_list(lambda: self._compile(gl_id))
		glCallList(gl_id)
	
	def _compile(self, gl_id):
		global compiling_display_list
		compiling_display_list = True
		glNewList(gl_id, GL_COMPILE)
		try:
			self.do_setup()
		finally:
			glEndList()
			compiling_display_list = False

	def do_setup(self):
		"""Make all the necessary OpenGL calls to compile the display list,
		except for glNewList() and glEndList() which will be called automatically
		before and after. The default implementation calls the 'setup' property."""
		setup = self._setup
		if setup:
			setup()
		else:
			raise NotImplementedError(
				"No setup function or do_setup method for GL.DisplayList")


compiling_display_list = False
pending_functions = []

def call_when_not_compiling_display_list(func):
	#print "GLDisplayLists: entering call_when_not_compiling_display_list" ###
	if compiling_display_list:
		#print "GLDisplayLists: deferring", func ###
		pending_functions.append(func)
	else:
		#print "GLDisplayLists: immediately calling", func ###
		func()
		while pending_functions:
			#print "GLDisplayLists: calling deferred", func ###
			pending_functions.pop()()
	#print "GLDisplayLists: exiting call_when_not_compiling_display_list" ###
