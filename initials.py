import io
import struct
from gzip import GzipFile

print("Loading...")
#ZipFile = zipfile.ZipFile()
with GzipFile("terrain.gz", "rb") as map:
#with ZipFile("terrain.zip", "r") as map_zip:
	#with map_zip.open("terrain", "r") as map:
		bb = io.BytesIO(map.read())
bb.seek(0)
dim = struct.unpack('I', bb.read(4))[0]
bb.seek(4)
length = struct.unpack('I', bb.read(4))[0]

spatial = {

	'loc':
		{
		'pre':[0,0],
		'cur':[0,0],
		},
		
	'ort':
		{
		'val':(0,1),
		'str':"North",
		'var':"N",
		},
		
	'gametime':0,
}

buffer = {

	'terrain':{
		'dim':dim,
		'length':length,
		'bb':bb,
		}
}