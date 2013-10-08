#!/usr/bin/python
import minion, screen, re, signal, help, time

class Sschat:
	def __init__(self):
		self.screen=screen.Screen()
                signal.signal(signal.SIGINT, self.screen.clearInput)
                signal.signal(signal.SIGHUP, self.cleanQuit)
	        signal.signal(signal.SIGWINCH, self.screen.handlerResize)
		self.screen.printMessage("Hi, which channel would you like to connect to ?")
		self.channel = self.screen.getInput()
		while not re.match("^[A-Za-z]*$", self.channel):
			self.screen.printMessage("Bad channel name.")
			self.channel = self.screen.getInput()
		self.screen.printMessage("What's your nickname ?")
		self.nickname = self.screen.getInput()
		while not re.match("^[A-Za-z]*$", self.nickname):
			self.screen.printMessage("Bad nickname.")
			self.nickname = self.screen.getInput()
		self.minion=minion.Minion(self.channel, self.screen, self.nickname)
		self.screen.clearConvers()
                self.screen.setTitle(self.channel, len(self.minion.mySocket.peers))
		self.motd()

	def main(self):
		while 1:
			chatMessage= self.screen.getInput()
			if chatMessage[0] != "/":
				chatMessage = self.nickname+"("+self.minion.pid+") : "+chatMessage
				self.minion.sendMessage("/msg "+chatMessage)
				self.screen.printMessage(chatMessage)
			else:
				self.command(chatMessage[1:])

        def cleanQuit(self, signum="", frame="", reason=""):
		try:
			self.minion
		except AttributeError:
	                self.screen.stopScreen()
        	        print "Bye !"
                	quit()
		else:
			if reason == "":
				reason = "None"
               		message= "/rem "+self.minion.pid+"|"+self.nickname+"|"+reason
	                self.minion.sendMessage(message)
        	        self.screen.stopScreen()
                	print "Bye !"
               		quit()

        def motd(self):
                f = open('motd', 'r')
                lines = f.readlines()
                f.close()
		for line in lines :
			self.screen.printMessage(line[:-1])

        def bug(self, mess):
                line = time.strftime("[%H:%M] ")+self.nickname+" : "+mess+"\n"
		try :
	                f = open('bugReport', 'a')
			f.write(line)
                	f.close()
			self.screen.printMessage("Bug sent.")			
		except:
			self.screen.printMessage("Bug not sent.")


	def command(self, mess):
		cmd = mess.split(" ")[0]
		args = mess.split(" ")[1:]
		if cmd == "clear":
			self.screen.clearConvers()
		elif cmd == "help":
			self.screen.scrollPrinter(help.help)
		elif cmd == "quit":
			reason=' '.join(args)
			self.cleanQuit(0, 0, reason)
		elif cmd == "timestamp":
			if mess.split(" ")[1] == "on":
				self.screen.timestamp=True
			if mess.split(" ")[1] == "off":
				self.screen.timestamp=False
		elif cmd == "nickname":
			nick = args[0]
			if re.match("^[A-Za-z]*$", nick):
				chatMessage = self.nickname+"("+self.minion.pid+") is now known as "+nick
				self.minion.sendMessage("/msg "+chatMessage)
				self.screen.printMessage(chatMessage)
				self.nickname=nick
			else:
				self.screen.printMessage("Bad nickname.")
		elif cmd == "bug":
			mess=' '.join(args)
			self.bug(mess)
		elif cmd == "pm":
			if len(args) >= 2:
				pid=args[0]
				message=' '.join(args[1:])
				outMessage="/msg PM from "+self.nickname+"("+self.minion.pid+") : "+message
		        	self.minion.sendMessageTo(outMessage, pid)		
				self.screen.printMessage("PM to "+pid+" : "+message)
		elif cmd == "history": #int=longueur
			if len(args) == 0:
				if self.screen.doHistory == 1:
					self.screen.scrollPrinter(self.screen.history)
			elif args[0] == "on":
				self.screen.doHistory=1
			elif args[0] == "off":
				self.screen.doHistory=0
				self.screen.history.clear()
			elif args[0] == "clear":
				self.screen.history.clear()
#			try:
#				newValue = int(args[0])
#   				if newValue <= 101 and newValue > 0 :
#					pass
#			except ValueError:
#				pass
		else:
			self.screen.printMessage("/"+mess)

chat=Sschat()
chat.main()
