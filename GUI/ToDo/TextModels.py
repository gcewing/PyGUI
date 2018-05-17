#
#   TextModels
#

import string
from array import array
from Models import Model

class TextModel(Model):
  """A TextModel is a Model holding a character string
  suitable for viewing and editing with a TextView."""

  _text = None
  _sel_start = (0, 0)
  _sel_end = (0, 0)

  #
  #   The text is kept in a list of strings. There is an
  #   implicit newline at the end of every string except the
  #   last one. There is always at least one string in the
  #   list; a completely empty text is represented by a
  #   list containing one empty string.
  #
  #   Positions in the text are represented by a tuple
  #   (line, col), where line is the line number (0-based)
  #   and col is the position within the line (0 to the
  #   number of characters in the line).
  #
  #   Pieces of text to be inserted or extracted are
  #   represented as simple strings, with lines separated
  #   by newlines.
  #
  #   Views may be sent the messages:
  #
  #      text_changed(start_pos, multiline)
  #         where start_pos is the start of the affected text and
  #         multiline is true if more than one line is affected.
  #
  #      selection_changed(pos1, pos2)
  #         where pos1 and pos2 are the extremes of the range
  #         of text affected.
  #

  def __init__(self, *args, **kw):
    apply(Model.__init__, (self,)+args, kw)
    self._text = [""]

  def text(self):
    "Return the whole text as a string."
    return string.join(self._text, '\n')

  def set_text(self, s):
    "Replace the whole text with a string."
    return self.set_chars((0, 0), self.end(), s)

  def num_lines(self):
    "Return the number of lines."
    return len(self._text)

  def line(self, i):
    """Return the specified line as a string, without any trailing newline"""
    return self._text[i]

  def end(self):
    "Return the ending position of the text."
    lines = self._text
    return (len(lines) - 1, len(lines[-1]))
    
  def char(self, (line, col)):
    "Return the character at (line, col)."
    return self._text[line][col]

  def chars(self, (line1, col1), (line2, col2)):
    "Return the text between (line1, col1) and (line2, col2)."
    text = self._text
    if line1 == line2:
      return text[line1][col1:col2]
    else:
      a = text[line1][col1:]
      b = text[line1 + 1 : line2 - 1]
      c = text[line2][:col2]
      return string.joinfields([a] + b + [c], '\n')

##   def set_char(self, (line, col), c):
##     "Replace the character at (line, col)."
##     self._text[line][col] = c
##     self.notify_views('char_changed', (line, col))

  def set_chars(self, (line1, col1), (line2, col2), s):
    """Replace the text between (line1, col1) and (line2, col2).
    Returns the line and column of the new endpoint of the
    inserted text."""
    #print "TextModel.set_chars", (line1, col1), (line2, col2), repr(s) ###
    text = self._text
    #print "...old text =", repr(text) ###

    # Step 1: Delete old text
    if line1 == line2:
      line = text[line1]
      text[line1] = line[:col1] + line[col2:]
    else:
      text[line1 : line2 + 1] = [text[line1][:col1] + text[line2][col2:]]
      #a = text[line1][:col1]
      #b = text[line2][col2:]
      #text[line1 : line2 + 1] = [a + b]

    # Step 2: Insert new text
    ss = string.splitfields(s, '\n')
    line = text[line1]
    if len(ss) == 1:
      text[line1] = line[:col1] + ss[0] + line[col1:]
    else:
      text[line1 : line1 + 1] = (
        [line[:col1] + ss[0]] +
        ss[1:-1] +
        [ss[-1] + line[col1:]])
    
    # Step 3: Calculate new endpoint
    #print "...ss =", repr(ss) ###
    if len(ss) == 1:
      line3 = line1
      col3 = col1 + len(s)
    else:
      line3 = line1 + len(ss) - 1
      col3 = len(ss[-1])
    new_end = (line3, col3)
    #print "...new_end =", new_end
    #print "...new text:", self._text
    multiline = line2 <> line1 and line3 <> line1
    self.notify_views('text_changed', (line1, col1), multiline)
    self.set_selection(self._sel_start,
                       self.min_pos(self._sel_end, new_end))
    return new_end

  def selection(self):
    "Return the endpoints of the current selection."
    return (self._sel_start, self._sel_end)

  def set_selection(self, new_start, new_end):
    "Set the endpoints of the current selection."
    new_start, new_end = self.normalise_range(new_start, new_end)
    old_start = self._sel_start
    old_end = self._sel_end
    if old_start <> new_start or old_end <> new_end:
      self._sel_start = new_start
      self._sel_end = new_end
      self.notify_views('selection_changed',
                        self.min_pos(old_start, new_start),
                        self.max_pos(old_end, new_end))

  def replace_selection(self, new_text):
    "Replace the selected text with the given string."
    new_end = self.set_chars(self._sel_start, self._sel_end, new_text)
    self.set_selection(self._sel_start, new_end)
    #print "TextModels.replace_selection: selection =", ( ###
    #  self._sel_start, self._sel_end) ###

  def max_line_length(self):
    "Return the number of characters in the longest line."
    return max(map(len, self._text))

  #
  #   Internal
  #

  def min_pos(self, pos1, pos2):
    line1, col1 = pos1
    line2, col2 = pos2
    if line1 < line2 or (line1 == line2 and col1 < col2):
      return pos1
    else:
      return pos2

  def max_pos(self, pos1, pos2):
    line1, col1 = pos1
    line2, col2 = pos2
    if line1 > line2 or (line1 == line2 and col1 > col2):
      return pos1
    else:
      return pos2

  def normalise_range(self, pos1, pos2):
    "Order two positions so that pos1 <= pos2."
    return self.min_pos(pos1, pos2), self.max_pos(pos1, pos2)
