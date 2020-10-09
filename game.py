import directions
import keymaps

#------------------------ Game classes ----------------------
class Spatial:
	
	#Dict in order to get indices.
	ort_n = {'N':'1','NE':'2','E':'3','SE':'4','S':'5','SW':'6','W':'7','NW':'8'}
	#Reverse dict in order to get name.
	ort_i = {'1':'N','2':'NE','3':'E','4':'SE','5':'S','6':'SW','7':'W','8':'NW'}
	
	def xyz(self, inp, loc, ort, map_dim):
		if inp == keymaps.go_fwd:
			if ((loc[0] + ort["val"][0] > -1 ) and (loc[1] + ort["val"][1] > -1)) and \
				((loc[0] + ort["val"][0] < map_dim) and (loc[1] + ort["val"][1] < map_dim)):
				loc = [x + y for x, y in zip(loc, ort["val"])]
			else:
				pass
			return loc

	def translation(self, inp, loc, ort, map_dim):
		loc_pre = loc["cur"]
		loc_cur = loc["cur"]
		loc_cur = self.xyz(inp, loc_cur, ort, map_dim)
		if loc_cur is None:
			loc = {'pre':loc_pre,'cur':loc_pre}
			return loc
		else:
			loc = {'pre':loc_pre,'cur':loc_cur}
			return loc
	
	def compass(self,ort):
		var = ort["var"]
		i = int(self.ort_n[var])
		if i == 8:
			var_l = self.ort_i[str(i - 1)]
			var_r = self.ort_i[str(1)]
		elif i == 1:
			var_l = self.ort_i[str(8)]
			var_r = self.ort_i[str(i + 1)]
		else:
			var_l = self.ort_i[str(i - 1)]
			var_r = self.ort_i[str(i + 1)]
			
		comp_l = getattr(directions, var_l)
		comp_r = getattr(directions, var_r)
		comp={'l':comp_l,'r':comp_r}
		return comp
	
	def orientation(self,inp,ort):
		#Get variable name.
		var = ort["var"]
		#Index of current orientation.
		i = int(self.ort_n[var])
		if inp == keymaps.turn_right and i < 8:
			i = i + 1
		elif inp == keymaps.turn_right and i >= 8:
			i = 1
		elif inp == keymaps.turn_left and i <= 8 and i != 1:
			i = i - 1
		elif inp == keymaps.turn_left and i == 1:
			i = 8
		
		new_var = self.ort_i[str(i)]
		ort = getattr(directions,new_var)
		return ort

class World:
	
	def counttime(self, gametime):
		gametime = gametime + 1
		#print("current time instance -",time)
		return gametime

#------------------------ Class instances --------------------
player = Spatial()
world = World()
	
#------------------------ Game loop --------------------------
def loop(inp, _state, _buffer):
	_state["ort"] = player.orientation(inp,_state["ort"])
	_state["loc"] = player.translation(inp,_state["loc"], _state["ort"], _buffer["terrain"]["dim"])
	_state["gametime"] = world.counttime(_state["gametime"])
	return _state