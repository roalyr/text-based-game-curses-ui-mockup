import curses
import random
import textwrap
import time

import game
import gamebuffer
import keymaps
import strings


######################################
#COMPOSE AND FORMAT
def strings_short(_state, _buffer, misc, classes, dec):
	sp = classes["sp"]
	
	loc_cur = _state["loc"]["cur"]
	loc_pre = _state["loc"]["pre"]
	elev = dec[1]["str"]
	landform = dec[0]["str"]
	map_dim = _buffer["terrain"]["dim"]
	
	comp_r = sp.compass(_state["ort"])
	comp_l = sp.compass(_state["ort"])
	compass_m = _state["ort"]["var"]
	compass_r = comp_r["r"]["var"]
	compass_l = comp_l["l"]["var"]
		
	ort_str = _state["ort"]["str"]
		
	if loc_pre == loc_cur:
		ann = " "
	else:
		ann = "You have moved {}."
		
	st = {
		'compass_m':compass_m,
		'compass_r':compass_r,
		'compass_l':compass_l,
		'ort_str':ort_str,
		'loc_cur':loc_cur,
		'loc_pre':loc_pre,
		'ann':ann,
		'elev':elev,
		'landform':landform,
		'map_dim':map_dim,
		}
		
	return st

#-------------------------------------
def textwin_form(_state, wi, st, colors, classes, misc, pad_pos, inp):
	
	height = misc["height"]
	pad_te_h_init = wi["pad_te_h_init"]
	pad_st_h = wi["pad_st_h"]
	win_co_h = wi["win_co_h"]
	pad_te_w = wi["pad_te_w"]
	win_an_h = wi["win_an_h"]
	tw = classes["tw"]
	bg_white = colors["bg_white"]
	loc_cur = st["loc_cur"]
	ort_str = st["ort_str"]
	elev = st["elev"]
	landform = st["landform"]
	
	gametime = _state["gametime"]
	
	te_prg1_w = tw.wrap(strings.te_prg1)
	te_prg2_w = tw.wrap(strings.te_prg2.format(landform, elev))
	te_prg3_w = tw.wrap(strings.te_prg3.format(ort_str, loc_cur, gametime))
	te_prg4_w = tw.wrap(strings.te_prg4)
		
	dn_zon_h = (
			+ len(te_prg1_w)
			+ len(te_prg2_w)
			+ len(te_prg3_w)
			+ len(te_prg4_w)
			) 
			
	str_rows = dn_zon_h + 8
		
	if str_rows > pad_te_h_init:
		pad_te_h = str_rows
		pad_te_scr = True
	else: 
		pad_te_h = pad_te_h_init
		pad_te_scr = False
		
	if pad_te_scr is True:
		if inp == keymaps.scroll_dn and pad_pos < (pad_te_h - pad_te_h_init):
			pad_pos = pad_pos + 1
		if inp == keymaps.scroll_up and pad_pos > 0:
			pad_pos = pad_pos - 1
	else:
		pad_pos = 0
		
	pad_te = curses.newpad(pad_te_h, pad_te_w)
	pad_te.bkgd(" ", bg_white)
	pad_te.border(curses.ACS_VLINE,curses.ACS_VLINE, ' ', ' ', curses.ACS_VLINE, curses.ACS_VLINE)
	
	
	if pad_pos <= (pad_te_h - pad_te_h_init) and pad_pos != 0:
		pad_te.addstr(pad_pos + 1, pad_te_w - 1, "^", curses.A_REVERSE)
	if pad_pos >= 0 and pad_pos != (pad_te_h - pad_te_h_init) and pad_te_scr is True:
		pad_te.addstr(pad_pos + (height - win_co_h - pad_st_h - win_an_h) - 2, pad_te_w - 1, "v", curses.A_REVERSE)

			
	tw = {
		'pad_pos':pad_pos,
		'pad_te':pad_te,
		'te_prg1_w':te_prg1_w,
		'te_prg2_w':te_prg2_w,
		'te_prg3_w':te_prg3_w,
		'te_prg4_w':te_prg4_w,
		}
	
	return tw

