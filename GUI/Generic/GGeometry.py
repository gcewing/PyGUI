#
#   Python GUI - Point and rectangle utilities - Generic
#

def add_pt((x1, y1), (x2, y2)):
	return (x1 + x2), (y1 + y2)

def sub_pt((x1, y1), (x2, y2)):
	return (x1 - x2), (y1 - y2)

def rect_sized((l, t), (w, h)):
	return (l, t, l + w, t + h)

def rect_left(r):
	return r[0]

def rect_top(r):
	return r[1]

def rect_right(r):
	return r[2]

def rect_bottom(r):
	return r[3]

def rect_width(r):
	return r[2] - r[0]

def rect_height(r):
	return r[3] - r[1]

def rect_topleft(r):
	return r[:2]

def rect_botright(r):
	return r[2:]

def rect_center((l, t, r, b)):
	return ((l + r) // 2, (t + b) // 2)

def rect_size((l, t, r, b)):
	return (r - l, b - t)

def union_rect((l1, t1, r1, b1), (l2, t2, r2, b2)):
	return (min(l1, l2), min(t1, t2), max(r1, r2), max(b1, b2))

def sect_rect((l1, t1, r1, b1), (l2, t2, r2, b2)):
	return (max(l1, l2), max(t1, t2), min(r1, r2), min(b1, b2))

def inset_rect((l, t, r, b), (dx, dy)):
	return (l + dx, t + dy, r - dx, b - dy)

def offset_rect((l, t, r, b), (dx, dy)):
	return (l + dx, t + dy, r + dx, b + dy)

def offset_rect_neg((l, t, r, b), (dx, dy)):
	return (l - dx, t - dy, r - dx, b - dy)

def empty_rect((l, t, r, b)):
	return r <= l or b <= t

def pt_in_rect((x, y), (l, t, r, b)):
	return l <= x < r and t <= y < b

def rects_intersect((l1, t1, r1, b1), (l2, t2, r2, b2)):
	return l1 < r2 and l2 < r1 and t1 < b2 and t2 < b1

def rect_with_center((l, t, r, b), (x, y)):
	w = r - l
	h = b - t
	rl = x - w // 2
	rt = y - h // 2
	return (rl, rt, rl + w, rt + h)
