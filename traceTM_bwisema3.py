#! /usr/bin/env python3
import sys


class TM:
    def __init__(self):
        self.flag

    def TM_print(self):
        pass

    def TM_trace(self):
        pass

    def TM_output(self):
        pass

def read_input(file_in):
    pass

def usage(rc):
    print("Usage: ./python3 traceTM_bwisema3.py [filename] [options] [input_strings]")
    print("\n[filename]:\n\tname of file")
    print("\n[options]:\n\t-h:   help message\n\t-t N: terminate after N transitions")
    print("\n[input_strings]:\n\tlist of strings to run")
    return rc

def main():

    if(len(sys.argv) < 2):
        return usage(1)

    flag = ''
    args = sys.argv[1:]
    filename = args.pop(0)

    strings = []
    
    while(len(args) != 0):
        arg = args.pop(0)
        if(arg == "-t"):
            flag = int(args.pop())
        elif(arg == "-h"):
            return usage(1)
        else:
            strings.append(arg)

    print(strings)

if __name__ == "__main__":
    main()
