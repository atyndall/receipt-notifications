import os, sys
import win32print
import textwrap


class Printer:
  PRINTER_NAME = "ReceiptPrinter"
  LINE_WIDTH = 40
  lines = []

  def red(self, data):
    return self.fmt(data, False, True)
    
  def wide(self, data):
    return self.fmt(data, True, False)

  def black(self, data):
    return self.fmt(data, False, False)
    
  def fmt(self, data, double_width=False, red=False):
    data = data.encode('latin1', 'replace').replace('\r\n', ' ').replace('\n', ' ')
    data = self.sanitise(data)
    
    if double_width and not red:
      data = "".join("\0\x1E" + c + "\x1F\0" for c in data)
      
    if red and not double_width:
      data = "".join("\0\x12" + c + "\x12\0" for c in data)
      
    if red and double_width:
      data = "".join("\x1E\x12" + c + "\x12\x1F" for c in data)
      
    if not red and not double_width:
      data = "".join("\0\0" + c + "\0\0" for c in data)
      
    return data
    
  def wrap(self, data, width=None):
    if data == "":
      return ""
  
    if width is None:
      width = self.LINE_WIDTH
  
    accumulate = ""
    out = ""
    count = 0
    
    if len(data) % 5 != 0:
      print("error on encoding!?")
      print(data)
    
    n = 5
    split = [[data[i+2], data[i:i+n]] for i in range(0, len(data), n)]
    orig_str = "".join(s[0] for s in split)
    new_str = "\n".join(textwrap.wrap(orig_str, width))
    
    ret_str = ""
    offset = 0
    for i, c in enumerate(new_str):
      if c == "\n":
        offset += 1
        ret_str += c
      else:
        ret_str += split[i - 0][1]
    
    return ret_str.replace("\0", "")
    
  def sanitise(self, data):
    lowest = int(0x20)
    highest = int(0xFF)
    
    ret = ""
    for c in data:
      o = ord(c)
      if o < lowest or o > highest:
        ret += "?"
      else:
        ret += c
        
    return ret

  def add_line(self, data, double_width=False):
    if double_width:
      self.lines.append(self.wrap(data), width=self.LINE_WIDTH/2)
    else:
      self.lines.append(self.wrap(data))
    
  def output(self):
    hPrinter = win32print.OpenPrinter(self.PRINTER_NAME)
    try:
      hJob = win32print.StartDocPrinter (hPrinter, 1, ("Notification", None, "RAW"))
      try:
        win32print.StartPagePrinter (hPrinter)
        win32print.WritePrinter (hPrinter, "\x1B\x63\x1B\x78" + "\n".join(self.lines) + "\x0C")
        win32print.EndPagePrinter (hPrinter)
      finally:
        win32print.EndDocPrinter (hPrinter)
    finally:
      win32print.ClosePrinter (hPrinter)
      self.lines = []
    