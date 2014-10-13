#!/usr/bin/python
#Author: Nguyen Duc Trung Dung - Network Operator (SPSVietNam) - ndtdung@spsvietnam.vn
#Personal email: dung.nguyendt@gmail.com
#Blog: http://ndtdung.blogspot.com/
#Check_peplink_wan
#Check WAN Interface status of Peplink device
#Version 1.0 : Initial version
#License: GPLv2
#Requires python modules: mechanize, BeautifulSoup
#-------------------------------------------------------

import sys, optparse
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

#Get option
optp = optparse.OptionParser()
optp.add_option('-H', '--host', help='hostname or ipaddress', dest='ip')
optp.add_option('-i', '--interface', help='WAN interface to check', dest='inf')
optp.add_option('-u', '--user', help='username', dest='user')
optp.add_option('-p', '--password', help='password', dest='password')
optp.add_option('-a', '--auth', help='use authentication file instead. Fisrt line: username. Second line: password', dest='auth')
opts, args = optp.parse_args()
if opts.ip is None or opts.inf is None:
    optp.print_help()
    sys.exit(2)
if opts.auth is None:
    if opts.user is None or opts.password is None:
        print 'Error: You must specify username and password'
        sys.exit(2)
    else:
        user = opts.user
        pwd = opts.password
else:
    try:
        f = open(opts.auth, 'r')
    except IOError, e:
        print 'CRIT -', e
        sys.exit(2)
    info = f.read().split('\n')
    f.close()
    user = info[0]
    pwd = info[1]

#Login function
br = Browser()
def login(br, url, username, password):
    br.open(url)
    #Get the form used by normal user to logon
    br.select_form(name="login_form")
    #send login information
    br.form["username"] = username
    br.form["password"] = password
    br.submit() #submit form

#Split tags
def splittag(string):
    return string[3:len(string)-2]

#Read info
def getinfo(name):
    infos = soup.findAll(name)
    for info in infos:
        clean = info.findAll(text=True)
        return splittag(str(clean))

#Main
try:
    int(opts.inf)
except ValueError:
    print 'Interface should contains only number...'
    sys.exit(2)
login(br, 'https://' + opts.ip + '/cgi-bin/MANGA/index.cgi', user, pwd)
page = br.open('https://' + opts.ip + '/cgi-bin/MANGA/wanstatus_v2.cgi?wanlink=' + opts.inf)
soup = BeautifulSoup(page.read().encode('utf-8'))
if 'Connected' in getinfo('status_message'):
    print 'OK - Interface WAN %s (%s): %s, %s, Gateway: %s, DNS:%s %s' %(opts.inf, getinfo('name'), getinfo('ip'), getinfo('status_message'), getinfo('gateway'), getinfo('dns'), getinfo('moredns'))
    sys.exit(0)
else:
    print 'CRIT - Interface WAN %s (%s): %s, %s!, Gateway: %s, DNS:%s %s' %(opts.inf, getinfo('name'), getinfo('ip'), getinfo('status_message'), getinfo('gateway'), getinfo('dns'), getinfo('moredns'))
    sys.exit(2)
