#!/usr/bin/env python

'''
create an interactive shell and listen on a port
liam@slacker.com

'''

import thread
import socket
import SocketServer
import time
import traceback
import sys
        
class _handler(SocketServer.StreamRequestHandler):

    def handle(self):
        main = sys.modules['__main__']
        
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        while True:
            self.wfile.write(">>> ")
            self.data = self.rfile.readline().strip()
            if self.data == "quit" or self.data == "exit":
                break
            myvar = ""
            save = sys.stdout
            sys.stdout = self.wfile
            try:
                exec(self.data)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print "exception"
                myvar = "".join(traceback.format_exception(exc_type, exc_value,
                                              exc_traceback))
            sys.stdout = save
            
            # Likewise, self.wfile is a file-like object used to write back
            # to the client
            self.wfile.write(myvar)

class socketshell():
    def __init__(self):
        pass
    
    class Threader():
        def __init__(self,socketshell):
            self.socketshell=socketshell
        def run(self,lock):
            self.threaderlock = lock
            SocketServer.TCPServer.allow_reuse_address = True
            self.s = SocketServer.ThreadingTCPServer(("127.0.0.1", self.socketshell.port), _handler)
            self.s.serve_forever()
        
    def start(self,port):
        self.port = port
        self._threader = self.Threader(self)
        self.lock = thread.allocate_lock()
        self.lock.acquire()
        thread.start_new_thread(self._threader.run,(self.lock,)) 

if __name__ == "__main__":
    ss = socketshell()
    ss.start(port)
