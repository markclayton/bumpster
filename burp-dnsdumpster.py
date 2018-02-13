from burp import IBurpExtender
from burp import IContextMenuFactory

from javax.swing import JMenuItem 
from java.util import List, ArrayList 
from java.net import URL 

import socket # probably not needed
import urllib # probably not needed
import json 
import re 
import base64 
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI

class BurpExender(IBurpExtender, IContextMenuFactory):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers   = callbacks.getHelpers() 
        self.context    = None

        callbacks.setExtensionName("Dnsdumpster")
        callbacks.registerContextMenuFactory(self)

        return 

    def createMenuItems(self, context_menu):
        self.context = context_menu 
        menu_list = ArrayList()
        menu_list.add(JMenuItem("Send to Dnsdumpster", actionPerformed=self.dnsdumpster_menu))
        return menu_list

    def dnsdumpster_menu(self, event):
        http_traffic = self.context.getSelectedMessages() 

        print "%d requests highlighted" % len(http_traffic)

        for traffic in http_traffic:
            http_service = traffic.getHttpService() 
            host = http_service.getHost() 

            print "User selected host: %s" % host 

            self.dnsdumpster_search(host) 

        return 

    def dnsdumpster_search(self, host):

        #regex to check if IP or hostname 
        is_ip = re.match("[0-9]+(?:\.[0-9]+){3}", host)

        if is_ip:
            print "[-] Error: %s is not a domain name. Skipping... Unforunately dnsdumpster does not yet support IP/CIDR searches. Use a domain name instead." % host
            domain = False 
        else: 
            domain = True

        #make sure you get the domains 
        if domain: 
            self.dnsdumpster_query(host)

    def dnsdumpster_query(self, host):
        res = DNSDumpsterAPI().search(host)
        print res