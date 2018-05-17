#
#   TextViews
#

from math import floor
from Views import View
from Colors import Color
from Fonts import application_font
from Applications import application

class TextView(View):
  """A TextView provides an editable view of
  a TextModel."""

  _fg = Color(0, 0, 0)
  _bg = Color(1, 1, 1)
  _font = application_font()
  _line_height = _font.height()
  _ascent = _font.ascent()
  _left_margin = 5
  _right_margin = 5
  _top_margin = 5
  _bottom_margin = 5
  _caret_on = 1
  _caret_rect = None

  def __init__(self, *args, **kw):
    apply(View.__init__, (self,) + args, kw)
    self.update_caret_rect()

  #
  #   Properties
  #

  def font(self):
    "Return the font property."
    return self._font

  def set_font(self, f):
    "Set the font property."
    self._font = f
    self._line_height = f.height()
    self._ascent = f.ascent()
    self.update_extent()
    self.update_caret_rect()

  def margins(self):
    "Return the text margins."
    return (self._left_margin, self._top_margin,
	    self._right_margin, self._bottom_margin)

  def set_margins(self, l, t, r, b):
    "Set the text margins."
    self._left_margin = l
    self._top_margin = t
    self._right_margin = r
    self._bottom_margin = b
    self.update_extent()
    self.update_caret_rect()
    self.invalidate()

  #
  #   Callbacks
  #

  def draw(self, c):
    debug = 0
    if debug:
      print "TextView.draw:" ###
    text = self.model()
    sel_start, sel_end = text.selection()
    sel_start_line, sel_start_col = sel_start
    sel_end_line, sel_end_col = sel_end
    text_end_line, text_end_col = text.end()
##     if sel_start == sel_end and self._caret_on:
##       caret_line = sel_start_line
##     else:
##       caret_line = None
    (minx, miny), (maxx, maxy) = self.viewed_rect()
    min_line = max(self.y_to_line(miny), 0)
    max_line = min(self.y_to_line(maxy) + 1, text_end_line)
    fg = self._fg
    bg = self._bg
    c.set_font(self._font)
    #ext_right = self.extent_right()
    #ext_bottom = self.extent_bottom()
    #hilite_right_edge = self.viewed_rect()[1][0]
    right, bottom = self.viewed_rect()[1]
    top_margin = self._top_margin
    left_margin = self._left_margin
    bottom_margin = self._bottom_margin
    line_height = self._line_height
    ascent = self._ascent
    if debug:
      print "...min_line =", min_line
      print "...max_line =", max_line
##       print "...caret_line =", caret_line
      print "...line_height =", line_height
    # Erase top and left margin area
    c.set_forecolor(bg)
    c.fill_rect(((0, 0), (right, top_margin)))
    c.fill_rect(((0, top_margin), (left_margin, bottom)))
    # Draw relevant lines
    y = top_margin
    for line in xrange(min_line, max_line + 1):
      if debug:
        print "...drawing line", line
      chars = text.line(line)
      line_end_col = len(chars)
      if line == sel_start_line:
        hilite_start_col = sel_start_col
      elif line > sel_start_line:
        hilite_start_col = 0
      else:
        hilite_start_col = line_end_col
      if line == sel_end_line:
        hilite_end_col = sel_end_col
      elif line < sel_end_line:
        hilite_end_col = line_end_col
      else:
        hilite_end_col = 0
      hilite_to_eol = line >= sel_start_line and line < sel_end_line
      if debug:
        print "......hilite_start_col =", hilite_start_col ###
        print "......hilite_end_col =", hilite_end_col ###
        print "......line_end_col =", line_end_col ###
      x = left_margin
      #base = y + ascent
      # Draw chars before hilite
      if hilite_start_col > 0:
        x = self.draw_chars(
          c, chars, x, y, 0, hilite_start_col, fg, bg)
##       if line == caret_line:
##         caret_x = x
##         if debug:
##           print "......caret_x =", caret_x
      # Draw hilited chars
      if hilite_start_col < hilite_end_col:
        x = self.draw_chars(
          c, chars, x, y, hilite_start_col, hilite_end_col, bg, fg)
      # Draw chars after hilite
      if hilite_end_col < line_end_col:
        x = self.draw_chars(
          c, chars, x, y, hilite_end_col, line_end_col, fg, bg)
