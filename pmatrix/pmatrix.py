from string import printable
import collections
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

rand_string = lambda c, l: "".join(random.choice(c) for _ in xrange(l))

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(9, COLOR, curses.COLOR_BLACK)
    curses.start_color()
    size = stdscr.getmaxyx()

    PMatrix = collections.namedtuple("PMatrix",
                                ["foreground", "background", "dispense"])
    matr = PMatrix([], rand_string(printable.strip(), size[0] * size[1]), [])
    delta = 0
    lt = time.time()

    while 1:

        if ERASE:
            stdscr.erase()
        else:
            stdscr.clear()

        now = time.time()
        delta += (now - lt) * UPDATES_PER_SECOND
        lt = now

        while delta >= 1:

            if stdscr.getmaxyx() != size:
                # In the event that the size of the screen has changed,
                # return from this function, effectively restarting
                # pmatrix.  
                return

            for _ in xrange(LETTERS_PER_UPDATE):
                matr.dispense.append(random.randint(0, size[1] - 1))

            for i, c in enumerate(matr.dispense):
                matr.foreground.append([0, c])
                if not random.randint(0, PROBABILITY):
                    del matr.dispense[i]

            for a, b in enumerate(matr.foreground):
                if b[0] < size[0] - 1:
                    stdscr.addstr(b[0], b[1],
                                    matr.background[b[0] * size[0] + b[1]],
                                    curses.color_pair(9))
                    b[0] += 1
                else:
                    # We cannot simply use `del b`. This is because using del
                    # on the local variable b will only remove its binding
                    # from the local namespace. We have to remove it directly
                    # from the list.  
                    del matr.foreground[a]

            delta -= 1
            stdscr.refresh()

def start():
    parser = optparse.OptionParser()
    parser.add_option("-c", "--color", default="green",
            help="The colour of the falling text.")
    parser.add_option("-e", "--erase", action="store_true",
            help="Use stdscr.erase(), which may reduce flicker.")
    parser.add_option("-l", "--letters", type=int, default=2,
            help="The number of letters produced per update.")
    parser.add_option("-p", "--probability", type=int, default=5,
            help="1/p probability of a dispense point deactivating.")
    parser.add_option("-u", "--ups", type=int, default=15,
            help="The number of updates to perform per second.")
    options, args = parser.parse_args()

    global COLOR, ERASE, LETTERS_PER_UPDATE, PROBABILITY, UPDATES_PER_SECOND
    COLOR = COLORS.get(options.color.upper(), curses.COLOR_GREEN)
    ERASE = options.erase
    LETTERS_PER_UPDATE = abs(options.letters)
    PROBABILITY = options.probability - 1
    UPDATES_PER_SECOND = abs(options.ups)

    try:
        while 1:
            curses.wrapper(main)
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    start()
