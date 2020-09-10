#alex ortega
import os, sys, re

class Shell:

    def __init__(self):
        self.pid = os.getpid()
        print("process: ", self.pid)
        while 1:
            command = input()
            command.strip()
            if command == "exit":
                break
            print("command: ", command)


run = Shell()