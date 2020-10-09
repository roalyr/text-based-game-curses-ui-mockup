import gameui
import initials

class States:
	def game(self, init_module):
		_state = init_module.spatial
		return _state
	def buffer(self, init_module):
		_buffer = init_module.buffer
		return _buffer
		
#Getting initial state.
#_state acts like a memory buffer
init_state = States()
_state = init_state.game(initials)
_buffer = init_state.buffer(initials)

#Starting UI and game loop in it.
gameui.loop(_state, _buffer)
	

	


