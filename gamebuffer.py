import io
import struct
import array

import gamedata

def decypher(_buffer, inp_x, inp_y):
	dim = _buffer["terrain"]["dim"]
	length = _buffer["terrain"]["length"]
	bb = _buffer["terrain"]["bb"]
	
	
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
	
	decyph_dict = getattr(gamedata, "terrain")
	data_array = [0 for x in range(len(byte_array))]
	
	for i in range(len(byte_array)):
		try:
			data_array[i] = decyph_dict[str(i)][str(byte_array[i])]
		except KeyError:
			pass
	return data_array


