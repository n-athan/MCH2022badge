def hex2RGB(color):
	color = hex(color)
	color = color.lstrip('0').lstrip('x')
	return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

