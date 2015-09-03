#!/usr/bin/env python

'''

read a text file and pass each line to a pool of forked workers

'''

from multiprocessing import Process, Queue
import sys

num_of_workers = 8


def worker(q):
    quit = True
    while quit:
        try:
            d = q.get(0.01)
        except:
            pass
        else:
            if type(d) == type(True):
                quit = d
            else:
                print "processing line: %s" % (d)

if __name__ == '__main__':
    q = Queue()
    workers = {}
    for i in range(0,num_of_workers):
        workers[i] = Process(target=worker, args=(q,))
        workers[i].start()

    # do some work here

    f = open(sys.argv[1],"r") # open sys.argv[1]
    for i in f.readlines():
        i = i.replace("\n","")
        i = i.replace("\r","")
        q.put(i)
    # close all the jobs
    for i in range(0,num_of_workers):
        q.put(False)
    for i in range(0,num_of_workers):
        workers[i].join()
