import requests
from bs4 import BeautifulSoup
import sys


headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}


# gelbooru and danbooru
try:
    SOURCE = sys.argv[1]
except Exception as e:
    SOURCE = 'gelbooru'

if SOURCE == 'danbooru':
    url = 'https://danbooru.donmai.us/posts/random'
    r = requests.get(url, headers=headers, allow_redirects=True)


    soup = BeautifulSoup(r.text,'html.parser')
    tab = soup.find("div",{"class":"tag-list categorized-tag-list"})
    tables = tab.findAll('ul')

    tag_dict = {table.get('class')[0]:table for table in tab.findAll('ul')}
    # "tag-type-0" - general-tag-list
    # "tag-type-1" - artist-tag-list
    # "tag-type-3" - copyright-tag-list
    # "tag-type-4" - character-tag-list
    # "tag-type-5" - meta-tag-list

    tag_types = [['general-tag-list', "tag-type-0"],
     ['artist-tag-list', "tag-type-1"], None,
     ['copyright-tag-list', "tag-type-3"],
     ['character-tag-list', "tag-type-4"],
     ['meta-tag-list', "tag-type-5"]]


    tag_types_idx = [0]  # add indexes from tag_types if you want other ones, for example [-1, 0, 3] 

    all_the_tags = []

    for tag_idx in tag_types_idx:
        tag_slice = tag_dict[tag_types[tag_idx][0]]
    #     print(tag_slice.findAll('li'))
        all_the_tags.append([_['data-tag-name'] for _ in tag_slice.findAll('li')])

    all_the_tags = ', '.join([', '.join(_) for _ in all_the_tags])
    all_the_tags = all_the_tags.replace('_', ' ')
    print(r.url, '\n')
    print(all_the_tags)



elif SOURCE == 'gelbooru':

    url = 'https://gelbooru.com/index.php?page=post&s=random'
    r = requests.get(url, headers=headers, allow_redirects=True)
    r.text

    soup = BeautifulSoup(r.text,'html.parser')
    tab = soup.find("ul",{"class":"tag-list"})

    tag_types =['tag-type-artist',
    'tag-type-character',
    'tag-type-copyright',
    'tag-type-metadata',
    'tag-type-general']


    tag_types_idx = [-1] # add indexes from tag_types if you want other ones, for example [-1, 0, 3] 

    all_the_tags = []
    for tag_type_idx in tag_types_idx:
        tag_type = tag_types[tag_type_idx]
        tags = [_ for _ in tab.findAll('li') if _.get("class") == [tag_type]]
        all_the_tags.append([[_.text for _ in tag.findAll('a')][-1] for tag in tags])

    all_the_tags = ', '.join([', '.join(_) for _ in all_the_tags])
    all_the_tags = all_the_tags.replace('_', ' ')
    print(r.url, '\n')
    print(all_the_tags)
else:
    print('You can use only gelbooru and danbooru links!')
