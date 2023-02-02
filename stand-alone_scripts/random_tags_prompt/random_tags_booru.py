import requests
from bs4 import BeautifulSoup
import sys
import random 

def print_p(text):
    text = text.replace('(', '\(').replace(')', '\)')
    print(text)
    
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

def get_danbooru(url='https://danbooru.donmai.us/posts/random'):
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


    tag_types_idx = [0]

    all_the_tags = []

    for tag_idx in tag_types_idx:
        tag_slice = tag_dict[tag_types[tag_idx][0]]
    #     print(tag_slice.findAll('li'))
        all_the_tags.append([_['data-tag-name'] for _ in tag_slice.findAll('li')])

    all_the_tags = ', '.join([', '.join(_) for _ in all_the_tags])
    all_the_tags = all_the_tags.replace('_', ' ')
    return r.url + '\n'*2 + all_the_tags


def get_gelbooru(url='https://gelbooru.com/index.php?page=post&s=random'):
    r = requests.get(url, headers=headers, allow_redirects=True)
    r.text

    soup = BeautifulSoup(r.text,'html.parser')
    tab = soup.find("ul",{"class":"tag-list"})

    tag_types =['tag-type-artist',
    'tag-type-character',
    'tag-type-copyright',
    'tag-type-metadata',
    'tag-type-general']


    tag_types_idx = [-1]

    all_the_tags = []
    for tag_type_idx in tag_types_idx:
        tag_type = tag_types[tag_type_idx]
        tags = [_ for _ in tab.findAll('li') if _.get("class") == [tag_type]]
        all_the_tags.append([[_.text for _ in tag.findAll('a')][-1] for tag in tags])

    all_the_tags = ', '.join([', '.join(_) for _ in all_the_tags])
    all_the_tags = all_the_tags.replace('_', ' ')
    return r.url + '\n'*2 + all_the_tags


def get_safebooru(url='https://safebooru.org/index.php?page=post&s=random'):
    r = requests.get(url, headers=headers, allow_redirects=True)


    soup = BeautifulSoup(r.text,'html.parser')
    tab = soup.find("ul",{"id":"tag-sidebar"})


    tag_types = ['tag-type-copyright tag',
    'tag-type-character tag',
    'tag-type-artist tag',
    'tag-type-general tag',
    'tag-type-metadata tag']
    tag_types = [_.split(' ') for _ in tag_types]

    tag_types_idx = [-2]

    all_the_tags = []
    for tag_type_idx in tag_types_idx:
        tag_type = tag_types[tag_type_idx]
        tags = [_ for _ in tab.findAll('li') if _.get('class') == tag_types[tag_type_idx]]
        all_the_tags.append([[_.text for _ in tag.findAll('a')][-1] for tag in tags])


    all_the_tags = ', '.join([', '.join(_) for _ in all_the_tags])
    all_the_tags = all_the_tags.replace('_', ' ')
    return r.url + '\n'*2 + all_the_tags

# def download_page(prompt):
#     ''' for gcolab use '''
#     url_page = '"' + prompt.split('\n')[0] + '"'
#     !wget $url_page -O 'webpage' -q
#     with open('webpage', 'r') as f:
#         data = f.readlines()
#     url_img = [_ for _ in data if '<meta property="og:image" itemprop="image" content="' in _][0]
#     url_img = url_img.split('content="')[-1].split('" />')[0]
#     !wget $url_img -O 'img.jpg' -q
#     display(Image('img.jpg'))

# gelbooru, danbooru, safebooru
try:
    ARGV = sys.argv
    SOURCE = ARGV[1]
except Exception as e:
    SOURCE = 'gelbooru'

url = None
search = None

if SOURCE == 'url':
    url = ARGV[-1]
    type_booru = url.split('/')[2].split('.')[0]
    SOURCE = type_booru

if SOURCE == 'search':
    type_booru = ARGV[2]
    search = '+'.join(ARGV[3:])
    SOURCE = type_booru
    if SOURCE == 'safebooru':
        url_search = f"https://safebooru.org/index.php?page=post&s=list&tags={search.replace(' ', '+')}"
        print(url_search, '\n')
        r = requests.get(url_search, headers=headers, allow_redirects=True)

        soup = BeautifulSoup(r.text,'html.parser')
        tab = soup.find("div",{"class":"pagination"})

        last_page = int([_ for _ in tab][-1]['href'].split('pid=')[-1])//40
        page = random.randint(1, last_page)
        new_url = f"https://safebooru.org/index.php?page=post&s=list&tags={search.replace(' ', '+')}&pid={page*40%last_page}"
        r = requests.get(new_url, headers=headers, allow_redirects=True)

        soup = BeautifulSoup(r.text,'html.parser')
        tab = soup.find("div",{"class":"content"})
        url_list = [_['href'] for _ in tab.findAll('a') if 'pid=' not in _['href']]

        url = f'https://safebooru.org/{random.choice(url_list)}'

    else:
        assert False, "Only safebooru is implemented"



if SOURCE == 'danbooru':
    if not url:
        url = 'https://danbooru.donmai.us/posts/random'
    prompt = get_danbooru(url)
    print_p(prompt)


elif SOURCE == 'gelbooru':
    if not url:
        url = 'https://gelbooru.com/index.php?page=post&s=random'
    prompt = get_gelbooru(url)
    print_p(prompt)

elif SOURCE == 'safebooru':
    if not url:
        url = 'https://safebooru.org/index.php?page=post&s=random'
    prompt = get_safebooru(url)
    print_p(prompt)


else:
    print('You can use only gelbooru, danbooru or safebooru links!')
    print(f'Your arguments are { ARGV}')
