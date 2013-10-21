ss(c)h(at)
===================
No-Log, IRC type, ssh securised, chat.  

### INSTALL


First, clone or download sschat

```
git clone https://github.com/sl4shme/sschat.git
```

And next, to install juste create 2 users:
- One to add any key with key.py in shell
- One to connect to the chat with sschat.py in shell

```bash
cat /etc/passwd
...
sschat:x:1000:1000:,,,:/sschat:/sschat/sschat.py  
key:x:1001:1001:,,,:/sschat/key:/sschat/key/key.py  
...
```

And add this line to /etc/sudoers

```
key ALL=(ALL) NOPASSWD: /sschat/key/keycat.sh
```

### USAGE

If sschat user has a password just connect with sshchat user, else add your key with the key user.
One connected choice a username and a channel.

### COMMANDS

```
/help : Display this help, use j/k to navigate and q to quit.
/list : List peoples in channel.
/clear : Clear your screen.
/paste : Enter paste mode, usefull for pasting long links.
/quit [message] : Quit with an optional [message].
/history [on|off|clear] : With no argument, display the last 100 message.
/nickname <newNickname> : Change your nickname.
/channel <newChannelName> : Switch channel.
/pm <id> <message> : Send a private message to the user with the id <id>
/bug <message> : Send a bug / suggestion report.
/timestamp <on|off> : Enable/disable line timestamping.
/notif <on|off> : Toggle visual flash notification on new message.
/afk : Toggle afk.
/encrypt <on|off> : Toggle encryption.
```
