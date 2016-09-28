from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from string import printable
import collections
import random
import sys
import time

try:
    import curses
except ImportError:
    print "pmatrix requires curses for terminal rendering; exiting."
    exit(1)

# Colors that the user may set as foreground/background.
COLORS = {
    "BLACK" : curses.COLOR_BLACK,
    "BLUE" : curses.COLOR_BLUE,
    "CYAN" : curses.COLOR_CYAN,
    "GREEN" : curses.COLOR_GREEN,
    "MAGENTA" : curses.COLOR_MAGENTA,
    "RED" : curses.COLOR_RED,
    "WHITE" : curses.COLOR_WHITE,
    "YELLOW" : curses.COLOR_YELLOW,
}

def rand_string(character_set, length):
    """Returns a random string.
        character_set -- the characters to choose from.
        length        -- the length of the string.
    """
    return "".join(random.choice(character_set) for _ in xrange(length))

def main(stdscr):

    curses.curs_set(0)
    curses.init_pair(9, FG, BG)
    stdscr.bkgd(curses.color_pair(9))
    curses.start_color()
    size = stdscr.getmaxyx()

    # background is a matrix of the actual letters (not lit up) -- the underlay.
    # foreground is a binary matrix representing the position of lit letters -- the overlay.
    # dispense is where new 'streams' of lit letters appear from.
    background = rand_string(printable.strip(), size[0] * size[1])
    foreground = []
    dispense   = []

    delta = 0
    bg_refresh_counter = random.randint(3, 7)
    lt = time.time()

    while 1:

        if CLEAR:
            stdscr.clear()
        else:
            stdscr.erase()

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
                dispense.append(random.randint(0, size[1] - 1))

            for i, c in enumerate(dispense):
                foreground.append([0, c])
                if not random.randint(0, PROBABILITY):
                    del dispense[i]

            for a, b in enumerate(foreground):
                if b[0] < size[0] - 1:
                    stdscr.addstr(b[0], b[1],
                                    background[b[0] * size[0] + b[1]],
                                    curses.color_pair(9))
                    b[0] += 1
                else:
                    # We cannot simply use `del b`. This is because using del
                    # on the local variable b will only remove its binding
                    # from the local namespace. We have to remove it directly
                    # from the list.  
                    del foreground[a]

            bg_refresh_counter -= 1
            if bg_refresh_counter <= 0:
                background = rand_string(printable.strip(), size[0] * size[1])
                bg_refresh_counter = random.randint(3, 7)

            delta -= 1
            stdscr.refresh()

def start():

    parser = ArgumentParser(description="Create the matrix falling text.",
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument("-b", "--background", default="black",
            help="The colour of the falling text.")
    parser.add_argument("-c", "--clear", action="store_true",
            help="Use stdscr.clear() instead of stdscr.erase().")
    parser.add_argument("-f", "--foreground", default="green",
            help="The colour of the falling text.")
    parser.add_argument("-l", "--letters", type=int, default=2,
            help="The number of letters produced per update.")
    parser.add_argument("-p", "--probability", type=int, default=5,
            help="1/p probability of a dispense point deactivating each tick.")
    parser.add_argument("-u", "--ups", type=int, default=15,
            help="The number of updates to perform per second.")
    args = parser.parse_args()

    global BG, CLEAR, FG, LETTERS_PER_UPDATE, PROBABILITY, UPDATES_PER_SECOND
    CLEAR = args.clear
    FG = COLORS.get(args.foreground.upper(), curses.COLOR_GREEN)
    BG = COLORS.get(args.background.upper(), curses.COLOR_BLACK)
    LETTERS_PER_UPDATE = abs(args.letters)
    PROBABILITY = args.probability - 1
    UPDATES_PER_SECOND = abs(args.ups)

    try:
        while 1:
            curses.wrapper(main)
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)

if __name__ == "__main__":
    start()
