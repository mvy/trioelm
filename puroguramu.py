from jinja2 import FileSystemLoader, Environment
import yaml
import re
import glob
import os
import datetime

env = Environment()
env.loader = FileSystemLoader('.')

program = yaml.load(open('puroguramu.yaml').read())
full_piece = {}
youtube = {}
concert_of = {}
for piece in program:
    key = piece['key']
    full_piece[key] = piece
    work = piece['anime'] if 'anime' in piece else piece['game']
    full_piece[key]['work'] = work
    full_piece[key]['url'] = 'http://youtu.be/%s' % piece['youtube'] if 'youtube' in piece else '#'
    if 'youtube' in piece:
        for concert_key in piece['youtube']:
            concert_of[piece['youtube'][concert_key]] = concert_key
            youtube[piece['youtube'][concert_key]] = ('%s %s' % (work, piece.get('desc', 'OST')), piece['title'])

page = env.get_template('program.tpl.html')

all_concerts = []
pieces = {'jj': ['Walt']}
for filename in glob.glob('concerts/*.yaml'):
    pagename = filename.replace('.yaml', '.html')
    concert_key = os.path.basename(filename).replace('.yaml', '')
    concert = yaml.load(open(filename).read())
    concert['url'] = pagename
    for category in ['program', 'encores']:
        if category in concert:
            for key in concert[category]:
                pieces.setdefault(concert_key, []).append(key)
                piece = full_piece[key].copy()  # Il faut copier pour éventuellement remplacer la vidéo
                if 'youtube' in piece:
                    piece['url'] = next(iter(piece['youtube'].values()))  # Par défaut, la première vidéo qui vient
                    if concert_key in piece['youtube']:
                        piece['url'] = 'http://youtu.be/%s' % piece['youtube'][concert_key]  # En priorité, on choisit la vidéo du concert courant
                concert.setdefault('full_%s' % category, []).append(piece)
    all_concerts.append(concert)

all_concerts.sort(key=lambda concert: datetime.datetime.strptime(concert['date'], '%d/%m/%Y'), reverse=True)

for concert in all_concerts:
    with open(concert['url'], 'w') as f:
        f.write(page.render(concert=concert, all_concerts=all_concerts))

for piece in program:
    if 'youtube' in piece:
        for concert_key in piece['youtube']:
            if piece['key'] not in pieces[concert_key]:
                raise ValueError('You did not play %s at %s!' % (piece['title'], concert_key))

videos = yaml.load(open('videos.yaml').read())
all_videos = []
for video in videos:
    m = re.search(r'Trio ELM.* - (.*) \(([^)]*?)(?: cover)?(?:, TV size)?\)', video['title'])
    fallback_title, fallback_work = m.groups()
    if video['id'] in youtube:
        work, title = youtube[video['id']]
        if title != fallback_title:
            print(title, fallback_title)
        if work != fallback_work:
            print(work, fallback_work)
    else:
        print('Warning:', video['id'], 'is missing in puroguramu.yaml (%s)' % video['title'])
        title, work = fallback_title, fallback_work
    all_videos.append(dict(id=video['id'], title=title, work=work, concert=concert_of[video['id']], featured=video.get('featured')))

# Generate index
# os.system('cp concerts/telethon-ii.html index.html')
page = env.get_template('index.tpl.html')
with open('index.html', 'w') as f:
    f.write(page.render(all_concerts=all_concerts, all_videos=all_videos))
