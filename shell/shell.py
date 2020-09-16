#! /user/bin/env python3

import os, sys, re

class Shell:

    def __init__(self):
        self.pid = os.getpid()
        self.executeCommand()

    def executeCommand(self):        
        print("process:",self.pid)
        #command prompt
        while 1:
            currentPath = os.getcwd()
            command = input(currentPath + "\n$ ")
            if command == "exit":
                break
            tokens = command.split()
            if(tokens[0] == "cd"):
                self.changeDirectory(tokens[1])
            if(tokens[0] == "echo"):
                self.echoPrint(tokens[1])

    def changeDirectory(self, path):
        try:
            os.chdir(path)
        except:
            print("No such file or directory")

    def echoPrint(self, string):
        print(string)

        """
        newProcess = os.fork()
        if newProcess < 0:
            os.write(2, ("Fork failed: (%d\n" % newProcess).encode())
            sys.exit(1)
            """

run = Shell()