import io
import struct
import array
import os
import curses
import curses.textpad
import random
from gzip import GzipFile

import gamedata
import keymaps

def decypher(inp_x, inp_y, bb, name, dim, length):
	L = (inp_x) * (dim) * length + (inp_y) * length + 8
	try:
		bb.seek(L)
	except ValueError:
		bb.seek(0)
	try:
		u = struct.unpack('{}B'.format(length), bb.read(length))
	except struct.error:
		bb.seek(0)
		u = struct.unpack('{}B'.format(length), bb.read(length))
	byte_array = list(u)

	if inp_x < 0 or  inp_x > dim + 1:
		return

	if inp_y < 0 or inp_y > dim - 1:
		return
	
	decyph_dict = getattr(gamedata, name.strip(" "))
	data_array = [0 for x in range(len(byte_array))]
	
	for i in range(len(byte_array)):
		try:
			data_array[i] = decyph_dict[str(i)][str(byte_array[i])]
		except KeyError:
			pass
	return data_array, byte_array, L

def display(height, width, colors, display_mode, edit_mode, stdscr, name, dim, length, inp_x, inp_y, bb):
	col1 = colors["col1"]
	col2 = colors["col2"]
	
	#inp_x = 2 * inp_x
	
	pad_mp = curses.newpad(height - 3, width)
	if edit_mode == 0:
		pad_mp.bkgd(" ", col1)
	if edit_mode == 1:
		pad_mp.bkgd(" ", col2)
	
	center_x = width // 2
	if height // 2 * 2 < height:
		center_y = height // 2 
	else:
		center_y = height // 2 - 1
	
	for x in range(-center_x , +center_x, 2):
		for y in range(-center_y , +center_y):
			i = (inp_x * 2  + x) // 2
			j = inp_y - y
			if (y == 0) and ( x == 1 or x == 2):
				pad_mp.attron(curses.A_REVERSE)
			else:
				pad_mp.attroff(curses.A_REVERSE)
			try:
				map_data = decypher(i, j, bb, name, dim, length)[0]
				try:
					if (map_data[0]["anim"] == 1) and (display_mode == 0) and (edit_mode == 0):
						if round(random.uniform(0,100)) >= map_data[0]["anim_rat"]:
							pad_mp.addch(center_y + y , center_x + x , map_data[0]["sym"])
							pad_mp.addch(center_y + y , center_x + x + 1 , map_data[0]["sym2"])
								
						else:
							pad_mp.addch(center_y + y , center_x + x , map_data[0]["sym_anim"], curses.A_BOLD)
							pad_mp.addch(center_y + y , center_x + x + 1 , map_data[0]["sym_anim"], curses.A_BOLD)
								
					else:
						if map_data[0]["shift"] == 1:
							if y // 2 * 2 < y and inp_y // 2 * 2 < inp_y:
								pad_mp.addstr(center_y + y , center_x + x , map_data[display_mode]["sym"])
								pad_mp.addstr(center_y + y , center_x + x + 1 , map_data[display_mode]["sym2"])
							if y // 2 * 2 == y and inp_y // 2 * 2 < inp_y:
								pad_mp.addstr(center_y + y , center_x + x + 1 , map_data[display_mode]["sym"])
								pad_mp.addstr(center_y + y , center_x + x , map_data[display_mode]["sym2"])
							if y // 2 * 2 == y and inp_y // 2 * 2 == inp_y:
								pad_mp.addstr(center_y + y , center_x + x , map_data[display_mode]["sym"])
								pad_mp.addstr(center_y + y , center_x + x + 1, map_data[display_mode]["sym2"])
							if y // 2 * 2 < y and inp_y // 2 * 2 == inp_y:
								pad_mp.addstr(center_y + y , center_x + x + 1 , map_data[display_mode]["sym"])
								pad_mp.addstr(center_y + y , center_x + x , map_data[display_mode]["sym2"])
						else:
							pad_mp.addstr(center_y + y , center_x + x , map_data[display_mode]["sym"])
							pad_mp.addstr(center_y + y , center_x + x + 1, map_data[display_mode]["sym2"])
				except curses.error:
					pass
				
			except TypeError:
				pass
			
	if ((inp_x > -1 ) and (inp_y > -1)) and ((inp_x < dim) and (inp_y < dim)):
		pass
	else:
		pad_mp.addch(center_y, center_x + 1, ">")
		pad_mp.addch(center_y, center_x + 2 , "<")
	
	#try:
		#map_data = decypher(inp_x, inp_y, I, name, dim)
		
		#pad_mp.addch(center_y, center_x + 1, map_data[display_mode]["sym"], curses.A_REVERSE)
		#pad_mp.addch(center_y, center_x + 2, map_data[display_mode]["sym2"], curses.A_REVERSE)
	#except TypeError:
		#pass
	
	stdscr.refresh()
	try:
		pad_mp.refresh(0,0,0,0, height - 3, width)
	except curses.error:
		pass
		


