import curses, curses.textpad, time, collections, scroll, re

class Screen:
	def __init__(self, resize=0):
		self.isInScroll=0
		self.dualChar=0
		self.resize=resize
		self.mainWindow=curses.initscr()
		self.ySize, self.xSize = self.mainWindow.getmaxyx()
		self.titleWindow = curses.newwin(1, self.xSize, 0, 0)
		self.conversWindow = curses.newwin((self.ySize - 2), self.xSize, 1, 0)
                self.inputWindow = curses.newwin(1, (self.xSize - 1), (self.ySize - 1), 1)
		self.inputBox = curses.textpad.Textbox(self.inputWindow)
		self.inputBox.stripspaces=1
		self.conversWindow.scrollok(True)
		self.mainWindow.addch((self.ySize - 1),0,">")
		curses.noecho()
		self.mainWindow.refresh()
		if resize == 0:
			self.channel=""
			self.peersCount=""
			self.timestamp=True
			self.doHistory=True
			self.historyLen=50
			self.history=collections.deque(maxlen=self.historyLen)

	def printMessage(self, message):
		if self.timestamp == True:
			message=time.strftime("[%H:%M] ")+message
		if self.doHistory == True:
			self.history.append(message)
		if self.isInScroll == 0:
	                self.conversWindow.addstr(message+"\n")
        	        self.conversWindow.refresh()

	def getInput(self):
		while 1:
			inputMessage = self.inputBox.edit(self.validator)
			if self.resize == 1:
				self.resize=0
				continue
			if inputMessage != "":
				self.inputWindow.clear()
				self.inputWindow.refresh()
				return inputMessage[:-1]

        def strictInput(self):
                while 1:
                        input = self.getInput()
                        if re.match("^[A-Za-z]*$", input) and len(input) <= 12:
                                return input
                        self.printMessage("Bad input.")

        def validator(self, ch):
                if self.dualChar == 1:
                        self.dualChar=0
                        if ch == 169 or ch == 168 or ch == 170:
                                ch=101
                        if ch == 160:
                                ch=97
                        if ch == 185:
                                ch=117
                        if ch == 167:
                                ch=99
                if ch == 195:
                        self.dualChar=1
                return ch
	
	def stopScreen(self):
		curses.endwin()
	
        def setTitle(self, channel, people):
		self.channel=channel
		self.peersCount=people
                self.titleWindow.clear()
                self.titleWindow.addstr("Channel : "+channel+" / People : "+str(people))
                self.titleWindow.refresh()

	def clearConvers(self):
		self.conversWindow.clear()
		self.conversWindow.refresh()

	def clearInput(self, signum=None, frame=None):
		self.inputWindow.clear()
		self.inputWindow.refresh()

	def handlerResize(self, signum="", frame=""):
		if self.isInScroll==1:
			curses.ungetch("q")
		curses.endwin()
		self.__init__(1)
		curses.ungetch(curses.ascii.NL)
		oldH = self.doHistory
		oldT = self.timestamp
		self.mainWindow.clear()
		self.doHistory = False
		self.timestamp = False
		for histLine in self.history:
			self.printMessage(histLine)
		self.doHistory = oldH
		self.timestamp = oldT
		self.setTitle(self.channel,self.peersCount)
		curses.curs_set(1)

	def scrollPrinter(self, toPrint):
		self.isInScroll=1
		hist = scroll.Scroll(self.mainWindow, toPrint)
		self.isInScroll=0
		self.handlerResize()
