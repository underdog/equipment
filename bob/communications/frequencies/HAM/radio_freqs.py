import requests
from bs4 import BeautifulSoup
import os
import sys

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
baseurl = 'https://www.radioreference.com/apps/db/'
response = requests.get(baseurl, verify=False)
soup = BeautifulSoup(response.text, 'lxml')
form = soup.find_all('form')
usoptions = form[8]
uslist = []
for x in usoptions.find_all('option'):
  uslist.append([x['value'], x.text])

#url = 'https://www.radioreference.com/apps/db/?stid=48&tab=ham'
counter_0 = 1
basedir = os.getcwd()
statedir = basedir + '/states'
if not os.path.isdir(statedir):
  os.mkdir(statedir)
for x in uslist:
  os.chdir(basedir)
  url = baseurl + '?stid=' + str(x[0]) + '&tab=ham'
  stateurl = baseurl + '?stid=' + str(x[0])
  statename = x[1]
  response = requests.get(url, verify=False)
  soup = BeautifulSoup(response.text, 'html')
  freqs = soup.find('table',{'class':'rrtable'})
  f = freqs.text.split('\n')
  skipnext = False
  iterations = 1
  with open(statename, 'w') as outfile:
    print(statename)
    for i in range(2, len(f)):
      if i%9 == 0:
        #print('')
        outfile.write('\n')
        skipnext = True
        iterations += 1
      elif skipnext:
        skipnext = False
      else:
        if i % ((8*iterations)+(iterations-1)) == 0:
          outfile.write('{}'.format(f[i]))
          #print('{}'.format(f[i]), end='')
        else:
          outfile.write('{},'.format(f[i]))
          #print('{},'.format(f[i]), end='')
  outfile.close()
  try:
    os.chdir(statedir)
    os.mkdir(statename)
  except:
    continue
  os.chdir(statename)
  response = requests.get(stateurl, verify=False)
  soup = BeautifulSoup(response.text, 'html')
  counties = soup.find_all('option')
  for ct in counties:
    if 'ctid' in ct['value']:
      ctid = str(ct['value'].split(',')[1])
      countyname = ct.text.strip()
      print(f'\t{countyname}')
      countyurl = baseurl + '?inputs=1&ctid=' + ctid
      #print(f'{ctid}\t', end='')
      #print(f'{countyname}\t', end='')
      #print(f'{countyurl}')
      try:
        response = requests.get(countyurl, verify=False)
      except:
        response = requests.get(countyurl, verify=False)
        continue
      soup = BeautifulSoup(response.text, 'html')
      td = soup.find_all('td',{'class':['td0','td1']})
      count = 1
      with open(countyname, 'w') as outfile:
        for x in range(0, len(td)):
          if count%9 == 0:
            #print(f'{td[x].text}')
            outfile.write(f'{td[x].text}\n')
            count += 1
          else:
            #print(f'{td[x].text}\t', end='')
            outfile.write(f'{td[x].text}\t')
            count += 1
      outfile.close()
  os.chdir(basedir)
  #os.chdir(basedir)
#     for item in range(0, len(td)):
#        countyname = item.text
#        with open(countyname) as outfile:
#          ctid = item['value'].split(',')[2]
#          countyurl = baseurl + '?ctid=' + ctid
#          response = requests.get(countyurl, verify=False)
#          soup = BeautifulSoup(response.text, 'html')
#          td = soup.find_all('td',{'class':['td0','td1']})
#          for x in range(0,len(t)):
#            if count%8==0:
#              print(f'{t[x].text}')
#              count += 1
#            else:
#              print(f'{t[x].text}\t', end='')
#              count += 1

#soup.find_all('td',{'class':['td0','td1']})
#for x in range(0,len(t)):
#  if count%8==0:
#    print(f'{t[x].text}')
#    count += 1
#  else:
#    print(f'{t[x].text}\t', end='')
#    count += 1
