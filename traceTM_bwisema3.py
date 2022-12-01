#! /usr/bin/env python3
import sys

class TM:
    '''Class representing a TM'''
    def __init__(self, name, states, sigma, T, start, accept, reject, graph):
        '''Constructor'''
        self.flag = 100
        self.strings = []

        self.name = name
        self.states = states
        self.sigma = sigma
        self.T = T
        self.start = start
        self.accept = accept
        self.reject = reject
        self.graph = graph

        self.depth = 0
        self.max_depth = 0
        self.num_trans = 0
        self.transitions = []

    def TM_print(self):
        '''Print out info about TM'''
        print(f'Name: {self.name}')
        print(f'Strings: {self.strings}')
        print(f'Max Depth: {self.max_depth}')
        print(f'Number of Transitions: {self.num_trans}')
        print("(depth and transitions counted across all strings)\n")

    def TM_trace(self):
        '''Trace a TM on list of strings'''
        start = self.start

        # add empty string if none provided
        if not self.strings:
            self.strings.append("")

        # do all strings
        for string in self.strings:
            self.transitions.append((string, self.TM_trace_r(start, list(string + "_")), self.depth, self.max_reached))
            if(self.depth > self.max_depth):
                self.max_depth = self.depth

        # print out TM
        self.TM_print()

        # print out output
        for trans in self.transitions:
            self.TM_output(trans[1], trans[0], trans[2], trans[3])

    def TM_trace_r(self, start, string):
        '''Private(ish) trace call for each string'''
        self.depth = 0
        self.max_reached = False

        # add initial state (name of state, index of tapehead, hist)
        h = []
        new = (start, 0, h)

        # create queue 
        queue = []
        queue.append(new)
        
        # while we have configs and below threshold, loop
        while(queue and not self.max_reached):
            self.depth += 1
            src, index, hist = queue.pop(0)

            # if found accept state, make sure we have finished string before accepting, else continue
            if src in self.accept:
                if index == len(string):
                    index += 2
                    self.num_trans += 1
                    hist.append(''.join(string[:index]+[src]+string[index:]))
                    return hist.copy()
                else:
                    continue

            if index >= len(string):
                continue

            # increase num of trans, and add new tranisitons to queue
            self.num_trans += 1
            letter = string[index]
            if letter in self.graph[src]:
                for trans in self.graph[src][letter]:
                    if trans[2] == "R":
                        x = index + 1
                    elif trans[2] =="L":
                        if index == 0:
                            x = index
                        else:
                            x = index - 1
                    else:
                        x = index + 1
                    
                    # need to pop since local copy
                    hist.append(''.join(string[:index] + [src] + string[index:]))
                    queue.append((trans[0], x, hist.copy()))
                    hist.pop()
            
            # check make depth flag
            if(self.depth == self.flag):
                self.max_reached = True

        # empty string means reject
        return None

    def TM_output(self, path, string, depth, max_reached):
        '''Prints output for a string'''
        if(path):
            print(f'String ({string}) accepted in {depth} and had the following path')
            print(','.join(path))
        else:
            if max_reached:
                print("Max depth reached for ({string})")
            else:
                print(f'String ({string}) rejected in {depth}')
        print("")


def read_input(file_in):
    '''Read input and convert to a TM'''
    fin = open(file_in, "r")

    name = fin.readline().split(',')[0]
    states = fin.readline().strip('\n,').split(',')
    sigma = fin.readline().strip('\n,').split(',')
    T = fin.readline().strip('\n,').split(',')
    start = fin.readline().split(',')[0]
    accept = fin.readline().split(',')[0]
    reject = fin.readline().split(',')[0]

    # {current state: {see this letter : [(goto this state, write this letter, move this way)]}}
    # dict of all states with value of dict of possible letters to see with value of list of transitions to take
    graph = {}
    while(line := fin.readline().strip('\n')):
        src, read, dest, write, move = line.split(',')
        
        if src not in graph:
            graph[src] = {read : [(dest, write, move)]}
        else:
            if read not in graph[src]:
                graph[src][read] = [(dest, write, move)]
            else:
                graph[src][read].append((dest, write, move))

    return TM(name, states, sigma, T, start, accept, reject, graph)

def usage(rc):
    '''Print usage'''
    print("Usage: ./python3 traceTM_bwisema3.py [filename] [options] [input_strings]")
    print("\n[filename]:\n\tname of file")
    print("\n[options]:\n\t-h:   help message\n\t-t N: terminate after N transitions")
    print("\n[input_strings]:\n\tlist of strings to run")
    return rc

def main():
    '''Main execution'''

    # check args
    if(len(sys.argv) < 2):
        return usage(1)

    # init
    flag = ''
    args = sys.argv[1:]
    filename = args.pop(0)
    strings = []
    
    # read args
    while(len(args) != 0):
        arg = args.pop(0)
        if(arg == "-t"):
            flag = int(args.pop())
        elif(arg == "-h"):
            return usage(1)
        else:
            strings.append(arg)

    # set up tm and trace
    tm = read_input(filename)
    tm.strings = strings
    if(flag):
        tm.flag = int(flag)

    tm.TM_trace()

if __name__ == "__main__":
    main()