def write_new(stdscr):
	height, width = stdscr.getmaxyx()
	
	stdscr.clear()
	stdscr.addstr(0, 0, "set file name:")
	stdscr.refresh()
	sub = stdscr.subwin(1, width - 1, 1, 0)
	tb = curses.textpad.Textbox(sub)
	#name = tb.edit()
	name = "terrain"
	stdscr.refresh()
	stdscr.addstr(1, 0, name)
	
	stdscr.addstr(2, 0, "set map dimension:")
	stdscr.refresh()
	sub = stdscr.subwin(1, width - 1, 3, 0)
	tb = curses.textpad.Textbox(sub)
	dim = int(tb.edit())
	stdscr.refresh()
	stdscr.addstr(3, 0, str(dim))
	#dim = dim * 100

	param = 2
	
	#stdscr.clear()
	stdscr.addstr(4, 0, "generating ...")
	stdscr.refresh()
	#I = [[0 for x in range(dim)] for y in range(dim)]

	#for x in range (dim):
		#for y in range (dim):
			#I[x][y] = [0 for i in range(param)]
	
	length = param

	#for x in range (dim):
		#for y in range (dim):
			#I[x][y] = array.array('B', I[x][y])

	#bulk = [0 for i in range(dim * dim * length)]
	
	bdim = struct.pack('I', dim)
	blen = struct.pack('I', length)
	#bbulk = array.array('B', bulk)
	
	#with open(name, "wb") as map:
	with GzipFile("terrain.gz", "wb") as map:
		map.write(bdim)
		map.write(blen)
		#for x in range (dim):
			#for y in range (dim):
				#map.write(I[x][y])
		map.write(b'\x00' * length * dim * dim )
			
	stdscr.clear()
	
