check_peplink_wan
=================
Requires: python module mechanize & BeautifulSoup

Check WAN connection status for Peplink Balance 1350. Return OK if WAN is connected (included IP, Gateway, DNS), CRIT for other status.

Usage: check_peplink_wan.py [options]

Options:
-h, --help show this help message and exit
-H IP, --host=IP hostname or ipaddress
-i INF, --interface=INF
WAN interface to check
-u USER, --user=USER username
-p PASSWORD, --password=PASSWORD
password
-a AUTH, --auth=AUTH use authentication file instead.

Authentication file sample:
myuser #1st line
mypassword #2nd line
