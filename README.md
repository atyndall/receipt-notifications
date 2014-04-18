Have you ever found an old Citizen iDP-460 receipt printer being thrown away?

Have you ever wanted to output your emails, Facebook notifications and friend's private anonymous messages to said printer?

I know I have, that's why I've created this awfully hacky set of Python scripts to allow for just that.

Basic configuration steps:
 # Install necessary Python libraries
 # Copy configuration from config.example.py to config.py and fill it out
 # Copy contents of 'talkatme' to a remote webserver that can run Python CGI scripts
 # Configure receipt printer over parallel or USB to parallel with the Windows "Generic / Text Only" driver 
 # Name the configured printer "ReceiptPrinter"
 # (if you're not on Windows, hack printer.py so that it writes to the Linux /dev/lp0 or /dev/usb/lp0 file)
 # ????
 # Profit!

 