def read_map(stdscr, colors):
	height, width = stdscr.getmaxyx()
	stdscr.clear()
	#stdscr.addstr(0, 0, "select file name:")
	stdscr.refresh()
	sub = stdscr.subwin(1, width - 1, 1, 0)
	tb = curses.textpad.Textbox(sub)
	#name = tb.edit()
	name = "terrain"
	stdscr.addstr(1, 0, name)
	
	stdscr.addstr(2, 0, "reading file ...")
	stdscr.refresh()
	
	with GzipFile("terrain.gz", "rb") as map:
		#with map_gzip.open("terrain", "r") as map:
			bb = io.BytesIO(map.read())
	
	bb.seek(0)
	dim = struct.unpack('I', bb.read(4))[0]
	bb.seek(4)
	length = struct.unpack('I', bb.read(4))[0]
	
	#I = [[0 for x in range(dim)] for y in range(dim)]

	#bb.seek(8)
	#for x in range (dim):
		#for y in range (dim):
			#I[x][y] = struct.unpack('{}B'.format(length), bb.read(length))
	
	inp_x = 0
	inp_y = 0
	inp = 0
	display_mode = 0
	edit_mode = 0
	by = 0
	
	
	while True:
		#try:
			#map_data = decypher(inp_x, inp_y, bb, name, dim, length)[0]
		#except TypeError:
			#pass
		height, width = stdscr.getmaxyx()
		if inp == keymaps.scroll_up:
			inp_y = inp_y + 1
		if inp == keymaps.scroll_dn:
			inp_y = inp_y - 1
		if inp == keymaps.scroll_lt:
			inp_x = inp_x - 1
		if inp == keymaps.scroll_rt:
			inp_x = inp_x + 1
		
		#L = (inp_x) * (dim) * length + (inp_y) * length + 8
		#try:
			#bb.seek(L)
		#except ValueError:
			#bb.seek(0)
		#try:
			#u = struct.unpack('{}B'.format(length), bb.read(length))
		#except struct.error:
			#bb.seek(0)
			#u = struct.unpack('{}B'.format(length), bb.read(length))
		#e = list(u)
		
		#I = [[0 for x in range(dim)] for y in range(dim)]

		#bb.seek(8)
		#for x in range (dim):
			#for y in range (dim):
				#I[x][y] = struct.unpack('{}B'.format(length), bb.read(length))
		
		#stdscr.timeout(500)
		#print(map_data)
		#return
		display(height, width, colors, display_mode, edit_mode, stdscr, name, dim, length, inp_x, inp_y, bb)
		inp = stdscr.getch()
		
		if inp == ord("m"):
			if not display_mode == length - 1:
				display_mode = display_mode + 1
			else:
				display_mode = 0
				
		if inp == ord("e"):
			if edit_mode == 0:
				edit_mode = 1
			else:
				edit_mode = 0
				
		if inp == keymaps.escape:
			break
		
		
		try:
			by = int(chr(inp))
		except ValueError:
			pass
		
		try:
			tile = gamedata.terrain[str(display_mode)][str(by)]["sym"]
		except KeyError:
			tile = "N"
		
		#stdscr.clear()
		
		#stdscr.addstr(height - 3, width - 3, str(by))
		try:
			stdscr.addstr(height - 3, 0, "Map {0}x{0}. display_mode {1}. Tile to place: {2}".format(dim, display_mode, tile))
			for x in range(width):
				stdscr.addstr(height - 2, x, " ")
			#try:
			stdscr.addstr(height - 2, 0, "Cursor @{0},{1}.".format(inp_x, inp_y))
			#except TypeError:
				#pass
			stdscr.addstr(height - 1, 0, "'Esc' - close view. 'e' - switch to drawing mode. 'm' - change display mode.")
		except curses.error:
			pass
			
		stdscr.refresh()
		
		if edit_mode == 1:
			stdscr.timeout(-1)
			if ((inp_x > -1 ) and (inp_y > -1)) and ((inp_x < dim ) and (inp_y < dim)):
				e = decypher(inp_x, inp_y, bb, name, dim, length)[1]
				L = decypher(inp_x, inp_y, bb, name, dim, length)[2]
				i = display_mode
				if i > (len(e) - 1):
					i = len(e) - 1
				if i < 0:
					i = 0
				
				if by < 0:
					by = 0
				e[i] = by
			
				try:
					be = array.array('B',e)
				except OverflowError:
					be = array.array('B',[0])
				gb = bb.getbuffer()
				try:
					gb[L:(L+length)] = bytes(be)
				except ValueError:
					pass
				del gb
				bb.seek(0)
				b = bb.read()
				
				#with open(name, "r+b") as map:
				#map.close()
				with GzipFile("terrain.gz", "wb") as map:
					map.write(b)
			else:
				pass
				
				
	stdscr.clear()
			
	

def draw(stdscr):
	curses.curs_set(False)
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)
	
	colors = {
		'col1':curses.color_pair(1),
		'col2':curses.color_pair(2),
		}
		
	while True:
		stdscr.timeout(-1)
		stdscr.bkgd(" ", curses.A_REVERSE)
		stdscr.addstr(0,0, "'w'rite or 'r'ead and edit the map?:")
		stdscr.addstr(1,0, "'q'uit")
		inp_n = stdscr.getkey()
		
		if inp_n == "w":
			write_new(stdscr)
		if inp_n == "r":
			read_map(stdscr, colors)
		if inp_n == "q":
			break
		stdscr.refresh()
	
def loop():
	curses.wrapper(draw)
	
loop()
