import curses
from curses import wrapper #initialises curses module so terminal inputting and prints is different
import time
import random

def start_screen(stdscr):
    stdscr.clear() # clears screen
    stdscr.addstr("Welcome to the Speed Typing Test!")  #std = standard output (terminal) scr = screen
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh() # refreshes screen
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0): #if set parameter = 0 it's default will be 0 if nothing is passed when the funcion is called
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM:{wpm}") # f string allows us to directly use a variable into a string without having to do converstion to type string and then concatenate 2 strings. Variable in curly braces.

    for i, char in enumerate(current): # i, char = (index, element) because of enumerate
        correct_char = target[i]
        colour = curses.color_pair(1)
        if char != correct_char:
            colour = curses.color_pair(2)

        stdscr.addstr(0, i, char, colour)

def load_text():
    with open("text.txt", "r", encoding='utf-8') as f: # with as f means the file will close when we are done using it. Important to specify the encoding so that you don't get weird symbols for puncuation.
        lines = f.readlines()
        return random.choice(lines).strip() #There is a hidden /n at the end of every line in the text file so .strip() removes it


def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True) # STOPS key = stdscr.getkey() from waiting for a user keystroke

    while True:
        time_elapsed = max(time.time() - start_time, 1) # using max(,1) to stop 0 division error rounds 0 to 1
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5) # average of 5 letters in a word

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text: # "".join combines list elements into a string. The "" is the delimiter (seperator) and .join takes the list as argument.
            stdscr.nodelay(False) #restarts waiting for user to input a key
            break
        try:
            key = stdscr.getkey()
        except:
            continue # if exception is triggered the code restart the while loop and skips the code below

        if ord(key) == 27: #ord(key) takes the ASCII or UNICODE value of the character. The ASCII CODE for ESC is 27.
            break

        if key in ("KEY_BACKSPACE", '\b', "\x7f"): # There are all the ways of representing backslash on various OS'
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK) #foreground colour green background colour white connected to id = 1
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break
    '''
    stdscr.addstr("Hello World!", curses.color_pair(1)) # prints hello world using colour pair id = 1 (green)
    stdscr.addstr(1,  5, "Hello World!") #prints hello world 1 row down 5 columns across in terminal
    key = stdscr.getkey() # assigns variable to user keystrokes
    '''
wrapper(main)
