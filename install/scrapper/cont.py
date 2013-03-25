# coding: utf-8
import requests as rq
s = rq.Session()
r1 = s.get("http://admin.masterlens.org/member.php")
data = {'ipaddress':'217.162.244.23', 'member':'Login', 'password': '4-citizens', 'username':'rafi'}
r2 = s.post("http://admin.masterlens.org/member.php", data = data)
r2.text
r3 = s.get("http://admin.masterlens.org/search.php?")
r3.text
BeautifulSoup(r3.text, "html5lib")
from bs4 import BeautifulSoup
BeautifulSoup(r3.text, "html5lib")
soup = BeautifulSoup(r3.text, "html5lib")
s2 = soup.find(id="message-listing")
s2 
s3 = s2.table
s3 
s4 = s3.tbody
s4 
trow = s4.find_all('tr')
len(trow)
trow[0]
trow[1]
cells = trow[0].find_all('td')
len(cells)
cells1 = trow[0].find_all('td')
cells2 = trow[0].find_all('th')
len(cells2)
cells2[1]
import re
id = re.search('sID(?P<id>\d+)img',cells2[1])
id = re.search('sID(?P<id>\d+)img',str(cells2[1]))
id
str(cells2[1])
cells2[0]
cells2[2]
cells2[1]
cells1[0]
cells1[1]
id = re.search('sID(\d+',str(cells1[1]))
id = re.search('sID\(\d+',str(cells1[1]))
id
id.string
id.groups 
id.groups()
id.regs
id.span 
id.span()
id.groups 
id.groups()
id.group()
id = re.search('\(\d+\)',str(cells1[1]))
id
id.group()
id.group()[1:-1]
id = re.search('\(\d+\)',str(cells1[1])).group()[1:-1]
id
print '------------------------------'
ldata = backgroundID0
by_member_nameAll Members (*)
date_optionDiscovered
discoveryID0
displaypage0
get_ipython().magic(u"doctest_mode")
foregroundID0
hrefaction
inputactionSearch
lensID22
lensgradeAll Grades (*)
lenssort0
mode