from collections import defaultdict
from copy import deepcopy
import string
import re
# import unicode
## regex for finding sloka number
regex = r"(\d+)\-(\d+)\-(\d+)"
exclude = list(set(string.punctuation))
# ANy is the prose, Slo is the sloka
slpAny = [item.split() for item in open('data/slpAny.txt').read().splitlines()]
slpSlo = [item.split() for item in open('data/slpSlo.txt').read().splitlines()]

sloAnv = defaultdict(dict)
for i,item in enumerate(slpSlo):
    if unicode(item[0], 'utf-8').isnumeric() == False:
        print (item)

    sloAnv[int(item[0])]['slo'] = list()
    st = []
    for stuff in item[1:]:
        match = re.search(regex, stuff)
        if match is not None:
            if match.start() != 0:
                stuff2 = re.sub(regex,'',stuff)

            elif match.end()!= len(stuff):
                stuff2 = re.sub(regex,'',stuff)
        else:
            stuff2 = stuff
        st.append(stuff2)
    stuff2 = ' '.join(st)
    stuff2 = stuff2.strip()
    stuff2 = ''.join([ch for ch in stuff2 if ch not in exclude])
    if len(stuff2) > 0:
        sloAnv[int(item[0])]['slo'].append(stuff2)
    # print i
for item in slpAny:
    sloAnv[int(item[0])]['anv'] = list()
    if unicode(item[0], 'utf-8').isnumeric() == False:
        print ('anv',item)
    stuff = ' '.join(item[1:])
    stuff = stuff.strip()
    stuff = ''.join([ch for ch in stuff if ch not in exclude])
    if len(stuff) > 0:
        sloAnv[int(item[0])]['anv'].append(stuff)
    # sloAnv[int(item[0])]['anv'] = [stuff.strip().translate(translator).strip() for stuff in item[1:]]

f1 = open('data/poetry.txt', 'w')
f2 = open('data/prose.txt', 'w')

for keys in sloAnv.keys():
    k = sloAnv[keys].keys()
    if 'slo' in k and 'anv' in k:
        f1.write(str(sloAnv[keys]['slo'][0].strip()) + '\n')
        f2.write(str(sloAnv[keys]['anv'][0].strip()) + '\n')
print len(sloAnv)
