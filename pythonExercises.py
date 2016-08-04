def do_twice(f):
	f()
	f()

def print_twice(strn):
	print(strn)
	print(strn)

def do_four(f):
	do_twice(f)
	do_twice(f)

def print_top():
	print('+ - - - -', end=" ")

def print_side():
	print('|        ', end=" ")

def print_cap():
	print('+')

def print_sides():
	do_twice(print_side)
	print_side()
	print('')

def print_grid():
	do_twice(print_top)
	print_cap()
	do_four(print_sides)

def print_2x2():
	do_twice(print_grid)
	do_twice(print_top)
	print_cap()

print_2x2()
