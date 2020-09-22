import os, sys, re
'''
@Author Alejandro Ortega
class Shell will emulate a bash terminal
'''
class Shell:

    def __init__(self):
        self.executeCommand()

    '''
    executeCommand will manage the commands that invoke methods 
    that are required to successfully emulate a bash terminal
    '''
    def executeCommand(self):  

        #command prompt
        while 1:

            command = self.getUserInput()

            if command == "exit":
                sys.exit(0)
            elif ">" in command or "<" in command:
                self.redirection(command)
            elif "|" in command: 
                self.pipeCommand(command)
            elif "cd" in command: 
                tokens = command.split()
                self.changeDirectory(tokens[1])
            else:
                self.runCommand(command)
                pass

    def getUserInput(self):
        currentPath = os.getcwd()
        print(currentPath + "\n$ ", end = " ")
        userInput = os.read(0, 128)
        userInput = userInput.decode().split("\n")
        userInput = userInput[0]
        userInput = str(userInput)
        
        return userInput

    '''
    runCommand() will manage the commands
    it will create a new process to run the command in it
    to run the desired commands
    '''
    def runCommand(self, command):
        args = command.split()
        pid  = os.getpid()

        newProcess = os.fork()
        if newProcess < 0:

            os.write(2,("Fork failed.").encode())
            sys.exit(1)

        elif newProcess == 0:

            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])

                try:
                    os.execve(program, args, os.environ) 
                except FileNotFoundError:                
                    pass                                 

            os.write(2, ("Command %s not found. Try again.\n" % args[0]).encode())
            sys.exit(1)                                  

        else: 
            waiting = os.wait()

    '''
    changeDirectory() will manage the directory change
    '''
    def changeDirectory(self, path):
        try:
            os.chdir(path)
        except:
            os.write(1, "No such directory\n".encode())

    '''
    redirection() will manage the command redirection, it will
    define if the command contains an input or output redirection
    it will have to create a new process to run both commands that 
    are linked by '<' or '>'
    '''
    def redirection(self, command):
        newProcess = os.fork()

        if newProcess < 0:

            os.write(2, ("Fork failed, returning %d\n" % newProcess).encode())
            sys.exit(1)

        elif newProcess == 0: 

            if '>' in command:

                redirect = command.split('>')
                os.close(1)
                os.open(redirect[1], os.O_CREAT | os.O_WRONLY)
                os.set_inheritable(1, True)
                self.runCommand(redirect[0])

            if '<' in command:

                redirect = command.split('<')
                os.close(0)
                os.open(redirect[1], os.O_RDONLY)
                os.set_inheritable(0, True)
                self.runCommand(redirect[0])

            self.runCommand(command)
        else:
            if not '&' in command:
                waiting = os.wait()

    '''
    pipeCommand() will manage piping to emulate the terminals by splitting the command
    by the '|' character and then it will run both commands in different processes
    '''
    def pipeCommand(self, command):
        cmd1, cmd2 = command.split('|')    
        pr, pw = os.pipe()

        for f in (pr, pw):
            os.set_inheritable(f, True)

        newProcess = os.fork()
        if newProcess < 0:

            os.write(1, "fork failed, returning %d\n" %newProcess)
            sys.exit(1)

        elif newProcess == 0:

            os.close(1)        
            os.dup(pw)
            os.set_inheritable(1, True)
            for fd in (pr, pw):
                os.close(fd)
            self.runCommand(cmd1)                    

        else:

            os.close(0)
            os.dup(pr)
            os.set_inheritable(0, True)
            for fd in (pw, pr):
                os.close(fd)
            self.runCommand(cmd2)
        
run = Shell()