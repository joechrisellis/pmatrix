from string import printable
import curses
import optparse
import random
import time

COLORS = {
	"BLUE" : curses.COLOR_BLUE,
	"CYAN" : curses.COLOR_CYAN,
	"GREEN" : curses.COLOR_GREEN,
	"MAGENTA" : curses.COLOR_MAGENTA,
	"RED" : curses.COLOR_RED,
	"WHITE" : curses.COLOR_WHITE,
	"YELLOW" : curses.COLOR_YELLOW,
}

rand_string = lambda c, l: "".join(random.choice(c) for i in xrange(l))

def main(stdscr):
	curses.curs_set(0)
	curses.init_pair(9, COLOR, curses.COLOR_BLACK)
	curses.start_color()
	size = stdscr.getmaxyx()

	back = rand_string(printable.strip(), size[0] * size[1])
	dispense, visible = [], []

	lt = time.time()
	delta = 0
	while 1:
		now = time.time()
		delta += (now - lt) * UPDATES_PER_SECOND
		lt = now

		while delta >= 1:

			if stdscr.getmaxyx() != size:
				return # returns back to start()

			for i in xrange(LETTERS_PER_UPDATE):
				dispense.append(random.randint(0, size[1] - 1))

			for i, c in enumerate(dispense):
				visible.append([0, c])
				if not random.randint(0, 5):
					del dispense[i]

			for a, b in enumerate(visible):
				if b[0] < size[0] - 1:
					stdscr.addstr(b[0], b[1], back[b[0] * size[0] + b[1]], curses.color_pair(9))
					b[0] += 1
				else:
					# can't use del obj since it's not a reference to the
					# list, but instead a copy. we have to delete by index.
					del visible[a]

			delta -= 1
			stdscr.refresh()

		if ERASE:
			stdscr.erase()
		else:
			stdscr.clear()

def start():
	parser = optparse.OptionParser()
	parser.add_option("-c", "--color", default="green",
			help="The colour of the falling text.")
	parser.add_option("-e", "--erase", action="store_true",
			help="Use stdscr.erase(), which may reduce flicker.")
	parser.add_option("-l", "--letters", type=int, default=2,
			help="The number of letters produced per update.")
	parser.add_option("-u", "--ups", type=int, default=30,
			help="The number of updates to perform per second.")
	options, args = parser.parse_args()

	global COLOR, ERASE, LETTERS_PER_UPDATE, UPDATES_PER_SECOND
	COLOR = COLORS.get(options.color.upper(), curses.COLOR_GREEN)
	ERASE = options.erase
	LETTERS_PER_UPDATE = abs(options.letters)
	UPDATES_PER_SECOND = abs(options.ups)

	try:
		while 1: curses.wrapper(main)
	except KeyboardInterrupt:
		exit(0)

if __name__ == "__main__":
	start()
