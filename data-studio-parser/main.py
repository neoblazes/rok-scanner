# -*- coding: utf-8 -*-

def parse_file(fname):
    f = open(fname, encoding='utf-8')
    l = f.readlines()

    for i in range(len(l)):
        l[i] = l[i].rstrip('\n')
        l[i] = l[i].replace(',', '')
        try:
            if l[i][-1] == 'B':
                l[i] = str(int(float(l[i][:-1]) * 1000000000))
            if l[i][-1] == 'M':
                l[i] = str(int(float(l[i][:-1]) * 1000000))
            if l[i][-1] == 'K':
                l[i] = str(int(float(l[i][:-1]) * 1000))
        except:
            pass

    i = 0
    parsed = []
    while i + 31 < len(l):
        parsed.append([l[i+1], l[i+3], l[i+9], l[i+12], l[i+15], l[i+18], l[i+31]])
        i += 32
    return parsed

parsed = parse_file('data_studio_raw.txt')

csv_lines = [','.join(p) for p in parsed]
f = open('data_stadio.csv', 'w', encoding='utf-8')
f.write('Governor,ID,Killpoints,T4,Kills,T5,Kills,Deads,DKP\n')
f.write('\n'.join(csv_lines))