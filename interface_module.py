import curses

def deinit() :
    __screen.clear()
    curses.endwin()

def get_key_pressed() :
    key = __screen.getch()
    __screen.addstr(5,5, 'keycode:' + str(key) + ' - key:' + chr(key))
##    __screen.addch(10,0,key) #debug pressed key code
    __screen.refresh()
    return __key_map[key] if key in __key_map else key

def set_line(line_id, tag, content) :
    __screen.addstr(line_id,1, '[' + str(tag) + '] - ' + str(content))
    __screen.refresh()

def __init_screen() :
    screen = curses.initscr()
    curses.cbreak()
    screen.keypad(1) #set 1 to let curses accept escape keys

    # (y-position, x-position, string)
    screen.addstr(0, 10, "hit 'q' to quit")
    screen.addstr(1, 5, "press arrow keys to controll")

    # update display to show whatever drawn
    screen.refresh()

    return screen

## initialize #####
__screen = None
__key_map = {
    curses.KEY_UP : 'up',
    curses.KEY_DOWN : 'down',
    curses.KEY_LEFT : 'left',
    curses.KEY_RIGHT : 'right',
    32 : 'space',
    49 : '1',
    50 : '2',
    ord('q') : 'q'
}

__screen = __init_screen()
curses.noecho()
