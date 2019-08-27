from curses import wrapper
import curses
import observer

class MyWin(observer.Observer):

    def __init__(self,stdscr,h,w,bh,bg):
        self.win = curses.newwin(h,w,bh,bg)
        self.linesToPrint = ["starting","lol"]

    def loop(self):
        for i in range(len(self.linesToPrint)):
            self.win.addstr('something to print lol: {}\n'.format(self.linesToPrint[i]))
        

    def refresh(self):
        self.win.refresh() 

    def update(self,args):
        self.linesToPrint = args


class App():

    def __init__(self):
        self.arrows = {261:"rightarrow",260:"leftarrow",258:"downarrow",259:"uparrow"}
        wrapper(self.main)

    def main(self,stdscr):
    # Clear screen
        while True:
            stdscr.clear()
            height = 0; width = 0

            self.DetectedNetworksWin=MyWin(stdscr, height,width,0,0)## curses.LINES - 1, curses.COLS - 1,0, int(curses.COLS/2))
            self.DetectedNetworksWin.loop()

            # self.userInput(stdscr)
            self.DetectedNetworksWin.refresh()

    def userInput(self,stdscr):
        while True:
            c = stdscr.getch()
            if c in self.arrows.keys():
                print(self.arrows[c])
            elif c == ord('q'):
                return 0  # Exit the while loop
            else:
                pass
        # elif c == curses.KEY_HOME:
        #     x = y = 0
