from printer import Printer
import poplib
import time
from email import parser, utils, message_from_string, header
from time import localtime, strftime
import facebook
import imaplib
from datetime import datetime, timedelta
import pytz
import urllib2
import csv
import StringIO  
import re, htmlentitydefs
from config import *

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.

def unescape(text):
  def fixup(m):
    text = m.group(0)
    if text[:2] == "&#":
      # character reference
      try:
        if text[:3] == "&#x":
          return unichr(int(text[3:-1], 16))
        else:
          return unichr(int(text[2:-1]))
      except ValueError:
        pass
    else:
      # named entity
      try:
        text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
      except KeyError:
        pass
    return text # leave as is
  return re.sub("&#?\w+;", fixup, text)
  
  
def to_ascii(data):
  return data.encode('latin-1', 'replace')
  
def header_to_ascii(hdr):
  decodes = header.decode_header(hdr)
  ustr = u''
  for str, charset in decodes:
    ustr += str.decode(charset if charset != None else 'utf-8')
  
  return to_ascii(ustr)
  
def check_mail(last_check):
  #pop_conn = poplib.POP3_SSL(POP_SERVER)
  #pop_conn.user(POP_USERNAME)
  #pop_conn.pass_(POP_PASSWORD)
  #Get messages from server:
  #messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
  # Concat message pieces:
  #messages = ["\n".join(mssg[1]) for mssg in messages]
  #Parse message intom an email object:
  #messages = [parser.Parser().parsestr(mssg) for mssg in messages]
  #pop_conn.quit()
  #return messages
  email = []
  
  conn = imaplib.IMAP4_SSL(IMAP_SERVER)
  try:
      (retcode, capabilities) = conn.login(IMAP_USERNAME, IMAP_PASSWORD)
  except:
      print sys.exc_info()[1]
      sys.exit(1)
      
  #print 'checking'

  conn.select(readonly=1) # Select inbox or default namespace
  query = '(NOT SEEN)'
  (retcode, messages) = conn.search(None, query)
  #print query
  if retcode == 'OK':
      #print messages
      for num in messages[0].split():
          typ, data = conn.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM RECEIVED)])')
          eml = message_from_string(data[0][1])
          
          recieved = eml['Received'].split(';')[1].strip()
          parsedt = utils.parsedate_tz(recieved)
          recieved = datetime.fromtimestamp(utils.mktime_tz(parsedt), pytz.utc)
          
          #print recieved
          #print last_check
          #print recieved - last_check
          if recieved - last_check > timedelta(0, -2):
            frm = header_to_ascii(eml['From'])
            subject = header_to_ascii(eml['Subject'])
            email.append([frm, subject])
          
  conn.close()
  
  return email
    
def check_fb(graph, p):
  notifications = graph.get_object('me/notifications', include_read=False)
  
  read_notifications = []
  notification_texts = []
  
  for n in notifications['data']:
    read_notifications.append(n['id'])
    
    txt = n['title'].decode('utf8')
    frm = n['from']['name'].decode('utf8')

    notification_texts.append([frm, txt])
    
  for n in read_notifications:
    graph.put_object(n, "", unread=0)
    
  return notification_texts
  
  
def check_talktome():
  response = urllib2.urlopen(TAM_LOG_URL)
  urllib2.urlopen(TAM_CLEAR_URL)
  txt = response.read()
  csvr = csv.reader(StringIO.StringIO(txt))
  
  allmsgs = reversed([m for m in csvr])
  
  msgs = []
  for t, frm, msg in allmsgs:
    if t == "CLEAR":
      break
      
    msgs.append((t.decode('latin1'), unescape(frm.decode('latin1')), unescape(msg.decode('latin1')).split("\n")))
    
  return msgs
 

def main():
  p = Printer()
  graph = facebook.GraphAPI(FB_API_KEY)

  last_check = datetime.utcnow()
  last_check = last_check.replace(tzinfo=pytz.utc)

  while True:
    time.sleep(5)
    print "Polling"
    
    try:
      msgs = check_mail(last_check)
      
      last_check = datetime.utcnow()
      last_check = last_check.replace(tzinfo=pytz.utc)
      
      fb = check_fb(graph, p)
      
      talks = check_talktome()
    except:
      print "Issue retrieving data, is there interwebs?"
      continue
      
    prnt = False
    
    if len(msgs) > 0:
      prnt = True
    
      p.add_line(
        p.wide("Email")
      )
      
      p.add_line(
        p.black(strftime("%a, %d %b %Y %X", localtime()))
      )
    
      for frm, subject in msgs:
        
        p.add_line(
          p.black("From: ") +\
          p.red(frm if frm.strip() != "" else "Unknown")
        )
        
        p.add_line(
          p.black("Subject: ") +\
          p.red(subject if subject.strip() != "" else "None")
        ) 
        
        if len(msgs) > 1:
          p.add_line(p.black("\n"))
          
    if len(fb) > 0:
      prnt = True
      
      p.add_line(
        p.wide("Facebook")
      )
      
      p.add_line(
        p.black(strftime("%a, %d %b %Y %X", localtime()))
      )
      
      for frm, txt in fb:
        txt = p.black(txt)
        txt = txt.replace(p.black(frm), p.red(frm))
        
        p.add_line(txt)

        if len(msgs) > 1:
          p.add_line(p.black("\n"))
    
    if len(talks) > 0:
      prnt = True
      
      p.add_line(
        p.wide("Talk At Me")
      )
      
      for t, frm, msg in talks:
      
        p.add_line(
          p.black(t)
        )
        
        p.add_line(
          p.black("From: ") +\
          p.red(frm)
        )
        
        if len(msg) > 6:
          msg = msg[:6]
        
        for m in msg:
          p.add_line(
            p.black(m)
          )
        
        if len(talks) > 1:
          p.add_line(p.black("\n"))
        
    
    if prnt:
      p.output()
      

if __name__ == '__main__':
  main()