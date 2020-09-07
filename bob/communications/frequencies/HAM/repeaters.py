#Pulls repeater list from repeaterbook
#writes to single file for now
#currently requires adding state with id number from site into the states dictionary
import requests
from bs4 import BeautifulSoup
import os

def get_repeaters(soup, state, file):
  table = (soup.find('table', {'class':'w3-table sortable w3-responsive w3-striped'}))
  t = table.text.split('\n')
  with open(file, "a") as of:
    print(f'STATE: {state}')
    of.write(f'STATE: {state}\n')
    #29.6800,-0.1 MHz,,123.0,Rose Hill,Harris,K5SOH,,OPEN,,,FM,,,,
    of.write(f'Frequency,Offset,,Tone Up/Down,Location,County,Call,,Use,,,Modes\n')
    count = 1
    for td in range(12,len(t)):
      if count % 16 == 0:
        if t[td].strip() == '':
          print(f'{t[td].strip()}')
          of.write(f'{t[td].strip()}\n')
        else:
          print(f'\n{t[td].strip()},', end='')
          of.write(f'\n{t[td].strip()},')
      else:
        print(f'{t[td].strip()},', end='')
        of.write(f'{t[td].strip()},')
      count += 1
    print(f'\n\n\n')
    of.write(f'\n\n\n')
  of.close()



states = {'Texas':48, 'Louisiana':22, 'Oklahoma':40, 'Arkansas':5, 'New Mexico':35}
file = 'repeater_list.csv'
if os.path.isfile(file):
  os.remove(file)
for k,v in states.items():
  if v <= 10:
    v = '0' + str(v)
  url = 'https://www.repeaterbook.com/repeaters/Display_SS.php?state_id=' + str(v) + '&band=%&loc=%&call=%&use=%'
  print(url)
  response = requests.get(url, verify=False)
  soup = BeautifulSoup(response.text, 'lxml')
  get_repeaters(soup, k, file)

