#!/usr/local/bin/python

import cgi #forms and such
import bsddb #berkeley db, hashes on disk, wee
import marshal #turning things into strings with dumps and back again with loads
#import cgitb #for debugging only
#cgitb.enable()

def printValUser(which, userTaken):
  if formData[which] is not None:
    print 'value="' + formData[which] + '" '
    print '/>'
    if userTaken:
      print '<font color=red><-Duplicated username, pick again!</font>'
  else:
    print '/> <font color=red><-Pick anything you like, @twitter handle, email, etc., must be unique</font>'
  print '</p>'

def printVal(which):
  print '''<p><input type="radio" name="answer%d" value="left" ''' % which
  if formData[which] == 'left':
    print " checked "
  print '''/>Left'''
  print '''<input type="radio" name="answer%d" value="right" align="right" ''' % which
  if formData[which] == 'right':
    print " checked "
  print '''/>Right '''
  if formData[which] is None:
    print '<font color=red><-Pick one</font>'
  print '</p>'

print 'Content-type: text/html\n\n'
print '<html><body>\n'

datadb = bsddb.hashopen("data.bdb")

form = cgi.FieldStorage()

varList = ["username", "answer1", "answer2", "answer3", "answer4", \
"answer5", "answer6", "answer7", "answer8"]
formData = []

allFilledIn = True
for variable in varList:
  data = form.getvalue(variable)
  if data is None:
    allFilledIn = False
  formData.append(data)

usernameTaken = False
if datadb.has_key(formData[0]):
  usernameTaken = True
  allFilledIn = False

if not allFilledIn:
  print '''<form method="post" action="quiz.cgi">
        <p>Username: <input type="text" name="username" '''
  printValUser(0, usernameTaken)
  print '''<h2>Pick the form of the molecule that you think is dominant at pH=7.4</h2><p>There are right/wrong answers, but I don't know them.<br>''' 
  for answerCount in xrange(1, 9):
    print '''<img src=%d.jpg></p>''' % answerCount  
    printVal(answerCount)
  

  print '''<p><input type="submit" name="submit" value="Send in your answers!" /></p>'''

  print '''   </form>'''

if allFilledIn: #actually add to the database!
  datadb[formData[0]] = marshal.dumps(formData[1:9]) #store
  print "<p><h1>Your answers have been recorded. Thank you!!</h1></p>"
  datadb.sync()
datadb.close()


print "</body></html>"
