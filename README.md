Receipt Notifications
=========

Have you ever found an old Citizen iDP-460 receipt printer being thrown away?

Have you ever wanted to output your emails, Facebook notifications and friend's private anonymous messages to said printer?

I know I have, that's why I've created this awfully hacky set of Python scripts to allow for just that.

Basic configuration steps:
1. Install necessary Python libraries
2. Copy configuration from config.example.py to config.py and fill it out
3. Copy contents of 'talkatme' to a remote webserver that can run Python CGI scripts
4. Configure receipt printer over parallel or USB to parallel with the Windows "Generic / Text Only" driver 
5. Name the configured printer "ReceiptPrinter"
6. (if you're not on Windows, hack printer.py so that it writes to the Linux /dev/lp0 or /dev/usb/lp0 file)
7. ????
8. Profit!

![Message output](https://github.com/atyndall/receipt-notifications/raw/master/talkatme/talk1.jpg)

![The printer in its natural environment](https://github.com/atyndall/receipt-notifications/raw/master/talkatme/talk2.jpg)