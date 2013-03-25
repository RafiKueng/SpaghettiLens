# coding: utf-8

import requests as rq
s = rq.Session()
r1 = s.get("http://admin.masterlens.org/member.php")
data = {'ipaddress':'217.162.244.23', 'member':'Login', 'password': '4-citizens', 'username':'rafi'}
r2 = s.post("http://admin.masterlens.org/member.php", data = data)
r2.text
r3 = s.get("http://admin.masterlens.org/search.php?")
r3
r3.text
import bf4
import beautifulsoup4
import beautifulsoup
import bs4
soup = bs4.BeautifulSoup(r3.text)
soup
soup = bs4.BeautifulSoup(r3.text)
soup = bs4.BeautifulSoup(r2.text)
soup 
soup = bs4.BeautifulSoup(r3.text)
get_ipython().magic(u"save 1-32")