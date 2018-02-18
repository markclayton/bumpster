#!/bin/sh 

pip install dnsdumpster -t . 
rm -rf requests*
rm -rf urllib3* 
cp DNSDumpsterAPI_urllib2.py dnsdumpster/DNSDumpsterAPI.py
