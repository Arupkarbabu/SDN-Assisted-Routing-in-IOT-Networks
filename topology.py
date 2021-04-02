#!/usr/bin/python

import sys
from mininet.log import setLogLevel, info
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.link import adhoc
from mininet.node import RemoteController

def topology():
    "Create a network."
    net = Mininet_wifi(controller=RemoteController)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1',position='10,43,0',range=5)
    sta2 = net.addStation('sta2',position='24,41,0',range=5)
    sta3 = net.addStation('sta3',position='63,51,0',range=5)
    sta4 = net.addStation('sta4',position='77,48,0',range=5)

    ap1 = net.addAccessPoint('ap1', ssid='ssid_1', mode='g', channel='1',position='17.86,53.017,0', range=20)

    ap2 = net.addAccessPoint('ap2', ssid='ssid_2', mode='g', channel='1',position='71,57,0', range=20)




    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1',port=6633,position='42,86,0', range=5)

    net.setPropagationModel(model="logDistance", exp=5)
    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.plotGraph(max_x=100, max_y=100)

    info("*** Associating...\n")
    net.addLink(ap1, sta1)
    net.addLink(ap1, sta2)
    net.addLink(sta1, intf='sta1-wlan0', cls=adhoc, ssid='adhocNet')
    net.addLink(sta2, intf='sta2-wlan0', cls=adhoc, ssid='adhocNet')
    net.addLink(ap2, sta3)
    net.addLink(ap2, sta4)
    net.addLink(sta3, intf='sta3-wlan0', cls=adhoc, ssid='adhocNet1')
    net.addLink(sta4, intf='sta4-wlan0', cls=adhoc, ssid='adhocNet1')





    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])


    info("*** Addressing...\n")
    sta1.setIP('192.168.10.1/24', intf="sta1-wlan0")
    sta2.setIP('192.168.10.2/24', intf="sta2-wlan0")
    sta3.setIP('192.168.10.3/24', intf="sta3-wlan0")
    sta4.setIP('192.168.10.4/24', intf="sta4-wlan0")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()