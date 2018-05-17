#
#		Python GUI - Windows - Generic
#

import Exceptions
from GUI.Properties import overridable_property
from GUI import Container
from GUI import application

class Window(Container):
	"""Top-level Container."""
	
	menus = overridable_property('menus', "Menus to be available when this window is active.")
	document = overridable_property('document', "Document with which this window is associated.")
	title = overridable_property('title', "Title of the window.")
	auto_position = overridable_property('auto_position', "Whether to position automatically when first shown.")	
	target = overridable_property('target', "Current target for key events and menu messages.")
	tab_chain = overridable_property('tab_chain', "List of subcomponents in tabbing order.")
	visible = overridable_property('visible', "Whether the window is currently shown.")	

	keeps_document_open = True

	_default_width = 200
	_default_height = 200
	_modal_styles = ('modal_dialog', 'alert')
	_dialog_styles = ('nonmodal_dialog', 'modal_dialog', 'alert')
	
	_menus = []
	_document = None
	_closable = 0
	_auto_position = True
	_tab_chain = None

	def __init__(self, style = 'standard', closable = None, **kwds):
		if closable is None:
			raise Exceptions.InternalError(
				"'closable' parameter unspecified in call to generic Window.__init__")
		Container.__init__(self, **kwds)
		self._style = style
		self._dialog_style = style.find('dialog') >= 0
		self._closable = closable
		application()._add_window(self)

	def destroy(self):
		"""Detaches the window from document and application and removes it
		from the screen."""
		self.set_document(None)
		application()._remove_window(self)
		Container.destroy(self)

	#
	#		Message handling
	#

	def next_handler(self):
		if self._document:
			return self._document
		else:
			return application()
	
	def dispatch(self, message, *args):
		self.target.handle(message, *args)

	#
	#		Menus
	#
	
	def get_menus(self):
		return self._menus

	def set_menus(self, x):
		self._menus = x

	#
	#		Document association
	#
	
	def get_document(self):
		return self._document
	
	def set_document(self, x):
		if self._document != x:
			if self._document:
				self._document._windows.remove(self)
			self._document = x
			if self._document:
				self._document._windows.append(self)
				self.update_title()

	#
	#		Title
	#
	
	def update_title(self):
		"""Update the window's title after a change in its document's title."""
		doc = self._document
		if doc:
			self.set_title(doc.title)
	
	#
	#   Showing and Positioning
	#
	
	def get_auto_position(self):
		return self._auto_position
	
	def set_auto_position(self, v):
		self._auto_position = v
	
	def center(self):
		"""Position the window in the centre of the screen."""
		sl, st, sr, sb = self._screen_rect()
		w, h = self.size
		l = (sr - sl - w) // 2
		t = (sb - st - h) // 2
		self.position = (l, t)
	
	def centre(self):
		self.center()

	def show(self):
		if self._auto_position:
			if self._style == 'standard':
				self._stagger()
			else:
				self.center()
			self._auto_position = False
		self._show()
	
	def _stagger(self):
		pass
	
	def _show(self):
		self.visible = True

	def hide(self):
		self.visible = False

	#
	#		Menu commands
	#

	def setup_menus(self, m):
		Container.setup_menus(self, m)
		app = application()
		if self._closable:
			m.close_cmd.enabled = 1

	def close_cmd(self):
		"""If this window is the only window belonging to a document
		whose keeps_document_open attribute is true, then close the
		document, else destroy the window."""
#		app = application()
#		if not app._may_close_a_window():
#			#print "GWindow.close_cmd: Quitting the application" ###
#			app.quit_cmd()
#		else:
		doc = self._document
		n = 0
		if doc:
			for win in doc._windows:
				if win is not self and win.keeps_document_open:
					n += 1
		if doc and n == 0:
			doc.close_cmd()
		else:
			self.destroy()
	
	#
	#   Tabbing
	#
	
	def get_tab_chain(self):
		chain = self._tab_chain
		if chain is None:
			chain = []
			self._build_tab_chain(chain)
			self._tab_chain = chain
		#print "Window.get_tab_chain:", chain ###
		return chain
	
	def _invalidate_tab_chain(self):
		self._tab_chain = None
	
	def _tab_to_next(self):
		self._tab_to(1)
	
	def _tab_to_prev(self):
		self._tab_to(-1)

	def _tab_to(self, direction):
		print "GWindow._tab_to:", direction ###
		chain = self.tab_chain
		if chain:
			old_target = application().target
			new_target = None
			n = len(chain)
			try:
				i = chain.index(old_target)
			except ValueError:
				if direction > 0:
					i = -1
				else:
					i = n
			k = n
			while k:
				k -= 1
				i = (i + direction) % n
				comp = chain[i]
				if comp._is_targetable():
					new_target = comp
					break
			if new_target:
				if old_target:
					old_target._tab_out()
				new_target._tab_in()

	def key_down(self, event):
		#print "GWindow.key_down:", event
		if self._generic_tabbing and event.char == '\t':
			#print "GWindow.key_down: doing generic tabbing"
			if event.shift:
				self._tab_to_prev()
			else:
				self._tab_to_next()
		else:
			Container.key_down(self, event)

	#
	#   Other
	#
	
	def get_window(self):
		return self

	def first_dispatcher(self):
		return self

	def _document_needs_saving(self, state):
		pass

	def modal_event_loop(self):
		"""Loop reading and handling events for the given window until
		exit_event_loop() is called. Interaction with other windows is prevented
		(although enabled application-wide menu commands can be used)."""
		#  Implementations can override this together with exit_modal_event_loop()
		#  to implement modal event loops in a different way.
		application()._event_loop(self)
	
	def exit_modal_event_loop(self):
		#  Cause the current call to modal_event_loop() to exit.
		application()._exit_event_loop()
