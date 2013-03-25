# coding: utf-8
import requests as rq
s = rq.Session()
r1 = s.get("http://admin.masterlens.org/member.php")
data = {'ipaddress':'217.162.244.23', 'member':'Login', 'password': '4-citizens', 'username':'rafi'}
r2 = s.post("http://admin.masterlens.org/member.php", data = data)
r3 = s.get("http://admin.masterlens.org/search.php?")
ldata = {'backgroundID': '0', 'by_member_name': 'All Members (*)', 'date_option': 'Discovered', 'discoveryID': '0', 'displaypage': '0', 'do': '', 'foregroundID': '0', 'hrefaction': '', 'inputaction': 'Search', 'lensID': '22', 'lensgrade': 'All Grades (*)', 'lenssort': '0', 'mode': '', 'or_by': 'modified_by', 'referenceID': '', 'searchoption': 'basic', 'special': '', 'status': '', 'substatus': '', 'xml': ''}
r4 = s.post("http://admin.masterlens.org/search.php?", data = ldata)
from bs4 import BeautifulSoup
s10 = BeautifulSoup(r4.text, "html5lib")
s10 
r10 = s.get("http://admin.masterlens.org/graphic.php?lensID=479&type=1&")
s11 = BeautifulSoup(r10.text, "html5lib")
s11 
s12 = s11.body.table.tbody
s12 
s13 = s12.find('img')
s13 
s13.src
s13.attrs
s13.attrs['src']