import yaml
import glob
import os
import jinja2
import datetime

program = yaml.load(open('puroguramu.yaml').read())
full_piece = {}
for piece in program:
    key = piece['key']
    full_piece[key] = piece
    full_piece[key]['work'] = piece['anime'] if 'anime' in piece else piece['game']
    full_piece[key]['url'] = 'http://youtu.be/%s' % piece['youtube'] if 'youtube' in piece else '#'

page = jinja2.Template(open('program.tpl.html').read())

all_concerts = []
for filename in glob.glob('concerts/*.yaml'):
    pagename = filename.replace('.yaml', '.html')
    basename = os.path.basename(filename).replace('.yaml', '')
    concert = yaml.load(open(filename).read())
    concert['url'] = pagename
    for category in ['program', 'encores']:
        if category in concert:
            for key in concert[category]:
                piece = full_piece[key].copy()  # We need to make a copy
                if basename in piece:
                    piece['url'] = 'http://youtu.be/%s' % piece[basename]
                concert.setdefault('full_%s' % category, []).append(piece)
    all_concerts.append(concert)

all_concerts.sort(key=lambda concert: datetime.datetime.strptime(concert['date'], '%d/%m/%Y'), reverse=True)

for concert in all_concerts:
    with open(concert['url'], 'w') as f:
        f.write(page.render(concert=concert, all_concerts=all_concerts))

# Generate index
# os.system('cp concerts/telethon-ii.html index.html')
page = jinja2.Template(open('index.tpl.html').read())
with open('index.html', 'w') as f:
    f.write(page.render(all_concerts=all_concerts))
