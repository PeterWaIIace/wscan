from curses import wrapper
import curses
import observer

class MyWin(observer.Observer):

    def __init__(self,stdscr,h,w,bh,bg):
        self.win = curses.newwin(h,w,bh,bg)
        self.win.scrollok(1)
        self.linesToPrint = []

        super().__init__()

    def loop(self):
        self._lock == True
        for i in range(len(self.linesToPrint)):
            self.win.addstr("{}\n".format(self.linesToPrint[i]),)
        self._lock == False

    def refresh(self):
        self.win.refresh() 

    def update(self,args):
        if self._lock == False:
            # print("updated")
            self.linesToPrint = args


class App():

    def __init__(self):
        self.arrows = {261:"rightarrow",260:"leftarrow",258:"downarrow",259:"uparrow"}

    def wapper_thread(self,interface):
        wrapper(self.main)

    def main(self,stdscr):
    # Clear screen
        self.DetectedNetworksWin=MyWin(stdscr, 50, 400,0,0)
        while True:
            # stdscr.clear()
            ## curses.LINES - 1, curses.COLS - 1,0, int(curses.COLS/2)) 
            self.DetectedNetworksWin.loop()
            # self.userInput(stdscr)
            self.DetectedNetworksWin.refresh()
            # stdscr.refresh()

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
