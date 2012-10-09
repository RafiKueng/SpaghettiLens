#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.websocket

import os, sys
lib_path = os.path.abspath('/home/rafik/myprojects/master/glass')

sys.path.append(lib_path)
import dummy_glass

from time import sleep #used to be able to accept the sleep(x) command

pref = "demo.tornado: "

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print pref+"WebSocket opened"

    def on_message(self, message):
        print "--------------------------"
        print pref + "Got message: " + message
        if message.startswith('b:'):
            print pref + "...witch is a special command, i'll execute it now..."
            try:
                msg = eval(message[2:])
            except:
                print pref + "...but it's no valid expr. : " + message[2:]
                msg = message[2:]
            if msg is None:
                msg = ""
                print pref + "no return value"
            else:
                msg = str(msg)
                print pref + msg
            print pref + "end eval, and still alife..."
            self.write_message(u"[" + message + "] --> ["+msg+"]")
        else:
            #call glass
            print pref + "starting dummyglass"
            msg = dummy_glass.doSomeStuff(message)
            print pref + "from glass i got: " + msg
            self.write_message(u"[" + message + "] --> ["+msg+"]")
            pass

    def on_close(self):
        print pref + "WebSocket closed"


application = tornado.web.Application([
    (r"/", EchoWebSocket),
])

if __name__ == "__main__":
    port=8080
    print pref + "Starting websocket server, litening on port "+str(port)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
