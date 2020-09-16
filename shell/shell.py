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
            path = os.getcwd()
            command = input(path + "\n$ ")
            if command == "exit":
                break
            tokens = command.split()
            print(tokens)

        """
        newProcess = os.fork()
        if newProcess < 0:
            os.write(2, ("Fork failed: (%d\n" % newProcess).encode())
            sys.exit(1)
            """

run = Shell()