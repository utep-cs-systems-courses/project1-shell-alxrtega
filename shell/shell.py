#! /usr/bin/env python3

import os, sys, re

class Shell:

    def __init__(self):
        self.executeCommand()

    def executeCommand(self):  
        #command prompt
        while 1:
            currentPath = os.getcwd()
            command = input(currentPath + "\n$ ")
            if command == "exit":
                sys.exit(0)
            elif command == "ls":
                self.listDir()
            elif ">" in command or "<" in command:
                self.specialCommand(command)
            elif "|" in command: 
                self.pipeCommand(command)
            else: 
                tokens = command.split()
                if tokens[0] == "cd":
                    self.changeDirectory(tokens[1])
                elif tokens[0] == "echo":
                    self.echoPrint(tokens[1:])
                else:
                    print(command+": command not found")

    def changeDirectory(self, path):
        try:
            os.chdir(path)
        except:
            print("No such file or directory")

    def echoPrint(self, string):
        print(' '.join(string))

    def listDir(self):
        print(" ".join(os.listdir()))

    def specialCommand(self, command):
        pid = os.getpid()
        newProcess = os.fork()
        args = command

        if newProcess < 0:
            os.write(2, ("Fork failed, returning %d\n" % newProcess).encode())
            sys.exit(1)
        elif newProcess == 0:      
            if '>' in args:
                redirect = command.split('> ')
                os.close(1)
                os.open(redirect[1], os.O_CREAT | os.O_WRONLY);
                os.set_inheritable(1, True)
                self.exeCommand(redirect[0])
            if '<' in args:
                redirect = command.split('< ')
                os.close(0)
                os.open(redirect[1], os.O_RDONLY);
                os.set_inheritable(0, True)
                self.exeCommand(redirect[0])
            self.exeCommand(args)
        else:
            if not '&' in args: #background task
                waiting = os.wait()

    def pipeCommand(self, command):
        cmd1, cmd2 = command.split('|')    
        pr, pw = os.pipe()
        for f in (pr, pw):
            os.set_inheritable(f, True)

        newProcess = os.fork()
        if newProcess < 0:
            print("fork failed, returning %d\n" %rc, file=sys.stderr)
            sys.exit(1)
        elif newProcess == 0:
            os.close(1)         #redirect child's stdout
            os.dup(pw)
            os.set_inheritable(1, True)
            for fd in (pr, pw):
                os.close(fd)
            self.exeCommand(command[0:command.index('|')])                    
        else:
            os.close(0)
            os.dup(pr)
            os.set_inheritable(0, True)
            for fd in (pw, pr):
                os.close(fd)
            self.exeCommand(command[command.index('|') + 1:])

    def exeCommand(self, command):
        args = command.split()
        for dir in re.split(":", os.environ['PATH']): #try each directory in the path
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) #try to exec program
            except FileNotFoundError:                #this is expected
                pass                                 #fail quietly                
        os.write(2, ("Command %s not found. Try again.\n" % args[0]).encode())
        sys.exit(1)                                  #terminate with error
        
run = Shell()