##       # Draw caret
##       if line == caret_line:
##         if debug:
##           print "......drawing caret at", (caret_x, y)
##         c.set_forecolor(fg)
##         c.fill_rect(((caret_x, y), (caret_x + 1, y + line_height)))
      # Erase to end of line
      if x < right:
        if hilite_to_eol:
          c.set_forecolor(fg)
        else:
          c.set_forecolor(bg)
        r = ((x, y), (right, y + line_height))
        if debug:
          print "...erasing", r ###
        c.fill_rect(r)
      y = y + line_height
    # Erase to bottom of extent
    c.fill_rect(((0, y), (right, bottom)))
    # Draw caret
    if self._caret_on:
      r = self._caret_rect
      if r:
        c.set_forecolor(fg)
        c.fill_rect(r)

  def draw_chars(self, c, line, x, y, start_col, end_col, fg, bg):
    debug = 0
    if debug:
      print ".........TextView.draw_chars:", \
            repr(line), "at", (x, y), "col", start_col, "to", end_col ###
      print "............using", fg, "on", bg ###
    chars = line[start_col:end_col]
    w = self._font.width(chars)
    c.set_forecolor(bg)
    c.fill_rect(((x, y), (x + w, y + self._line_height)))
    c.set_forecolor(fg)
    c.set_backcolor(bg)
    c.moveto(x, y + self._ascent)
    c.show(chars)
    return x + w


  def line_to_y(self, line):
    return self._top_margin + line * self._line_height

  def col_to_x(self, line, col):
    return self._left_margin + self._font.width(self.model().line(line)[:col])

  def y_to_line(self, y):
    #print "TextView.y_to_line:", y
    #print "...self._top_margin =", self._top_margin
    #print "...self._line_height =", self._line_height
    return int((y - self._top_margin) / self._line_height)

  def x_to_col(self, line, x):
    chars = self.model().line(line)
    if chars is not None:
      return self._font.x_to_pos(chars, x - self._left_margin)
    else:
      return 0

  def pt_to_pos(self, (x, y)):
    text = self.model()
    line = self.y_to_line(y)
    if line < 0:
      return (0, 0)
    elif line < text.num_lines():
      col = self.x_to_col(line, x)
      return (line, col)
    else:
      return text.end()
    
  def selection_changed(self, (line1, col1), (line2, col2)):
    top = self.line_to_y(line1)
    if line1 == line2:
      left = self.col_to_x(line1, col1)
      right = self.col_to_x(line1, col2)
      bottom = top + self._line_height
    else:
      left = self.extent_left()
      right = self.extent_right()
      bottom = self.line_to_y(line2 + 1)
    self.invalidate_rect(((left, top), (right, bottom)))
    self.update_caret_rect()

  def text_changed(self, (line, col), multiline):
    self.update_extent()
    top = self.line_to_y(line)
    right = self.extent_right()
    if not multiline:
      left = self.col_to_x(line, col)
      bottom = top + self._line_height
    else:
      left = self.extent_left()
      bottom = self.viewed_rect()[1][1]
    if top < bottom:
      self.invalidate_rect(((left, top), (right, bottom)))

  def click(self, e):
    text = self.model()
    pos1 = self.pt_to_pos(e.where())
    #print "TextView.click: pos1=", pos1
    text.set_selection(pos1, pos1)
    while self.track_mouse():
      pos2 = self.pt_to_pos(self.get_mouse().where())
      #print "TextView.click: pos2=", pos2
      text.set_selection(pos1, pos2)

  def key(self, e):
    c = e.char
    if c == '\b' or c == '\177':
      self.backspace()
    else:
      if c == '\r':
        c = '\n'
      self.insert(c)

  def update_extent(self):
    text = self.model()
    max_line, _ = text.end()
    width = text.max_line_length() * self._font.width("m")
    height = (max_line + 1) * self._line_height
    self.set_extent(
      ((0, 0), (self._left_margin + width + self._right_margin,
                self._top_margin + height + self._bottom_margin)))

  #
  #   Caret
  #

  def blink(self):
    #print "TextView.blink" ###
    self.set_caret(not self._caret_on)

  def set_caret(self, on):
    # print "TextView.set_caret:", on ###
    self._caret_on = on
    r = self._caret_rect
    if r:
      #print "...invalidating", r ###
      self.invalidate_rect(r)

  def update_caret_rect(self):
    old_r = self._caret_rect
    text = self.model()
    sel_start, sel_end = text.selection()
    if sel_start == sel_end:
      line, col = sel_start
      #print "TextView.update_caret_rect:" ###
      #print "...line =", line ###
      #print "...line_height =", self._line_height ###
      y = self.line_to_y(line)
      x = self.col_to_x(line, col)
      new_r = ((x - 1, y), (x, y + self._line_height))
    else:
      new_r = None
    if old_r <> new_r:
      if old_r:
        self.invalidate_rect(old_r)
      if new_r:
        self.invalidate_rect(new_r)
      self._caret_rect = new_r
      self.set_caret(1)
      self.reset_blink()

  #
  #   Menu commands
  #

  def setup_menus(self, m):
    text = self.model()
    start, end = text.selection()
    if start <> end:
      m.enable('cut_cmd')
      m.enable('copy_cmd')
      m.enable('clear_cmd')
    if application().clipboard():
      m.enable('paste_cmd')
    View.setup_menus(self, m)

  def cut_cmd(self):
    self.copy_cmd()
    self.clear_cmd()

  def copy_cmd(self):
    text = self.model()
    start, end = text.selection()
    chars = text.chars(start, end)
    #print "TextView.copy_cmd: chars =", repr(chars) ###
    application().set_clipboard(chars)

  def paste_cmd(self):
    self.insert(str(application().clipboard()))

  def clear_cmd(self):
    self.insert("")

  #
  #   Text modification
  #

  def insert(self, chars):
    """Replace selection with the given chars and position insertion
    point just after the inserted chars."""
    text = self.model()
    text.replace_selection(chars)
    _, end = text.selection()
    text.set_selection(end, end)

  def backspace(self):
    """Delete the selection, or if the selection is empty, delete
    the character just before the selection, if any."""
    text = self.model()
    start, end = text.selection()
    if start == end:
      if start <> (0, 0):
        line, col = start
        if col > 0:
          col = col - 1
        else:
          line = line - 1
          col = len(text.line(line))
        start = (line, col)
        text.set_chars(start, end, "")
        text.set_selection(start, start)
    else:
      self.clear_cmd()

