import curses
import optparse
import random
from string import printable
from time import sleep

COLOR = curses.COLOR_GREEN
COLORS = {
	"BLUE" : curses.COLOR_BLUE,
	"CYAN" : curses.COLOR_CYAN,
	"GREEN" : curses.COLOR_GREEN,
	"MAGENTA" : curses.COLOR_MAGENTA,
	"RED" : curses.COLOR_RED,
	"WHITE" : curses.COLOR_WHITE,
	"YELLOW" : curses.COLOR_YELLOW,
}

LETTERS_PER_UPDATE = 2
UPDATE_DELAY = 0.03
rand_string = lambda c, l: "".join(random.choice(c) for i in xrange(l))

def main(stdscr):
	curses.curs_set(0)
	curses.init_pair(9, COLOR, curses.COLOR_BLACK)
	curses.start_color()
	initial_size = stdscr.getmaxyx()

	back = [rand_string(printable.strip(), initial_size[1]) for i in xrange(initial_size[0])]
	dispense, visible = [], []
	
	while 1:
		size = stdscr.getmaxyx()
		if size != initial_size:
			return # returns back to start()

		stdscr.clear()

		for i in xrange(LETTERS_PER_UPDATE):
			dispense.append(random.randint(0, size[1] - 1))

		for i, c in enumerate(dispense):
			visible.append([0, c])
			if not random.randint(0, 5):
				del dispense[i]

		for i, c in enumerate(visible):
			if c[0] < size[0] - 1:
				stdscr.addstr(c[0], c[1], back[c[0]][c[1]], curses.color_pair(9))
				c[0] += 1
			else:
				# can't use del obj since it's not a reference to the
				# list, but instead a copy. we have to delete by index.
				del visible[i]

		stdscr.refresh()
		sleep(UPDATE_DELAY)

def start():
	parser = optparse.OptionParser()
	parser.add_option("-c", "--color", default="green",
			help="The colour of the falling text.")
	parser.add_option("-d", "--delay", type=float, default=0.03,
			help="The update delay.")
	parser.add_option("-l", "--letters", type=int, default=2,
			help="The number of letters produced per update.")
	options, args = parser.parse_args()

	global COLOR, LETTERS_PER_UPDATE, UPDATE_DELAY
	COLOR = COLORS.get(options.color.upper(), curses.COLOR_GREEN)
	LETTERS_PER_UPDATE = abs(options.letters)
	UPDATE_DELAY = abs(options.delay)

	try:
		while 1: curses.wrapper(main)
	except KeyboardInterrupt:
		exit(0)

if __name__ == "__main__":
	start()
