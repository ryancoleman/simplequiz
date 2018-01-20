#!/usr/local/bin/python

import cgi #forms and such
import bsddb #berkeley db, hashes on disk, wee
import marshal #turning things into strings with dumps and back again with loads
#import cgitb #for debugging only
#cgitb.enable()

datadb = bsddb.hashopen("data.bdb", 'r')

for username in datadb.keys():
  print username, marshal.loads(datadb[username])

datadb.close()
