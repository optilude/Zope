#!/usr/local/bin/python1.5.1
"""ZServer configuration and start script

You should make a copy of this file, then add, change or comment out
appropriately. Then you can start up the server by simply typing

  python start.py
  
You may also want to use a shell script (under Unix) or a bath file (under
win32) to set environment variables and run this script.

For more information on Medusa see http://www.nightmare.com/medusa/
"""
import os

### Zope configuration
###

# This should point to your Zope directory
INSTANCE_HOME='d:\\program files\\1.10.2'

### ZServer configuration 
###

## HTTP configuration
##

# This is the IP address of the network interface you want your servers to
# be visible from.  This can be changed to '' to listen on all interfaces.
IP_ADDRESS=''

# Host name of the server machine. You may use 'localhost' if your server 
# doesn't have a host name.
HOSTNAME='localhost'

# IP address of your DNS server. If you have DNS service on your local machine
# then you can set this to '127.0.0.1'
DNS_IP='205.240.25.3'

# Port for HTTP Server. The standard port for HTTP services is 80.
HTTP_PORT=9673

# Module to publish. If you are not using the Zope management framework,
# this should be the name of your published module. Note that this module
# must be accessible in the Python path.
MODULE='Main'

# Location of the ZServer log file. This file logs all ZServer activity.
# You may wish to create different logs for different servers. See
# medusa/logger.py for more information.
LOG_FILE=os.path.join(INSTANCE_HOME,'var','ZServer.log')

## FTP configuration
##

# Port for the FTP Server. The standard port for FTP services is 21.
FTP_PORT=8021

## PCGI configuration

# You can configure the PCGI server manually, or have it read its
# configuration information from a PCGI info file.
PCGI_FILE=os.path.join(INSTANCE_HOME,'Zope.cgi')

# Add Zope to the Python path first.
# If you are using a binary release of Zope, you may need
# to add additional paths here.
#
import sys
sys.path.insert(0,os.path.join(INSTANCE_HOME,'lib','python'))

from medusa import resolver,logger,http_server,asyncore
from HTTPServer import zhttp_server, zhttp_handler
from PCGIServer import PCGIServer
from FTPServer import FTPServer

## ZServer startup
##

# To disable some of the servers simply comment out the relevant stanzas. 

# Resolver and Logger, used by other servers
rs = resolver.caching_resolver(DNS_IP)
lg = logger.file_logger(LOG_FILE)

# HTTP Server
hs = zhttp_server(
	ip=IP_ADDRESS,
	port=HTTP_PORT,
	resolver=rs,
	logger_object=lg)

zh = zhttp_handler(MODULE,'')
hs.install_handler(zh)

# PCGI Server
zpcgi = PCGIServer(
	ip=IP_ADDRESS,
	pcgi_file=PCGI_FILE,
	resolver=rs,
	logger_object=lg)

# FTP Server	
zftp = FTPServer(
	module=MODULE,
	hostname=HOSTNAME,
	port=FTP_PORT,
	resolver=rs,
	logger_object=lg)


# Try to become nobody. This will only work if this script is run by root.
try:
	import pwd
	try:
		nobody = pwd.getpwnam('nobody')[2]
	except pwd.error:
		nobody = 1 + max(map(lambda x: x[2], pwd.getpwall()))
	os.setuid(nobody)
except:
	pass

# Start Medusa
asyncore.loop()