#-------------------------------------
def win_compose(height, width, wi, st, tw):
	
	win_co_w = wi["win_co_w"]
	win_co = wi["win_co"]
	win_an = wi["win_an"]
	pad_te = tw["pad_te"]
	pad_mp = wi["pad_mp"]

	pad_st = wi["pad_st"]
	pad_mp_w = wi["pad_mp_w"]
	pad_mp_h = wi["pad_mp_h"]
	
	compass_l = st["compass_l"]
	compass_m = st["compass_m"]
	compass_r = st["compass_r"]
	
	loc_cur = st["loc_cur"]
	ort_str = st["ort_str"]
	map_dim = st["map_dim"]
	
	ann = st["ann"]
	
	te_prg1_w = tw["te_prg1_w"]
	te_prg2_w = tw["te_prg2_w"]
	te_prg3_w = tw["te_prg3_w"]
	te_prg4_w = tw["te_prg4_w"]
	
	for x in range(1, win_co_w - 1):
		win_co.addstr(0, x, ".")
	win_co.addstr(0, 1, "[{}]".format(compass_l))
	win_co.addstr(0, win_co_w // 2 - len(compass_m) // 2 - 1, "[{}]".format(compass_m))
	win_co.addstr(0, win_co_w - (len(compass_r) + 3), "[{}]".format(compass_r))
	
	center_x = pad_mp_w // 2
	if pad_mp_h // 2 * 2 < pad_mp_h:
		center_y = pad_mp_h // 2 
	else:
		center_y = pad_mp_h // 2 - 1
		
	for i in range(0, len(te_prg1_w)):
		pad_te.addstr(0 + i, 1, 
							te_prg1_w[i].format(width, height, map_dim))
							
	for i in range(0, len(te_prg2_w)):
		pad_te.addstr(1 + len(te_prg1_w)
						+ i, 1, 
							te_prg2_w[i])
							
	for i in range(0, len(te_prg3_w)):
		pad_te.addstr(2 + len(te_prg1_w)
						+ len(te_prg2_w)
						+ i, 1, 
							te_prg3_w[i])
							
	for i in range(0, len(te_prg4_w)):
		pad_te.addstr(3 + len(te_prg1_w)
						+ len(te_prg2_w)
						+ len(te_prg3_w)
						+ i, 1, 
							te_prg4_w[i])
		
	win_an.addstr(1, 1, ann.format(ort_str))


#-------------------------------------
def window_geom(colors, classes, misc):
	bg_white = colors["bg_white"]
	height = misc["height"]
	width = misc["width"]
	tw = classes["tw"]

	win_co_h = 1
	win_co_w = width
		
	pad_mp_h = height // 2
	pad_mp_w = width // 2 + 3
		
	pad_st_h = pad_mp_h 
	pad_st_w = (width - 1) // 2 + 1
		
	win_an_h = 3
	win_an_w = width
		
	pad_te_h_init = (height - win_an_h - win_co_h - pad_st_h) + 2
	pad_te_w = width
	tw.width = pad_te_w - 2
		
	win_co = curses.newwin(win_co_h, win_co_w, 0, 0)
	pad_mp = curses.newpad(pad_mp_h, pad_mp_w)
	pad_st = curses.newpad(pad_st_h, pad_st_w)
	win_an = curses.newwin(win_an_h, win_an_w, height - win_an_h, 0)
		
	win_co.bkgd(" ", bg_white)
			
	pad_mp.bkgd(" ", bg_white)
	
	pad_mp.addch(0, 0, curses.ACS_ULCORNER)
			
	pad_st.bkgd(" ", bg_white)

	win_an.bkgd(" ", bg_white)
	win_an.box()
	win_an.addch(0, 0, curses.ACS_LTEE)
	win_an.addch(0, win_an_w - 1, curses.ACS_RTEE)
	
	wi = {
		'win_co_h':win_co_h,
		'win_co_w':win_co_w,
		'pad_st_h':pad_st_h,
		'pad_st_w':pad_st_w,
		'win_an_h':win_an_h,
		'win_an_w':win_an_w,
		'pad_te_h_init':pad_te_h_init,
		'pad_te_w':pad_te_w,
		'win_co':win_co,
		'pad_st':pad_st,
		'win_an':win_an,
		'pad_mp':pad_mp,
		'pad_mp_h':pad_mp_h,
		'pad_mp_w':pad_mp_w,
		}
		
	return wi


#-------------------------------------
def refresh_all(stdscr, wi, tw, misc):
	
	height = misc["height"]
	width = misc["width"]
	
	win_co = wi["win_co"]
	win_co_h = wi["win_co_h"]
	
	pad_te = tw["pad_te"]
	pad_te_w = wi["pad_te_w"]
	pad_pos = tw["pad_pos"]
	
	pad_mp = wi["pad_mp"]
	pad_mp_h = wi["pad_mp_h"]
	pad_mp_w = wi["pad_mp_w"]
	
	pad_st = wi["pad_st"]
	pad_st_h = wi["pad_st_h"]
	pad_st_w = wi["pad_st_w"]
				
	win_an = wi["win_an"]
	win_an_h = wi["win_an_h"]
	
	stdscr.refresh()
	win_co.refresh()
	try:
		pad_te.refresh(pad_pos, 0, (win_co_h + pad_st_h), 0, (height - win_an_h - 1), pad_te_w)
		
		pad_mp.border(curses.ACS_VLINE, curses.ACS_VLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_ULCORNER, curses.ACS_URCORNER, curses.ACS_LTEE)
		pad_mp.refresh(0, 0, (win_co_h), 0, (win_co_h + pad_mp_h), pad_mp_w )
			
		pad_st.border(curses.ACS_VLINE, curses.ACS_VLINE, curses.ACS_HLINE, curses.ACS_HLINE, curses.ACS_TTEE, curses.ACS_URCORNER, curses.ACS_BTEE, curses.ACS_RTEE)
		pad_st.refresh(0, 0, (win_co_h), (width // 2), (win_co_h + pad_st_h - 1), width - 1)
	
	except curses.error:
		pass
	win_an.refresh()











######################################
#UI ELEMENTS
def ui_map(wi, _state, _buffer, colors, misc):
	pad_mp = wi["pad_mp"]
	pad_mp_h = wi["pad_mp_h"]
	pad_mp_w = wi["pad_mp_w"]
	map_dim = _buffer["terrain"]["dim"]
	stdscr = misc["stdscr"]
	ort = _state["ort"]["val"]
	center_x = pad_mp_w // 2 - 1
	center_y = pad_mp_h // 2 
	
	inp_x = _state["loc"]["cur"][0]
	inp_y = _state["loc"]["cur"][1]
	
	_map_state = {'loc':{'cur':[1, 1]}}
	
	for x in range(-center_x , +center_x, 2):
		for y in range(-center_y , +center_y):
			
			i = (inp_x * 2 + x) // 2
			j = inp_y - y
			
			if ((x == 0 or x == 1) and y == 0) or ((x == 0 + 2 * ort[0]  or x == 1 + 2 * ort[0] ) and y == 0 - ort[1]):
				pad_mp.attron(curses.A_REVERSE)
			else:
				pad_mp.attroff(curses.A_REVERSE)
			if (x == 0 + 2 * ort[0]  or x == 1 + 2 * ort[0] ) and y == 0 - ort[1]:
				pad_mp.attron(curses.A_BOLD)
			else:
				pad_mp.attroff(curses.A_BOLD)
				
			try:
				map_data = gamebuffer.decypher(_buffer, i, j)
				try:
					if (map_data[0]["anim"] == 1):
						if round(random.uniform(0,100)) >= map_data[0]["anim_rat"]:
							pad_mp.addch(center_y + y , center_x + x , map_data[0]["sym"])
							pad_mp.addch(center_y + y , center_x + x + 1 , map_data[0]["sym2"])
								
						else:
							pad_mp.addch(center_y + y , center_x + x , map_data[0]["sym_anim"], curses.A_BOLD)
							pad_mp.addch(center_y + y , center_x + x + 1 , map_data[0]["sym_anim"], curses.A_BOLD)
								
					else:
						if map_data[0]["shift"] == 1:
							if y // 2 * 2 < y and inp_y // 2 * 2 < inp_y:
								pad_mp.addstr(center_y + y , center_x + x , map_data[0]["sym"])
								pad_mp.addstr(center_y + y , center_x + x + 1 , map_data[0]["sym2"])
							if y // 2 * 2 == y and inp_y // 2 * 2 < inp_y:
								pad_mp.addstr(center_y + y , center_x + x + 1 , map_data[0]["sym"])
								pad_mp.addstr(center_y + y , center_x + x , map_data[0]["sym2"])
							if y // 2 * 2 == y and inp_y // 2 * 2 == inp_y:
								pad_mp.addstr(center_y + y , center_x + x , map_data[0]["sym"])
								pad_mp.addstr(center_y + y , center_x + x + 1, map_data[0]["sym2"])
							if y // 2 * 2 < y and inp_y // 2 * 2 == inp_y:
								pad_mp.addstr(center_y + y , center_x + x + 1 , map_data[0]["sym"])
								pad_mp.addstr(center_y + y , center_x + x , map_data[0]["sym2"])
						else:
							pad_mp.addstr(center_y + y , center_x + x , map_data[0]["sym"])
							pad_mp.addstr(center_y + y , center_x + x + 1, map_data[0]["sym2"])
				except curses.error:
					pass
				
			except TypeError:
				pass
				
			#_map_state["loc"]["cur"][0] = inp_x
			#_map_state["loc"]["cur"][1] = inp_y
			#map_data = gamebuffer.decypher(_map_state, _buffer, "terrain", map_dim)
			#pad_mp.addch(center_y, center_x + 0 , map_data[0]["sym"], curses.A_REVERSE)
			#pad_mp.addch(center_y, center_x + 1, map_data[0]["sym2"], curses.A_REVERSE)
			
			#_map_state["loc"]["cur"][0] = inp_x + _state["ort"]["val"][0]
			#_map_state["loc"]["cur"][1] = inp_y + _state["ort"]["val"][1]
			#map_data = gamebuffer.decypher(_map_state, _buffer, "terrain", map_dim)
			#if map_data is not None:
				#pad_mp.addch(center_y - _state["ort"]["val"][1], center_x + _state["ort"]["val"][0] * 2 + 0,
					#map_data[0]["sym"], curses.A_REVERSE | curses.A_BOLD)
				#pad_mp.addch(center_y - _state["ort"]["val"][1], center_x + _state["ort"]["val"][0] * 2 + 1,
					#map_data[0]["sym2"], curses.A_REVERSE | curses.A_BOLD)
			#else:
				#pass

#-------------------------------------
def ui_newwin(misc, colors):
	height = misc["height"]
	width = misc["width"]
	bg_white = colors["bg_white"]
	
	inp_n = 0
	while True:
		win_n = curses.newwin(height, width, 0, 0)
		win_n.bkgd(".", bg_white)
		win_n.addstr(0, 0, "Press 'Esc' to return")
		inp_n = win_n.getch()
		win_n.refresh()
		if inp_n == 27:
			break

#-------------------------------------
def ui_greetscr(stdscr, misc):
	height = misc["height"]
	width = misc["width"]
	stdscr.addstr(height // 2, 0, strings.grts)
	stdscr.getkey()
	stdscr.refresh()
	stdscr.clear() 
	curses.endwin()

#-------------------------------------
def ui_pholder(stdscr, misc):
	height = misc["height"]
	width = misc["width"]
	stdscr.bkgd(" ")
	stdscr.refresh()
	try:
		stdscr.getkey()
	except curses.error:
		pass
	stdscr.clear()
	curses.endwin()


#######################################
#MAIN FUNCTION

def draw(stdscr, _state, _buffer):
	
	anim_time = 500
	height, width = stdscr.getmaxyx()
	inp = 0
	#map_dim = [0]
	#map_str = _buffer["map_str"]
	#mapr = gamebuffer.MapRead()
	max_h = 13
	max_w = 25
	pad_pos = 0
	
	curses.curs_set(False)
	curses.start_color()
	curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_WHITE)
	curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_WHITE)
	curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)

	colors = {
		'bg_white':curses.color_pair(1),
		'mp_green':curses.color_pair(2),
		'mp_yellow':curses.color_pair(3),
		'mp_blue':curses.color_pair(4),
		'mp_white':curses.color_pair(5),
			}

	
	
	#for i in range(len(map_str)):
		#s = str(map_str[i]) + "map"
		#_buffer["maps"][map_str[i]], map_dim[i] = mapr.read(map_str[i])
		#stdscr.addstr(i,0,s)
		
	stdscr.refresh()
	
	classes = {
		'sp':game.Spatial(),
		'tw':textwrap.TextWrapper(),
		}
	
	misc = {
		#'map_dim':map_dim,
		'stdscr':stdscr,
		'height':height,
		'width':width,
		}

	if width < max_w or height < max_h:
		ui_pholder(stdscr, misc)
		stdscr.clear()
	else:
		ui_greetscr(stdscr, misc)
		stdscr.clear()
		while True:
			
			
			stdscr.timeout(anim_time)
			height, width = stdscr.getmaxyx()
			misc["height"] = height
			misc["width"] = width
			
			if width < max_w or height < max_h:
				ui_pholder(stdscr, misc)
			else:
					
				try:
					pad_pos = tw["pad_pos"]
				except UnboundLocalError:
					pass
				
				dec = gamebuffer.decypher(_buffer, _state["loc"]["cur"][0], _state["loc"]["cur"][1])
				wi = window_geom(colors, classes, misc)
				st = strings_short(_state, _buffer, misc, classes, dec)
				tw = textwin_form(_state, wi, st, colors, classes, misc, pad_pos, inp)
				win_compose(height, width, wi, st, tw)
				
				ui_map(wi, _state, _buffer, colors, misc)
				refresh_all(stdscr, wi, tw, misc)
				
				inp = stdscr.getch()
				
				if inp != -1:
					_state=game.loop(inp, _state, _buffer)
		
				#UI menus.
				if inp == keymaps.new_win:
					ui_newwin(height, width, colors)
		
				if inp == keymaps.escape:
					break
		
		
def loop(_state, _buffer):
	curses.wrapper(draw, _state, _buffer)