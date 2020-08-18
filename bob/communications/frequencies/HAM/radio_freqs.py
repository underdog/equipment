import requests
from bs4 import BeautifulSoup
import os
import sys

baseurl = 'https://www.radioreference.com/apps/db/'
response = requests.get(baseurl, verify=False)
soup = BeautifulSoup(response.text, 'lxml')
form = soup.find_all('form')
usoptions = form[8]
uslist = []
for x in usoptions.find_all('option'):
  uslist.append([x['value'], x.text])

#url = 'https://www.radioreference.com/apps/db/?stid=48&tab=ham'

for x in uslist:
  url = baseurl + '?stid=' + str(x[0]) + '&tab=ham'
  filename = x[1]
  response = requests.get(url, verify=False)
  soup = BeautifulSoup(response.text, 'html')
  freqs = soup.find('table',{'class':'rrtable'})
  f = freqs.text.split('\n')
  skipnext = False
  iterations = 1
  with open(filename, 'w') as outfile:
    for i in range(2, len(f)):
      if i%9 == 0:
        print('')
        outfile.write('\n')
        skipnext = True
        iterations += 1
      elif skipnext:
        skipnext = False
      else:
        if i % ((8*iterations)+(iterations-1)) == 0:
          outfile.write('{}'.format(f[i]))
          print('{}'.format(f[i]), end='')
        else:
          outfile.write('{},'.format(f[i]))
          print('{},'.format(f[i]), end='')
  outfile.close()