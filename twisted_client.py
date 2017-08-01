#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import print_function

from twisted.internet import task
from twisted.internet.defer import Deferred
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver



class EchoClient(LineReceiver):
    end = "Bye-bye!"

    def connectionMade(self):
        self.sendLine("req")
        #self.sendLine("What a fine day it is.")
        #self.sendLine(self.end)
	print("sent req")


    def lineReceived(self, line):
        print("receive:", line)
	self.sendLine("post_1_FF:FF:FF:FF:FF:E9")
        if line == self.end:
            self.transport.loseConnection()



class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def __init__(self):
        self.done = Deferred()


    def clientConnectionFailed(self, connector, reason):
        print('connection failed:', reason.getErrorMessage())
        self.done.errback(reason)


    def clientConnectionLost(self, connector, reason):
        print('connection lost:', reason.getErrorMessage())
        self.done.callback(None)



def main(reactor):
    factory = EchoClientFactory()
    reactor.connectTCP('localhost', 11000, factory)
    return factory.done



if __name__ == '__main__':
    task.react(main)
