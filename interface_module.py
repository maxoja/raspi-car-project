import curses

def deinit() :
    __screen.clear()
    curses.endwin()

def get_key_pressed() :
    key = __screen.getch()
##    __screen.addstr(6,1, 'keycode:' + str(key) + ' - key:' + chr(key))
    __screen.refresh()
    return __key_map[key] if key in __key_map else key

def set_line(line_id, tag, content) :
    __queue.append((line_id,tag,content))

#called in sonar thread
def update_screen() :
    while len(__queue) > 0 :
        line_id,tag,content = __queue[0]
        del __queue[0]
        
        if tag == '' :
            __screen.addnstr(line_id,0,str(content) + ' '*20, get_width())
        else :
            __screen.addnstr(line_id,1, '[' + str(tag) + '] - ' + str(content)  + ' '*20, get_width()-1)
            
        __screen.refresh()
        
    
def get_size() :
    return __screen.getmaxyx()

def get_width() :
    return get_size()[1]

def get_height() :
    return get_size()[0]

def set_info(name, value) :
    __info_dict[name] = value

    temp = dict(__info_dict)

    for i,k in enumerate(temp) :
        v = temp[k]
        set_line(i+8, k, v)

def __init_screen() :
    global __screen
    __screen = curses.initscr()
    curses.cbreak()
    __screen.keypad(1) #set 1 to let curses accept escape keys

    # (y-position, x-position, string)
    __screen.addnstr(1, 0, " to quit         : press 'q'", get_width())
    __screen.addnstr(2, 0, " to toggle swing : press 's'", get_width())
    __screen.addnstr(3, 0, " to toggle auto  : press 'a'", get_width())
    __screen.addnstr(4, 0, " to control      : use arrow keys and spacebar", get_width())
    __screen.addnstr(5, 0, " to adjust speed : press '1'/'2' to decrease/increase duty cycle limit", get_width())

    __screen.addnstr(7, 0, " [ - INFO - ]", get_width())

    # update display to show whatever drawn
    __screen.refresh()

## initialize #####
__key_map = {
    curses.KEY_UP : 'up',
    curses.KEY_DOWN : 'down',
    curses.KEY_LEFT : 'left',
    curses.KEY_RIGHT : 'right',
    32 : 'space',
    49 : '1',
    50 : '2',
    ord('q') : 'q',
    ord('s') : 's',
    ord('a') : 'a'
}

__screen = None
__init_screen()
curses.noecho()

__info_dict = {}

__queue = []
